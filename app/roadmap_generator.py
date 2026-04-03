"""
Roadmap Generator Module

Generates personalized interview preparation roadmaps based on user's skills,
weak areas, and target company requirements.
"""

import json
import logging
import os
from openai import OpenAI
import google.generativeai as genai
from datetime import datetime, timedelta

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



class RoadmapGenerator:
    """Generate personalized interview preparation roadmaps."""
    
    # Common learning resources
    RESOURCES_DB = {
        'Python': ['LeetCode Python Problems', 'GeeksforGeeks Python', 'Real Python Tutorials'],
        'Java': ['LeetCode Java Problems', 'Oracle Java Docs', 'Baeldung Java Tutorials'],
        'JavaScript': ['JavaScript.info', 'MDN Web Docs', 'LeetCode JS Problems'],
        'Data Structures': ['Visualgo.net', 'Data Structures & Algorithms Course', 'LeetCode'],
        'System Design': ['System Design Primer', 'Grokking System Design', 'YouTube Channels'],
        'SQL': ['SQLZoo', 'LeetCode SQL', 'Mode Analytics SQL Tutorial'],
        'Databases': ['PostgreSQL Docs', 'MongoDB University', 'Redis Documentation'],
        'APIs': ['REST API Best Practices', 'GraphQL Official Docs', 'API Design Patterns'],
        'Cloud': ['AWS Tutorials', 'Google Cloud Essentials', 'Azure Learning Paths'],
        'DevOps': ['Docker Documentation', 'Kubernetes Official Docs', 'CI/CD Best Practices'],
        'Behavioral': ['Behavioral Preparation Guide', 'STAR Method', 'Mock Interview Videos'],
    }
    
    def __init__(self):
        """Initialize roadmap generator."""
        pass
    
    def generate_roadmap(self, profile_data, performance_data=None, days=21):
        """
        Generate a personalized interview prep roadmap.
        
        Args:
            profile_data (dict): User's resume analysis
            performance_data (dict): Performance from previous sessions (optional)
            days (int): Number of days for roadmap (default 21 = 3 weeks)
            
        Returns:
            dict: Roadmap with daily study plan
        """
        # Identify weak areas
        weak_areas = self._identify_weak_areas(profile_data, performance_data)
        
        # Generate study topics
        topics = self._generate_topics(profile_data, weak_areas)
        
        # Create daily plan
        daily_plan = self._create_daily_plan(topics, days)
        
        # Recommend resources
        resources = self._recommend_resources(topics)
        
        # Create milestones
        milestones = self._create_milestones(days)
        
        return {
            'weak_areas': weak_areas,
            'duration_days': days,
            'topics': topics,
            'daily_plan': daily_plan,
            'resources': resources,
            'milestones': milestones,
            'generated_at': datetime.now().isoformat()
        }
    
    def _identify_weak_areas(self, profile_data, performance_data):
        """Identify areas where user needs improvement."""
        weak_areas = []
        
        # From resume analysis
        technical_skills = profile_data.get('technical_skills', {})
        experience_level = profile_data.get('experience_level', 'junior')
        
        # Check for missing common skills based on experience level
        essential_skills = {
            'fresher': ['Data Structures', 'Algorithms', 'System Design Basics'],
            'junior': ['System Design', 'SQL', 'APIs'],
            'mid': ['System Design Advanced', 'Distributed Systems', 'Performance Optimization'],
            'senior': ['Architecture Patterns', 'Trade-offs Analysis', 'Team Leadership']
        }
        
        for skill in essential_skills.get(experience_level, []):
            skill_lower = skill.lower()
            found = any(skill_lower in str(v).lower() for v in technical_skills.values())
            if not found:
                weak_areas.append(skill)
        
        # From performance data if available
        if performance_data:
            evaluations = performance_data.get('evaluations', [])
            if evaluations:
                # Find consistently low scores
                low_score_topics = []
                for eval in evaluations:
                    if eval.get('overall_score', 10) < 5:
                        topics_mentioned = eval.get('weaknesses', [])
                        low_score_topics.extend(topics_mentioned)
                
                # Add most common weak topics
                from collections import Counter
                if low_score_topics:
                    most_common = Counter(low_score_topics).most_common(2)
                    weak_areas.extend([topic for topic, _ in most_common])
        
        return weak_areas[:5]  # Top 5 weak areas
    
    def _generate_topics(self, profile_data, weak_areas):
        """Generate comprehensive list of study topics."""
        topics = []
        
        # Core topics everyone should cover
        core_topics = [
            'Data Structures & Algorithms',
            'System Design Basics',
            'Database Design',
            'API Design',
            'Behavioral Preparation'
        ]
        
        topics.extend(core_topics)
        topics.extend(weak_areas)
        
        # Add company-specific topics based on tech stack
        # This could be enhanced with company parameter
        
        return list(set(topics))[:15]  # Top 15 unique topics
    
    def _create_daily_plan(self, topics, days):
        """Create a day-by-day study plan."""
        daily_plan = []
        topics_per_day = 1 if len(topics) <= days else max(1, len(topics) // (days // 2))
        
        day = 1
        topic_index = 0
        
        while day <= days and topic_index < len(topics):
            topic = topics[topic_index]
            
            # Alternate between learning and practice
            if day % 2 == 1:
                activity = 'Learning'
                duration = '2-3 hours'
                description = f'Study {topic}'
            else:
                activity = 'Practice'
                duration = '2-3 hours'
                description = f'Practice problems on {topic}'
            
            daily_plan.append({
                'day': day,
                'topic': topic,
                'activity': activity,
                'duration': duration,
                'description': description,
                'tasks': self._get_daily_tasks(topic, activity)
            })
            
            day += 1
            if day % 2 == 1:  # Move to next topic every 2 days
                topic_index += 1
        
        # Fill remaining days with review
        while day <= days:
            daily_plan.append({
                'day': day,
                'topic': 'Review & Mock Interview',
                'activity': 'Revision',
                'duration': '3-4 hours',
                'description': 'Review weak areas and attempt mock interview',
                'tasks': ['Review notes', 'Solve quick problems', 'Attempt mock test']
            })
            day += 1
        
        return daily_plan
    
    def _get_daily_tasks(self, topic, activity):
        """Generate specific tasks for a day."""
        task_templates = {
            'Learning': [
                f'Read about {topic}',
                f'Watch tutorial on {topic}',
                f'Take detailed notes',
                'Create summary doc'
            ],
            'Practice': [
                f'Solve 3-5 {topic} problems',
                f'Write solution explanations',
                'Analyze time complexity',
                'Review solutions'
            ],
            'Revision': [
                'Review notes from past week',
                'Solve mixed problems',
                'Identify patterns',
                'Plan next week'
            ]
        }
        
        return task_templates.get(activity, ['Study', 'Practice', 'Review'])
    
    def _recommend_resources(self, topics):
        """Recommend learning resources for topics."""
        resources = {}
        
        for topic in topics:
            # Try exact match first
            if topic in self.RESOURCES_DB:
                resources[topic] = self.RESOURCES_DB[topic]
            else:
                # Try partial match
                for key, value in self.RESOURCES_DB.items():
                    if key.lower() in topic.lower() or topic.lower() in key.lower():
                        resources[topic] = value
                        break
                else:
                    # Default resources
                    resources[topic] = [
                        'LeetCode',
                        'GeeksforGeeks',
                        'YouTube Tutorials',
                        'Official Documentation'
                    ]
        
        return resources
    
    def _create_milestones(self, days):
        """Create progress milestones."""
        milestones = []
        
        milestones.append({
            'day': 1,
            'milestone': 'Start Interview Prep',
            'target': 'Complete Day 1 study session'
        })
        
        mid_day = days // 2
        milestones.append({
            'day': mid_day,
            'milestone': 'Halfway Point',
            'target': 'Attempt mock interview, assess progress'
        })
        
        milestones.append({
            'day': days,
            'milestone': 'Prep Complete',
            'target': 'Final review and confidence building'
        })
        
        return milestones
    
    def optimize_for_company(self, roadmap, company, company_tech_stack):
        """
        Optimize roadmap for specific company.
        
        Args:
            roadmap (dict): Base roadmap
            company (str): Company name
            company_tech_stack (list): Company's tech stack
            
        Returns:
            dict: Company-optimized roadmap
        """
        # Prioritize company-relevant topics
        tech_topics = [tech for tech in company_tech_stack if tech in roadmap.get('topics', [])]
        
        if tech_topics:
            roadmap['company_focus'] = tech_topics
            roadmap['company'] = company
        
        return roadmap
    
    def calculate_study_hours(self, roadmap):
        """Calculate total study hours needed."""
        daily_hours = 4  # Average 4 hours per day
        total_days = roadmap.get('duration_days', 21)
        total_hours = daily_hours * total_days
        
        return {
            'daily_hours': daily_hours,
            'total_hours': total_hours,
            'weeks': total_days // 7
        }


def generate_preparation_roadmap(profile_data, performance_data=None, days=21):
    """
    Utility function to generate roadmap.
    
    Args:
        profile_data (dict): User's resume analysis
        performance_data (dict): Previous performance data
        days (int): Number of days for roadmap
        
    Returns:
        dict: Generated roadmap
    """
    generator = RoadmapGenerator()
    return generator.generate_roadmap(profile_data, performance_data, days)


def optimize_roadmap_for_company(roadmap, company, tech_stack):
    """
    Optimize roadmap for specific company.
    
    Args:
        roadmap (dict): Base roadmap
        company (str): Company name
        tech_stack (list): Company's tech stack
        
    Returns:
        dict: Optimized roadmap
    """
    generator = RoadmapGenerator()
    return generator.optimize_for_company(roadmap, company, tech_stack)
