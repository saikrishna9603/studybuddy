"""
ML Engine - Pure Python ML logic for placement preparation
No external APIs - all predictions based on datasets and algorithms
"""

import re
import logging
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher
from .ml_data import (
    SKILLS_DATABASE,
    ROLE_SKILLS_MAP,
    QUESTION_BANK,
    ANSWER_KEYWORDS,
    EXPERIENCE_LEVELS,
    ROADMAP_TOPICS,
    SCORING_RUBRIC,
    COMMON_MISTAKES,
    STRENGTHS_INDICATORS
)

logger = logging.getLogger(__name__)

# ============================================================================
# 1. SKILL EXTRACTION FROM RESUME TEXT
# ============================================================================

def extract_skills(resume_text: str) -> Dict:
    """
    Extract skills from resume text using pattern matching and keyword extraction.
    
    Args:
        resume_text: Raw resume content
        
    Returns:
        Dictionary with extracted and matched skills
    """
    if not resume_text:
        logger.warning("Empty resume text provided")
        return {"matched_skills": [], "confidence": 0}
    
    text_lower = resume_text.lower()
    matched_skills = []
    skill_matches = {}
    
    # Direct keyword matching
    for skill, skill_info in SKILLS_DATABASE.items():
        # Exact and fuzzy matching
        if skill in text_lower:
            matched_skills.append(skill)
            skill_matches[skill] = {"method": "exact", "confidence": 1.0}
        else:
            # Fuzzy match for variations
            similarity = _fuzzy_match(skill, text_lower)
            if similarity > 0.7:
                matched_skills.append(skill)
                skill_matches[skill] = {"method": "fuzzy", "confidence": similarity}
    
    # Remove duplicates and sort by confidence
    unique_skills = list(set(matched_skills))
    
    logger.info(f"🔵 Extracted {len(unique_skills)} skills from resume")
    
    return {
        "matched_skills": unique_skills,
        "skill_details": skill_matches,
        "confidence": len(unique_skills) / len(SKILLS_DATABASE),
        "count": len(unique_skills)
    }


def _fuzzy_match(skill: str, text: str) -> float:
    """Fuzzy string matching for skill detection."""
    words = text.split()
    max_similarity = 0
    
    for word in words:
        similarity = SequenceMatcher(None, skill, word).ratio()
        max_similarity = max(max_similarity, similarity)
    
    return max_similarity


# ============================================================================
# 2. EXPERIENCE LEVEL CLASSIFICATION
# ============================================================================

def classify_experience(skills: List[str]) -> Dict:
    """
    Classify experience level based on number and type of skills.
    
    Args:
        skills: List of matched skills
        
    Returns:
        Experience classification with details
    """
    skill_count = len(skills) if isinstance(skills, list) else 0
    
    # Advanced skills boost (3+ advanced skills = senior+)
    advanced_skills = [s for s in skills if SKILLS_DATABASE.get(s, {}).get("level", 1) >= 3]
    advanced_boost = len(advanced_skills) * 0.5
    
    effective_count = skill_count + advanced_boost
    
    for level_name, level_config in EXPERIENCE_LEVELS.items():
        if level_config["min_skills"] <= effective_count <= level_config["max_skills"]:
            logger.info(f"📊 Classified experience as: {level_name} ({skill_count} skills)")
            return {
                "level": level_name,
                "skill_count": skill_count,
                "advanced_skills": advanced_skills,
                "confidence": min(1.0, effective_count / 15)  # Normalize to 0-1
            }
    
    # Default to expert if too many skills
    logger.info(f"🚀 Classified as EXPERT ({skill_count} skills)")
    return {
        "level": "expert",
        "skill_count": skill_count,
        "advanced_skills": advanced_skills,
        "confidence": 0.95
    }


# ============================================================================
# 3. ROLE PREDICTION
# ============================================================================

def predict_roles(skills: List[str]) -> Dict:
    """
    Predict best matching roles based on user skills.
    
    Args:
        skills: List of user's skills
        
    Returns:
        Ranked list of matching roles
    """
    skills_set = set(s.lower() for s in skills)
    role_scores = {}
    
    for role, role_config in ROLE_SKILLS_MAP.items():
        required = set(role_config["required"])
        preferred = set(role_config["preferred"])
        
        # Calculate match score
        required_match = len(skills_set & required) / len(required) if required else 0
        preferred_match = len(skills_set & preferred) / len(preferred) if preferred else 0
        
        # Weighted score (required is more important)
        score = (required_match * 0.7) + (preferred_match * 0.3)
        
        # Store matching skills
        matched_required = skills_set & required
        matched_preferred = skills_set & preferred
        
        role_scores[role] = {
            "score": score * 100,  # Convert to percentage
            "matched_required": list(matched_required),
            "matched_preferred": list(matched_preferred),
            "missing_required": list(required - skills_set),
            "missing_preferred": list(preferred - skills_set)
        }
    
    # Sort by score
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1]["score"], reverse=True)
    top_roles = sorted_roles[:3]  # Top 3 predictions
    
    logger.info(f"🎯 Predicted roles: {[r[0] for r in top_roles]}")
    
    return {
        "predicted_roles": [{"name": r[0], **r[1]} for r in top_roles],
        "all_scores": {k: v["score"] for k, v in role_scores.items()}
    }


# ============================================================================
# 4. QUESTION GENERATION
# ============================================================================

def generate_questions(skills: List[str], level: str = "medium", count: int = 6) -> Dict:
    """
    Generate interview questions based on skills and difficulty level.
    
    Args:
        skills: List of user's skills
        level: Difficulty level (easy, medium, hard)
        count: Number of questions to generate
        
    Returns:
        Structured question set
    """
    if level not in QUESTION_BANK.get(skills[0] if skills else "python", {}):
        level = "medium"
    
    generated_questions = {
        "technical": [],
        "behavioral": [],
        "coding": []
    }
    
    # Generate technical questions from user's top skills
    for skill in skills[:3]:  # Top 3 skills
        skill_questions = QUESTION_BANK.get(skill, {}).get(level, [])
        if skill_questions:
            generated_questions["technical"].append({
                "question": skill_questions[0],
                "skill": skill,
                "difficulty": level,
                "keywords": ANSWER_KEYWORDS.get(skill_questions[0], {}).get("keywords", [])
            })
    
    # Add behavioral questions
    generated_questions["behavioral"] = [
        {
            "question": "Tell me about a challenging problem you solved",
            "difficulty": level,
            "type": "behavioral"
        },
        {
            "question": "Describe a situation where you had to learn a new technology quickly",
            "difficulty": level,
            "type": "behavioral"
        }
    ]
    
    # Add coding questions if technical skills exist
    if skills:
        generated_questions["coding"] = [
            {
                "question": "Write a function to reverse a linked list",
                "difficulty": "medium",
                "type": "coding"
            }
        ]
    
    logger.info(f"✏️ Generated {len(generated_questions['technical'])} technical questions")
    
    return {
        "questions": generated_questions,
        "total_count": sum(len(v) for v in generated_questions.values()),
        "difficulty": level
    }


# ============================================================================
# 5. ANSWER EVALUATION
# ============================================================================

def evaluate_answer(question: str, user_answer: str) -> Dict:
    """
    Evaluate user's answer using keyword matching and heuristics.
    
    Args:
        question: The interview question
        user_answer: User's answer text
        
    Returns:
        Detailed evaluation with scoring
    """
    if not user_answer or len(user_answer) < 10:
        logger.warning("Answer too short for evaluation")
        return {
            "overall_score": 2,
            "scores": {"correctness": 1, "completeness": 2, "clarity": 1, "depth": 1},
            "strengths": ["Complete answer provided"],
            "weaknesses": ["Answer is too short", "Provide more detail"],
            "tips": ["Try to explain your reasoning in more detail"]
        }
    
    answer_lower = user_answer.lower()
    expected_keywords = ANSWER_KEYWORDS.get(question, {}).get("keywords", [])
    depth_keywords = ANSWER_KEYWORDS.get(question, {}).get("depth_keywords", [])
    
    # Calculate keyword matches
    keyword_matches = sum(1 for kw in expected_keywords if kw in answer_lower)
    depth_matches = sum(1 for kw in depth_keywords if kw in answer_lower)
    
    # Score components
    correctness = (keyword_matches / len(expected_keywords) * 10) if expected_keywords else 7
    completeness = min(10, len(user_answer) / 50)  # Longer = more complete
    clarity = 7 if len(user_answer.split()) > 20 else 4  # Better structure = later
    depth = (depth_matches / len(depth_keywords) * 10) if depth_keywords else 6
    
    # Weighted overall score
    scores = {
        "correctness": min(10, correctness),
        "completeness": min(10, completeness),
        "clarity": min(10, clarity),
        "depth": min(10, depth)
    }
    
    overall_score = (
        scores["correctness"] * SCORING_RUBRIC["correctness"]["weight"] +
        scores["completeness"] * SCORING_RUBRIC["completeness"]["weight"] +
        scores["clarity"] * SCORING_RUBRIC["clarity"]["weight"] +
        scores["depth"] * SCORING_RUBRIC["depth"]["weight"]
    )
    
    # Generate feedback
    strengths = []
    if keyword_matches > len(expected_keywords) * 0.5:
        strengths.append("Good coverage of key concepts")
    if len(user_answer) > 200:
        strengths.append("Detailed and comprehensive answer")
    if depth_matches > 0:
        strengths.append("Shows deeper understanding")
    
    weaknesses = []
    if keyword_matches < len(expected_keywords) * 0.3:
        weaknesses.append("Missing some key concepts")
    if len(user_answer) < 100:
        weaknesses.append("Answer could be more detailed")
    if depth_matches == 0:
        weaknesses.append("Could provide more advanced insights")
    
    logger.info(f"📊 Evaluated answer: {overall_score:.1f}/10")
    
    return {
        "overall_score": round(overall_score, 1),
        "scores": {k: round(v, 1) for k, v in scores.items()},
        "keyword_coverage": keyword_matches / len(expected_keywords) if expected_keywords else 0,
        "depth_coverage": depth_matches / len(depth_keywords) if depth_keywords else 0,
        "strengths": strengths or ["Attempted the question"],
        "weaknesses": weaknesses or ["Continue improving"],
        "tips": [
            "Review the key concepts mentioned in the expected answer",
            "Provide specific examples to strengthen your response",
            "Discuss edge cases and trade-offs when applicable"
        ],
        "model_answer": ANSWER_KEYWORDS.get(question, {}).get("ideal", "See resources for ideal answer")
    }


# ============================================================================
# 6. ROADMAP GENERATION
# ============================================================================

def generate_roadmap(skills: List[str], days: int = 21) -> Dict:
    """
    Generate personalized learning roadmap based on skill gaps.
    
    Args:
        skills: User's current skills
        days: Duration of roadmap
        
    Returns:
        Structured learning roadmap
    """
    skills_set = set(s.lower() for s in skills)
    
    # Identify weak areas
    weak_areas = []
    for skill_category, topics in ROADMAP_TOPICS.items():
        weak_areas.append({
            "topic": skill_category,
            "priority": "high" if len(skills) < 5 else "medium",
            "subtopics": topics["subtopics"][:3],  # First 3 subtopics
            "duration": topics["duration_days"]
        })
    
    # Create daily plan (distribute topics across days)
    daily_plan = []
    topics_per_day = max(1, len(weak_areas) / (days / 7))  # Spread across weeks
    
    for i in range(days):
        week = i // 7
        day_of_week = i % 7
        topic_idx = int(i * topics_per_day / days)
        
        if topic_idx < len(weak_areas):
            daily_plan.append({
                "day": i + 1,
                "week": week + 1,
                "activity": f"Learn {weak_areas[topic_idx]['topic']}",
                "duration": "2-3 hours",
                "resources": ["Online course", "Practice problems"],
                "milestone": "Ready for interview" if (i + 1) == days else None
            })
    
    # Generate milestones
    milestones = [
        {"week": 1, "goal": "Understand fundamentals", "skills": 3},
        {"week": 2, "goal": "Intermediate practice", "skills": 5},
        {"week": 3, "goal": "Advanced concepts", "skills": 8}
    ][:days // 7]
    
    logger.info(f"🗺️ Generated {days}-day roadmap with {len(weak_areas)} topics")
    
    return {
        "duration_days": days,
        "weak_areas": weak_areas,
        "daily_plan": daily_plan,
        "milestones": milestones,
        "topics": [t["topic"] for t in weak_areas],
        "total_hours": sum(t["duration"] for t in weak_areas),
        "resources": {
            "online": ["Coursera", "Udemy", "YouTube"],
            "practice": ["LeetCode", "HackerRank", "CodeSignal"],
            "community": ["GitHub", "Stack Overflow", "Dev Communities"]
        }
    }


# ============================================================================
# 7. HELPER FUNCTIONS
# ============================================================================

def calculate_ats_score(skills: List[str], experience_level: str) -> int:
    """Calculate ATS resume score based on skills."""
    base_score = min(100, len(skills) * 5)
    level_boost = {"fresher": 0, "junior": 10, "intermediate": 20, "senior": 30, "expert": 40}.get(experience_level, 0)
    return min(100, base_score + level_boost)


def get_interview_tips(level: str) -> List[str]:
    """Get interview tips based on experience level."""
    tips = {
        "fresher": [
            "Focus on learning and growth mindset",
            "Ask clarifying questions",
            "Be honest about what you don't know",
            "Discuss your projects and learning journey"
        ],
        "intermediate": [
            "Discuss system design concepts",
            "Provide specific metrics for your work",
            "Mention optimizations you've implemented",
            "Ask about team structure and challenges"
        ],
        "senior": [
            "Lead the discussion with insights",
            "Discuss architectural decisions",
            "Share lessons learned from failures",
            "Ask about growth opportunities"
        ]
    }
    return tips.get(level, tips["intermediate"])


def predict_success_rate(skills: List[str], predicted_roles: List[Dict]) -> Dict:
    """
    Predict likelihood of success for predicted roles.
    
    Args:
        skills: User skills
        predicted_roles: Predicted roles
        
    Returns:
        Success prediction data
    """
    if not predicted_roles:
        return {"prediction": "Unable to predict", "confidence": 0}
    
    top_role = predicted_roles[0]
    match_score = top_role.get("score", 0)
    
    # Higher score = better chance
    if match_score >= 80:
        prediction = "Very likely to succeed"
    elif match_score >= 60:
        prediction = "Good chance of success"
    elif match_score >= 40:
        prediction = "Moderate chance - focus on gaps"
    else:
        prediction = "Focus on building foundational skills"
    
    return {
        "prediction": prediction,
        "confidence": min(1.0, match_score / 100),
        "role": top_role.get("name"),
        "match_score": match_score
    }
