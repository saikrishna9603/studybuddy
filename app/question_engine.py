"""
Question Engine Module

Generates company-specific interview questions based on resume analysis,
company tech stack, and company interview patterns.

FIXED: Added comprehensive logging and error handling
"""

import json
import logging
import os
import random
import re

logger = logging.getLogger(__name__)

# Import the placement AI fix module for proper LLM handling
try:
    from .placement_ai_fix import PlacementAIFix
    logger.info("✅ Imported PlacementAIFix module")
except ImportError:
    logger.error("❌ Failed to import PlacementAIFix")
    PlacementAIFix = None


class QuestionEngine:
    """Generate tailored interview questions for specific companies."""
    
    # Fall back questions for when LLM fails
    FALLBACK_QUESTIONS = {
        'technical': [
            "Explain the concept of RESTful APIs and how they work.",
            "What is the difference between SQL and NoSQL databases?",
            "Describe the MVC architecture pattern.",
            "What is caching and why is it important?",
            "Explain the concept of microservices.",
        ],
        'behavioral': [
            "Tell me about a challenging project you worked on.",
            "Describe a time you had to work with a difficult team member.",
            "How do you handle tight deadlines?",
            "Give an example of when you showed leadership.",
            "Describe a time you learned something new quickly.",
        ],
        'coding': [
            "Reverse a string without using built-in functions.",
            "Find the two numbers in a list that sum to a target.",
            "Implement a function to detect if a string has balanced parentheses.",
            "Write a function to find the longest substring without repeating characters.",
            "Implement a simple LRU cache.",
        ]
    }
    
    # Company tech stacks (commonly known)
    COMPANY_TECH_STACKS = {
        'Google': ['Python', 'Java', 'C++', 'JavaScript', 'Go'],
        'Microsoft': ['C#', '.NET', 'Azure', 'JavaScript', 'TypeScript'],
        'Amazon': ['Java', 'JavaScript', 'Python', 'AWS', 'DynamoDB'],
        'Meta': ['Python', 'JavaScript', 'React', 'GraphQL', 'Hack'],
        'Apple': ['Swift', 'Objective-C', 'C++', 'Java'],
        'Netflix': ['Java', 'JavaScript', 'Python', 'AWS', 'Kafka'],
        'Uber': ['Go', 'Java', 'Python', 'Node.js', 'Kafka'],
        'Airbnb': ['JavaScript', 'React', 'Java', 'Python', 'AWS'],
        'LinkedIn': ['Java', 'JavaScript', 'Python', 'Scala', 'Kafka'],
        'Twitter': ['Scala', 'Java', 'JavaScript', 'Ruby'],
    }
    
    def __init__(self):
        """Initialize question engine."""
        pass
    
    def generate_questions(self, company, profile_data, role='Software Engineer', num_questions=10):
        """
        Generate interview questions for a specific company.
        
        Args:
            company (str): Company name
            profile_data (dict): User's resume analysis data
            role (str): Target job role
            num_questions (int): How many questions to generate (default 10)
            
        Returns:
            dict: Questions organized by type (technical, behavioral, coding)
        """
        logger.info(f"🚀 Starting question generation: {num_questions} questions for {role} at {company}")
        logger.debug(f"Profile data: {profile_data}")
        
        questions = {
            'technical': [],
            'behavioral': [],
            'coding': []
        }
        
        try:
            # Try using OpenAI first
            logger.info("📍 Attempting question generation with OpenAI")
            questions = self._generate_with_openai(company, profile_data, role, num_questions)
            if questions and any(questions.values()):
                logger.info("✅ Questions successfully generated with OpenAI")
                return questions
            else:
                logger.warning("⚠️ OpenAI returned empty questions, trying Gemini")
        except Exception as e:
            logger.warning(f"❌ OpenAI generation failed: {e}, attempting Gemini fallback")
            
        try:
            # Fallback to Gemini
            logger.info("📍 Attempting question generation with Gemini (fallback)")
            questions = self._generate_with_gemini(company, profile_data, role, num_questions)
            if questions and any(questions.values()):
                logger.info("✅ Questions successfully generated with Gemini (fallback)")
                return questions
            else:
                logger.warning("⚠️ Gemini also returned empty questions, using hardcoded fallback")
        except Exception as e2:
            logger.error(f"❌ Gemini generation failed: {e2}, using hardcoded fallback")
        
        # Use fallback questions
        logger.warning("⚠️ Using hardcoded fallback questions")
        return self._get_fallback_questions(num_questions)
    
    def _generate_with_openai(self, company, profile_data, role, num_questions):
        """Generate questions using OpenAI API with proper error handling."""
        logger.info(f"🔵 Generating {num_questions} questions for {role} at {company} via OpenAI")
        
        tech_stack = self.COMPANY_TECH_STACKS.get(company, [])
        user_skills = profile_data.get('technical_skills', {})
        experience = profile_data.get('experience_level', 'mid')
        
        logger.debug(f"User skills: {user_skills}")
        logger.debug(f"Company tech stack: {tech_stack}")
        logger.debug(f"Experience level: {experience}")
        
        prompt = f"""Generate exactly {num_questions} interview questions for a {role} position at {company}.

User Background:
- Experience Level: {experience}
- Technical Skills: {json.dumps(user_skills)}
- Projects: {', '.join(profile_data.get('projects', [])[:3])}

Company Info:
- Tech Stack: {', '.join(tech_stack) if tech_stack else 'General'}
- Company: {company}

Return ONLY this JSON (no markdown, no extra text):
{{
    "technical": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}},
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}}
    ],
    "behavioral": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}},
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}}
    ],
    "coding": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}},
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}}
    ]
}}"""
        
        if not PlacementAIFix:
            logger.error("PlacementAIFix not available, using fallback")
            return self._get_fallback_questions(num_questions)
        
        response_text = PlacementAIFix.call_openai(
            prompt,
            system_prompt="You are an expert technical interviewer. Return ONLY valid JSON.",
            temperature=0.7,
            max_tokens=2000
        )
        
        if not response_text:
            logger.error("OpenAI returned empty response")
            return self._get_fallback_questions(num_questions)
        
        # Extract and parse JSON
        result = PlacementAIFix.extract_json_from_text(response_text)
        
        if result and isinstance(result, dict):
            # Validate structure
            if all(k in result for k in ['technical', 'behavioral', 'coding']):
                logger.info("✅ Successfully generated questions with OpenAI")
                return result
        
        logger.error("Invalid JSON structure received from OpenAI")
        return self._get_fallback_questions(num_questions)
    
    def _generate_with_gemini(self, company, profile_data, role, num_questions):
        """Generate questions using Google Gemini API with proper error handling."""
        logger.info(f"🔵 Generating {num_questions} questions for {role} at {company} via Gemini")
        
        tech_stack = self.COMPANY_TECH_STACKS.get(company, [])
        user_skills = profile_data.get('technical_skills', {})
        experience = profile_data.get('experience_level', 'mid')
        
        prompt = f"""Generate exactly {num_questions} interview questions for a {role} position at {company}.

User Background:
- Experience Level: {experience}
- Technical Skills: {json.dumps(user_skills)}

Company Tech Stack: {', '.join(tech_stack) if tech_stack else 'General'}

Return ONLY this JSON (no markdown, no extra text):
{{
    "technical": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}},
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}}
    ],
    "behavioral": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}},
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}}
    ],
    "coding": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}},
        {{"question": "...", "difficulty": 1-5, "keywords": ["keyword1", "keyword2"]}}
    ]
}}"""
        
        if not PlacementAIFix:
            logger.error("PlacementAIFix not available, using fallback")
            return self._get_fallback_questions(num_questions)
        
        response_text = PlacementAIFix.call_gemini(
            prompt,
            system_prompt="You are an expert technical interviewer. Return ONLY valid JSON."
        )
        
        if not response_text:
            logger.error("Gemini returned empty response")
            return self._get_fallback_questions(num_questions)
        
        # Extract and parse JSON
        result = PlacementAIFix.extract_json_from_text(response_text)
        
        if result and isinstance(result, dict):
            # Validate structure
            if all(k in result for k in ['technical', 'behavioral', 'coding']):
                logger.info("✅ Successfully generated questions with Gemini")
                return result
        
        logger.error("Invalid JSON structure received from Gemini")
        return self._get_fallback_questions(num_questions)
    
    def _get_fallback_questions(self, num_questions):
        """Use fallback questions when LLM fails."""
        logger.warning(f"🔄 Using {num_questions} fallback questions")
        
        # Distribute questions among three types
        total_tech = max(1, num_questions // 3)
        total_behavioral = max(1, num_questions // 3)
        total_coding = num_questions - total_tech - total_behavioral
        
        logger.debug(f"Fallback distribution: tech={total_tech}, behavioral={total_behavioral}, coding={total_coding}")
        
        result = {
            'technical': [
                {
                    'question': q, 
                    'difficulty': random.randint(2, 4), 
                    'keywords': ['key', 'concept']
                }
                for q in random.sample(
                    self.FALLBACK_QUESTIONS['technical'], 
                    min(total_tech, len(self.FALLBACK_QUESTIONS['technical']))
                )
            ],
            'behavioral': [
                {
                    'question': q, 
                    'difficulty': random.randint(2, 4), 
                    'keywords': ['experience', 'skill']
                }
                for q in random.sample(
                    self.FALLBACK_QUESTIONS['behavioral'], 
                    min(total_behavioral, len(self.FALLBACK_QUESTIONS['behavioral']))
                )
            ],
            'coding': [
                {
                    'question': q, 
                    'difficulty': random.randint(2, 4), 
                    'keywords': ['algorithm', 'code']
                }
                for q in random.sample(
                    self.FALLBACK_QUESTIONS['coding'], 
                    min(total_coding, len(self.FALLBACK_QUESTIONS['coding']))
                )
            ]
        }
        
        logger.info(f"✅ Returned {len(result['technical'])} tech, {len(result['behavioral'])} behavioral, {len(result['coding'])} coding fallback questions")
        return result
    
    def get_company_tech_stack(self, company):
        """Get known tech stack for a company."""
        return self.COMPANY_TECH_STACKS.get(company, [])
    
    def refine_question(self, question, difficulty_level):
        """
        Refine a question to specific difficulty level.
        
        Args:
            question (str): Original question
            difficulty_level (int): 1-5 difficulty level
            
        Returns:
            str: Refined question
        """
        prompts = {
            1: f"Make this question simpler for a beginner: {question}",
            2: f"Make this question moderately easy: {question}",
            3: f"Keep this question at medium difficulty: {question}",
            4: f"Make this question harder: {question}",
            5: f"Make this question very challenging for an expert: {question}"
        }
        
        prompt = prompts.get(difficulty_level, prompts[3])
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert interviewer refining interview questions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to refine question: {e}")
            return question


def generate_interview_questions(company, profile_data, role='Software Engineer'):
    """
    Utility function to generate questions.
    
    Args:
        company (str): Company name
        profile_data (dict): User profile/resume analysis
        role (str): Job role
        
    Returns:
        dict: Generated questions
    """
    engine = QuestionEngine()
    return engine.generate_questions(company, profile_data, role, num_questions=10)
