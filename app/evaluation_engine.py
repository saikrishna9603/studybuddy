"""
Evaluation Engine Module

AI-powered evaluation system that scores interview answers and provides
detailed feedback on correctness, clarity, depth, and communication.

FIXED: Added comprehensive logging and error handling
"""

import json
import logging
import os
import re

logger = logging.getLogger(__name__)

# Import the placement AI fix module for proper LLM handling
try:
    from .placement_ai_fix import PlacementAIFix
    logger.info("✅ Imported PlacementAIFix module for evaluation")
except ImportError:
    logger.error("❌ Failed to import PlacementAIFix")
    PlacementAIFix = None



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
        logger.info(f"🚀 Starting answer evaluation for {question_type} question")
        logger.debug(f"Question: {question[:100]}...")
        logger.debug(f"Answer length: {len(user_answer) if user_answer else 0} chars")
        
        if not user_answer or not user_answer.strip():
            logger.warning("⚠️ Empty answer provided, returning empty evaluation")
            return self._get_empty_evaluation("Answer cannot be empty")
        
        try:
            # Try OpenAI first
            logger.info("📍 Attempting evaluation with OpenAI")
            evaluation = self._evaluate_with_openai(
                question, user_answer, question_type, expected_keywords
            )
            if evaluation and 'scores' in evaluation:
                logger.info("✅ Successfully evaluated with OpenAI")
                return evaluation
            else:
                logger.warning("⚠️ OpenAI returned invalid evaluation, trying Gemini")
        except Exception as e:
            logger.warning(f"❌ OpenAI evaluation failed: {e}, trying Gemini fallback")
            
        try:
            # Fallback to Gemini
            logger.info("📍 Attempting evaluation with Gemini (fallback)")
            evaluation = self._evaluate_with_gemini(
                question, user_answer, question_type, expected_keywords
            )
            if evaluation and 'scores' in evaluation:
                logger.info("✅ Successfully evaluated with Gemini (fallback)")
                return evaluation
            else:
                logger.warning("⚠️ Gemini also returned invalid evaluation, using fallback")
        except Exception as e2:
            logger.error(f"❌ Gemini evaluation also failed: {e2}, using fallback")
        
        logger.warning("⚠️ Using fallback evaluation")
        return self._get_fallback_evaluation(user_answer)
    
    def _evaluate_with_openai(self, question, user_answer, question_type, expected_keywords):
        """Evacuate answer using OpenAI with proper error handling."""
        logger.info(f"🔵 Calling OpenAI for {question_type} answer evaluation")
        
        keywords_text = ""
        if expected_keywords:
            keywords_text = f"\n\nExpected keywords/concepts: {', '.join(str(k) for k in expected_keywords)}"
        
        prompt = f"""Evaluate this interview answer and respond with ONLY valid JSON (no markdown).

QUESTION: {question}
TYPE: {question_type}
{keywords_text}

ANSWER:
{user_answer}

Rate on 4 dimensions (0-10 each): correctness, clarity, depth, communication.

Return only this JSON:
{{
    "scores": {{"correctness": 7, "clarity": 8, "depth": 6, "communication": 7}},
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["area1", "area2"],
    "model_answer": "Ideal answer...",
    "tips": ["tip1", "tip2"]
}}"""
        
        if not PlacementAIFix:
            logger.error("PlacementAIFix not available, using fallback")
            return self._get_fallback_evaluation(user_answer)
        
        response_text = PlacementAIFix.call_openai(
            prompt,
            system_prompt="You are an expert technical interviewer. Respond with only valid JSON.",
            temperature=0.3,
            max_tokens=1000
        )
        
        if not response_text:
            logger.error("OpenAI returned empty response")
            return self._get_fallback_evaluation(user_answer)
        
        # Extract and parse JSON
        result = PlacementAIFix.extract_json_from_text(response_text)
        
        if result and isinstance(result, dict):
            logger.info("✅ Successfully parsed OpenAI evaluation JSON")
            return self._validate_evaluation(result)
        
        logger.error("Failed to parse OpenAI response as JSON")
        return self._get_fallback_evaluation(user_answer)
    
    def _evaluate_with_gemini(self, question, user_answer, question_type, expected_keywords):
        """Evaluate answer using Google Gemini with proper error handling."""
        logger.info(f"🔵 Calling Gemini for {question_type} answer evaluation")
        
        keywords_text = ""
        if expected_keywords:
            keywords_text = f"\n\nExpected keywords: {', '.join(str(k) for k in expected_keywords)}"
        
        prompt = f"""Evaluate this interview answer and respond with ONLY valid JSON (no markdown).

QUESTION: {question}
TYPE: {question_type}
{keywords_text}

ANSWER:
{user_answer}

Rate on 4 dimensions (0-10 each): correctness, clarity, depth, communication.

Return only this JSON:
{{
    "scores": {{"correctness": 7, "clarity": 8, "depth": 6, "communication": 7}},
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["area1", "area2"],
    "model_answer": "Ideal answer...",
    "tips": ["tip1", "tip2"]
}}"""
        
        if not PlacementAIFix:
            logger.error("PlacementAIFix not available, using fallback")
            return self._get_fallback_evaluation(user_answer)
        
        response_text = PlacementAIFix.call_gemini(
            prompt,
            system_prompt="You are an expert technical interviewer. Respond with only valid JSON."
        )
        
        if not response_text:
            logger.error("Gemini returned empty response")
            return self._get_fallback_evaluation(user_answer)
        
        # Extract and parse JSON
        result = PlacementAIFix.extract_json_from_text(response_text)
        
        if result and isinstance(result, dict):
            logger.info("✅ Successfully parsed Gemini evaluation JSON")
            return self._validate_evaluation(result)
        
        logger.error("Failed to parse Gemini response as JSON")
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
