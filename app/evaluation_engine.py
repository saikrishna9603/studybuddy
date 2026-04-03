"""
Evaluation Engine Module

AI-powered evaluation system that scores interview answers and provides
detailed feedback on correctness, clarity, depth, and communication.
"""

import json
import logging
import os
import re
from openai import OpenAI
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Initialize LLM clients - handle missing keys gracefully
try:
    openai_client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'))
except Exception as e:
    logger.warning(f"OpenAI client initialization warning: {e}")
    openai_client = None

# Configure Gemini
try:
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    logger.warning(f"Gemini configuration warning: {e}")



class EvaluationEngine:
    """Evaluate interview answers using AI models."""
    
    def __init__(self):
        """Initialize evaluation engine."""
        pass
    
    def evaluate_answer(self, question, user_answer, question_type='technical', 
                       expected_keywords=None):
        """
        Evaluate a user's answer to an interview question.
        
        Args:
            question (str): The interview question
            user_answer (str): The user's answer
            question_type (str): Type of question (technical, behavioral, coding)
            expected_keywords (list): Expected keywords for the answer
            
        Returns:
            dict: Evaluation results with scores, feedback, and tips
        """
        if not user_answer or not user_answer.strip():
            return self._get_empty_evaluation("Answer cannot be empty")
        
        try:
            # Try OpenAI first
            evaluation = self._evaluate_with_openai(
                question, user_answer, question_type, expected_keywords
            )
        except Exception as e:
            logger.warning(f"OpenAI evaluation failed: {e}, trying Gemini")
            try:
                # Fallback to Gemini
                evaluation = self._evaluate_with_gemini(
                    question, user_answer, question_type, expected_keywords
                )
            except Exception as e2:
                logger.error(f"Both LLM evaluations failed: {e2}, using fallback")
                evaluation = self._get_fallback_evaluation(user_answer)
        
        return evaluation
    
    def _evaluate_with_openai(self, question, user_answer, question_type, expected_keywords):
        """Evaluate answer using OpenAI."""
        keywords_text = ""
        if expected_keywords:
            keywords_text = f"\n\nExpected keywords/concepts: {', '.join(expected_keywords)}"
        
        prompt = f"""Evaluate this interview answer thoroughly and provide scores and feedback.

QUESTION: {question}

QUESTION TYPE: {question_type}
{keywords_text}

CANDIDATE'S ANSWER:
{user_answer}

Evaluate on these 4 dimensions (rate 0-10 for each):
1. Correctness: Is the answer technically accurate?
2. Clarity: How well is the answer explained?
3. Depth: Does it show deep understanding and reasoning?
4. Communication: Is it articulate and professional?

Provide response in this exact JSON format:
{{
    "scores": {{
        "correctness": 7,
        "clarity": 8,
        "depth": 6,
        "communication": 7
    }},
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["area1", "area2"],
    "model_answer": "An ideal answer would cover...",
    "tips": ["tip1", "tip2"]
}}

Be fair but critical. Focus on content quality not just form."""
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert interviewer evaluating candidate responses."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3  # Lower temp for consistent grading
        )
        
        try:
            content = response.choices[0].message.content
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                evaluation = json.loads(json_match.group())
                return self._validate_evaluation(evaluation)
        except Exception as e:
            logger.error(f"Failed to parse OpenAI evaluation: {e}")
        
        return self._get_fallback_evaluation(user_answer)
    
    def _evaluate_with_gemini(self, question, user_answer, question_type, expected_keywords):
        """Evaluate answer using Google Gemini."""
        keywords_text = ""
        if expected_keywords:
            keywords_text = f"\n\nExpected keywords: {', '.join(expected_keywords)}"
        
        prompt = f"""Evaluate this {question_type} interview answer on 4 dimensions (0-10 each):
1. Correctness - Technical accuracy
2. Clarity - How well explained
3. Depth - Level of understanding shown
4. Communication - Articulate and professional

Question: {question}
{keywords_text}

Answer: {user_answer}

Return JSON response with scores, strengths, weaknesses, model answer, and tips."""
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        try:
            content = response.text
            # Extract JSON
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                evaluation = json.loads(json_match.group())
                return self._validate_evaluation(evaluation)
        except Exception as e:
            logger.error(f"Failed to parse Gemini evaluation: {e}")
        
        return self._get_fallback_evaluation(user_answer)
    
    def _validate_evaluation(self, evaluation):
        """Ensure evaluation has all required fields and valid scores."""
        # Ensure scores are within 0-10
        scores = evaluation.get('scores', {})
        scores['correctness'] = max(0, min(10, float(scores.get('correctness', 5))))
        scores['clarity'] = max(0, min(10, float(scores.get('clarity', 5))))
        scores['depth'] = max(0, min(10, float(scores.get('depth', 5))))
        scores['communication'] = max(0, min(10, float(scores.get('communication', 5))))
        
        # Calculate overall score
        overall = (
            scores['correctness'] + scores['clarity'] + 
            scores['depth'] + scores['communication']
        ) / 4.0
        
        return {
            'scores': scores,
            'overall_score': round(overall, 1),
            'strengths': evaluation.get('strengths', []),
            'weaknesses': evaluation.get('weaknesses', []),
            'model_answer': evaluation.get('model_answer', ''),
            'tips': evaluation.get('tips', [])
        }
    
    def _get_empty_evaluation(self, message):
        """Return empty evaluation with error message."""
        return {
            'scores': {
                'correctness': 0,
                'clarity': 0,
                'depth': 0,
                'communication': 0
            },
            'overall_score': 0,
            'strengths': [],
            'weaknesses': [message],
            'model_answer': 'Please provide a valid answer to be evaluated.',
            'tips': ['Try to answer the question completely.']
        }
    
    def _get_fallback_evaluation(self, user_answer):
        """Return reasonable fallback evaluation based on answer length."""
        word_count = len(user_answer.split())
        
        # Rough scoring based on answer completeness
        if word_count < 20:
            score = 3
        elif word_count < 50:
            score = 5
        elif word_count < 150:
            score = 7
        else:
            score = 8
        
        return {
            'scores': {
                'correctness': score,
                'clarity': score + 1,
                'depth': score - 1,
                'communication': score
            },
            'overall_score': round(score, 1),
            'strengths': ['You provided a response', 'Answer was comprehensible'],
            'weaknesses': ['Consider adding more depth', 'Could be more detailed'],
            'model_answer': 'An ideal answer would thoroughly address all aspects of the question.',
            'tips': ['Practice similar questions', 'Study the topic more deeply', 'Work on articulation']
        }
    
    def compare_answers(self, model_answer, user_answer):
        """
        Compare a model answer with user answer to identify gaps.
        
        Args:
            model_answer (str): The ideal answer
            user_answer (str): The user's answer
            
        Returns:
            dict: Comparison analysis
        """
        model_words = set(model_answer.lower().split())
        user_words = set(user_answer.lower().split())
        
        # Calculate coverage
        coverage = len(user_words & model_words) / len(model_words) if model_words else 0
        
        return {
            'coverage_percentage': int(coverage * 100),
            'missing_concepts': list(model_words - user_words)[:10],
            'extra_concepts': list(user_words - model_words)[:5]
        }
    
    def score_consistency(self, session_evaluations):
        """
        Analyze consistency of performance across multiple answers.
        
        Args:
            session_evaluations (list): List of evaluation results from a session
            
        Returns:
            dict: Consistency metrics
        """
        if not session_evaluations:
            return {'average_score': 0, 'consistency': 'N/A', 'trend': 'N/A'}
        
        scores = [e.get('overall_score', 0) for e in session_evaluations]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate variance
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores) if len(scores) > 1 else 0
        
        # Determine consistency
        if variance < 1:
            consistency = 'Very Consistent'
        elif variance < 3:
            consistency = 'Consistent'
        elif variance < 7:
            consistency = 'Variable'
        else:
            consistency = 'Highly Variable'
        
        # Determine trend
        if len(scores) >= 2:
            if scores[-1] > scores[0]:
                trend = 'Improving'
            elif scores[-1] < scores[0]:
                trend = 'Declining'
            else:
                trend = 'Stable'
        else:
            trend = 'N/A'
        
        return {
            'average_score': round(avg_score, 1),
            'consistency': consistency,
            'trend': trend,
            'num_answers': len(session_evaluations)
        }


def evaluate_interview_answer(question, answer, question_type='technical', expected_keywords=None):
    """
    Utility function to evaluate an answer.
    
    Args:
        question (str): Interview question
        answer (str): User's answer
        question_type (str): Type of question
        expected_keywords (list): Expected keywords
        
    Returns:
        dict: Evaluation results
    """
    engine = EvaluationEngine()
    return engine.evaluate_answer(question, answer, question_type, expected_keywords)
