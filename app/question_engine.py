"""
Question Engine Module

Generates company-specific interview questions based on resume analysis,
company tech stack, and company interview patterns.
"""

import json
import logging
import os
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
        questions = {
            'technical': [],
            'behavioral': [],
            'coding': []
        }
        
        try:
            # Try using OpenAI first
            questions = self._generate_with_openai(company, profile_data, role, num_questions)
        except Exception as e:
            logger.warning(f"OpenAI generation failed: {e}, attempting Gemini fallback")
            try:
                # Fallback to Gemini
                questions = self._generate_with_gemini(company, profile_data, role, num_questions)
            except Exception as e2:
                logger.error(f"Both LLM apis failed: {e2}, using fallback questions")
                # Use fallback questions
                questions = self._get_fallback_questions(num_questions)
        
        return questions
    
    def _generate_with_openai(self, company, profile_data, role, num_questions):
        """Generate questions using OpenAI API."""
        tech_stack = self.COMPANY_TECH_STACKS.get(company, [])
        user_skills = profile_data.get('technical_skills', {})
        
        prompt = f"""Generate {num_questions} interview questions for a {role} position at {company}.

User Background:
- Experience Level: {profile_data.get('experience_level', 'mid')}
- Technical Skills: {json.dumps(user_skills)}
- Projects: {', '.join(profile_data.get('projects', [])[:3])}

Company Info:
- Tech Stack: {', '.join(tech_stack)}
- Company: {company}

Generate questions in this exact JSON format:
{{
    "technical": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["...", "..."]}},
        ...
    ],
    "behavioral": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["...", "..."]}},
        ...
    ],
    "coding": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["...", "..."]}},
        ...
    ]
}}

Make sure:
- Questions are company/role specific
- Difficulty matches user's experience level
- Include relevant keywords for evaluation
- Total questions across all types = {num_questions}
"""
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical interviewer generating interview questions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )
        
        try:
            content = response.choices[0].message.content
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.error(f"Failed to parse OpenAI response: {e}")
        
        return {'technical': [], 'behavioral': [], 'coding': []}
    
    def _generate_with_gemini(self, company, profile_data, role, num_questions):
        """Generate questions using Google Gemini API."""
        tech_stack = self.COMPANY_TECH_STACKS.get(company, [])
        user_skills = profile_data.get('technical_skills', {})
        
        prompt = f"""Generate {num_questions} interview questions for a {role} position at {company}.

User Background:
- Experience Level: {profile_data.get('experience_level', 'mid')}
- Technical Skills: {json.dumps(user_skills)}

Company Tech Stack: {', '.join(tech_stack)}

Generate questions in this JSON format:
{{
    "technical": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["...", "..."]}},
    ],
    "behavioral": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["...", "..."]}},
    ],
    "coding": [
        {{"question": "...", "difficulty": 1-5, "keywords": ["...", "..."]}},
    ]
}}

Focus on {company}-specific patterns and {role} role requirements."""
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        try:
            content = response.text
            # Extract JSON
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.error(f"Failed to parse Gemini response: {e}")
        
        return {'technical': [], 'behavioral': [], 'coding': []}
    
    def _get_fallback_questions(self, num_questions):
        """Use fallback questions when LLM fails."""
        import random
        
        total_tech = max(1, num_questions // 3)
        total_behavioral = max(1, num_questions // 3)
        total_coding = num_questions - total_tech - total_behavioral
        
        return {
            'technical': [
                {'question': q, 'difficulty': random.randint(1, 5), 'keywords': []}
                for q in random.sample(self.FALLBACK_QUESTIONS['technical'], min(total_tech, 5))
            ],
            'behavioral': [
                {'question': q, 'difficulty': random.randint(1, 5), 'keywords': []}
                for q in random.sample(self.FALLBACK_QUESTIONS['behavioral'], min(total_behavioral, 5))
            ],
            'coding': [
                {'question': q, 'difficulty': random.randint(1, 5), 'keywords': []}
                for q in random.sample(self.FALLBACK_QUESTIONS['coding'], min(total_coding, 5))
            ]
        }
    
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
