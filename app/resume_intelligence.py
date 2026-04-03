"""
Resume Intelligence Module

Extracts technical skills, soft skills, projects, experience level, and predicted roles
from user resumes to support the AI Placement Preparation Assistant.
"""

import re
import json
import logging

logger = logging.getLogger(__name__)


class ResumeIntelligence:
    """Extract and analyze resume data for interview preparation."""
    
    # Common technical skills database
    TECH_KEYWORDS = {
        'Languages': ['Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 
                     'Rust', 'SQL', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'R', 'MATLAB'],
        'Frameworks': ['React', 'Angular', 'Vue.js', 'Django', 'Flask', 'FastAPI',
                      'Spring', 'Spring Boot', 'Node.js', 'Express', '.NET', 'Laravel'],
        'Databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'DynamoDB', 'Oracle',
                     'SQLite', 'Elasticsearch', 'Cassandra', 'Firebase'],
        'Cloud': ['AWS', 'GCP', 'Azure', 'Heroku', 'DigitalOcean', 'Kubernetes', 'Docker'],
        'Tools': ['Git', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'AWS', 'GCP',
                 'Linux', 'Unix', 'Jira', 'Slack']
    }
    
    # Common soft skills
    SOFT_SKILLS = [
        'Leadership', 'Communication', 'Teamwork', 'Problem-solving', 'Critical thinking',
        'Project Management', 'Mentoring', 'Presentation', 'Collaboration', 'Adaptability',
        'Time Management', 'Analytical', 'Negotiation', 'Decision making'
    ]
    
    # Job roles that might be suitable
    JOB_ROLES = [
        'Software Engineer', 'Full Stack Developer', 'Backend Developer', 'Frontend Developer',
        'DevOps Engineer', 'Data Engineer', 'Machine Learning Engineer', 'Cloud Architect',
        'Database Administrator', 'Systems Engineer', 'Solutions Architect', 'Technical Lead'
    ]
    
    def __init__(self):
        """Initialize resume intelligence analyzer."""
        pass
    
    def analyze_resume(self, resume_text):
        """
        Analyze resume and extract key information.
        
        Args:
            resume_text (str): The full text content of the resume
            
        Returns:
            dict: Contains technical_skills, soft_skills, projects, experience_level, predicted_roles, profile_score
        """
        if not resume_text:
            return self._get_empty_analysis()
        
        return {
            'technical_skills': self.extract_technical_skills(resume_text),
            'soft_skills': self.extract_soft_skills(resume_text),
            'projects': self.extract_projects(resume_text),
            'experience_level': self.classify_experience_level(resume_text),
            'predicted_roles': self.predict_suitable_roles(resume_text),
            'profile_score': self.score_resume(resume_text),
        }
    
    def extract_technical_skills(self, resume_text):
        """
        Extract technical skills from resume text.
        
        Args:
            resume_text (str): Resume content
            
        Returns:
            dict: Skills organized by category
        """
        found_skills = {}
        text_lower = resume_text.lower()
        
        for category, skills in self.TECH_KEYWORDS.items():
            category_skills = []
            for skill in skills:
                if skill.lower() in text_lower:
                    category_skills.append(skill)
            
            if category_skills:
                found_skills[category] = category_skills
        
        return found_skills
    
    def extract_soft_skills(self, resume_text):
        """
        Extract soft skills from resume text.
        
        Args:
            resume_text (str): Resume content
            
        Returns:
            list: Soft skills found in resume
        """
        found_skills = []
        text_lower = resume_text.lower()
        
        for skill in self.SOFT_SKILLS:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def extract_projects(self, resume_text):
        """
        Extract project descriptions from resume.
        
        Args:
            resume_text (str): Resume content
            
        Returns:
            list: Project titles/descriptions (top 5)
        """
        # Look for project sections
        project_patterns = [
            r'(?:Project|Projects|Experience|Professional Experience)[\s\n]+([^\n]+)',
            r'(?:Built|Developed|Created)[\s]+([^\.]+[\.])',
            r'(?:Project:?\s*)([^\n]+)',
        ]
        
        projects = []
        for pattern in project_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            projects.extend(matches)
        
        # Clean and deduplicate
        cleaned = list(set([p.strip() for p in projects if p.strip() and len(p) > 10]))
        return cleaned[:5]  # Return top 5
    
    def classify_experience_level(self, resume_text):
        """
        Classify experience level based on resume content.
        
        Args:
            resume_text (str): Resume content
            
        Returns:
            str: One of 'fresher', 'junior', 'mid', 'senior'
        """
        text_lower = resume_text.lower()
        
        # Check for fresher/internship indicators
        if any(word in text_lower for word in ['fresher', 'internship', 'graduate', 'recent graduate']):
            return 'fresher'
        
        # Extract years of experience
        exp_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        matches = re.findall(exp_pattern, text_lower)
        
        if matches:
            years = max([int(m) for m in matches])
        else:
            # Try to count jobs as proxy for experience
            job_keywords = ['worked', 'employed', 'position', 'role']
            job_count = sum(text_lower.count(kw) for kw in job_keywords)
            years = max(0, job_count // 2)  # Rough estimate
        
        if years < 1:
            return 'fresher'
        elif years < 3:
            return 'junior'
        elif years < 7:
            return 'mid'
        else:
            return 'senior'
    
    def predict_suitable_roles(self, resume_text):
        """
        Predict suitable job roles based on skills and experience.
        
        Args:
            resume_text (str): Resume content
            
        Returns:
            list: Predicted job roles (top 3)
        """
        tech_skills = self.extract_technical_skills(resume_text)
        soft_skills = self.extract_soft_skills(resume_text)
        experience_level = self.classify_experience_level(resume_text)
        
        # Scoring logic for roles
        role_scores = {}
        
        for role in self.JOB_ROLES:
            score = 0
            role_lower = role.lower()
            
            # Check for role-specific keywords
            if 'backend' in role_lower and 'Languages' in tech_skills:
                score += 30
            elif 'frontend' in role_lower and any(fw in str(tech_skills) for fw in ['React', 'Angular', 'Vue']):
                score += 30
            elif 'devops' in role_lower and 'Cloud' in tech_skills:
                score += 30
            elif 'data' in role_lower and any(lang in str(tech_skills) for lang in ['Python', 'SQL', 'R']):
                score += 30
            elif 'machine learning' in role_lower and any(lang in str(tech_skills) for lang in ['Python', 'R']):
                score += 30
            elif 'architect' in role_lower and experience_level in ['mid', 'senior']:
                score += 30
            elif 'lead' in role_lower and experience_level in ['mid', 'senior']:
                score += 20
            
            # Add points for leadership skills
            if 'lead' in role_lower.lower() and 'Leadership' in soft_skills:
                score += 15
            
            # Add points for communication skills
            if 'Communication' in soft_skills:
                score += 10
            
            if score > 0:
                role_scores[role] = score
        
        # Return top 3 roles
        sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
        return [role for role, score in sorted_roles[:3]]
    
    def score_resume(self, resume_text):
        """
        Score overall resume quality from 0-100.
        
        Args:
            resume_text (str): Resume content
            
        Returns:
            int: Resume quality score 0-100
        """
        score = 0
        text_lower = resume_text.lower()
        
        # Formatting (20 points)
        if '\n' in resume_text and len(resume_text) > 500:
            score += 18
        else:
            score += 8
        
        # Technical skills depth (25 points)
        tech_skills = self.extract_technical_skills(resume_text)
        total_tech_skills = sum(len(v) for v in tech_skills.values()) if tech_skills else 0
        if total_tech_skills >= 8:
            score += 25
        elif total_tech_skills >= 5:
            score += 18
        elif total_tech_skills >= 3:
            score += 12
        else:
            score += 5
        
        # Project mentions (20 points)
        projects = self.extract_projects(resume_text)
        if len(projects) >= 4:
            score += 20
        elif len(projects) >= 2:
            score += 12
        else:
            score += 5
        
        # Soft skills (15 points)
        soft_skills = self.extract_soft_skills(resume_text)
        if len(soft_skills) >= 4:
            score += 15
        elif len(soft_skills) >= 2:
            score += 10
        else:
            score += 5
        
        # Completeness (20 points)
        contact_info = ['email', 'phone', 'linkedin']
        found_info = sum(1 for info in contact_info if info in text_lower)
        score += (found_info * 7)  # 7 points per contact info
        
        return min(score, 100)
    
    def _get_empty_analysis(self):
        """Return empty analysis template."""
        return {
            'technical_skills': {},
            'soft_skills': [],
            'projects': [],
            'experience_level': 'fresher',
            'predicted_roles': [],
            'profile_score': 0,
        }


def analyze_resume_data(resume_text):
    """
    Utility function to analyze resume.
    
    Args:
        resume_text (str): Full resume text
        
    Returns:
        dict: Analysis results
    """
    analyzer = ResumeIntelligence()
    return analyzer.analyze_resume(resume_text)


def extract_resume_profile(resume_text):
    """
    Extract just the profile information (skills, roles, level).
    
    Args:
        resume_text (str): Full resume text
        
    Returns:
        dict: Profile information
    """
    analyzer = ResumeIntelligence()
    analysis = analyzer.analyze_resume(resume_text)
    
    return {
        'experience_level': analysis['experience_level'],
        'technical_skills': analysis['technical_skills'],
        'soft_skills': analysis['soft_skills'],
        'predicted_roles': analysis['predicted_roles'],
        'score': analysis['profile_score'],
    }
