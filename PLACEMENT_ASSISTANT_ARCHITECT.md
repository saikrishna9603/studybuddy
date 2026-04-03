# AI Placement Preparation Assistant - Architecture & Implementation Guide

> **Status:** Production-ready design for StudyBuddy platform transformation  
> **Scope:** Building an AI-driven end-to-end interview preparation system  
> **Timeline:** Hackathon-ready (Phase 1: 3-4 days, Full: 2 weeks)

---

## 1. SYSTEM ARCHITECTURE

### 1.1 High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER ENTRY POINT                               │
├─────────────────────────────────────────────────────────────────┤
│ 1. Login → 2. Upload/Existing Resume                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Resume Intelligence   │
        │    Module             │
        └────────────┬───────────┘
                     │
        • Extract skills (tech + soft)
        • Identify projects
        • Classify profile (junior/mid/senior)
        • Score resume quality
                     │
                     ▼
        ┌────────────────────────┐
        │  Company Selector      │
        │    Dashboard           │
        └────────────┬───────────┘
                     │
        • List 1000+ companies
        • Filter by industry/role
        • Select target role
                     │
                     ▼
        ┌────────────────────────┐
        │  Question Generator    │
        │    (RAG + LLM)        │
        └────────────┬───────────┘
                     │
        • Retrieve company-specific Q&A from RAG
        • Generate tailored technical questions
        • Generate HR/behavioral questions
        • Generate coding challenges
                     │
                     ▼
        ┌────────────────────────┐
        │  Interview Practice    │
        │    Interface           │
        └────────────┬───────────┘
                     │
        • Present questions
        • Capture text answers (voice in Phase 2)
        • Real-time coach chatbot
                     │
                     ▼
        ┌────────────────────────┐
        │  AI Answer Evaluator   │
        │    (LLM Powered)       │
        └────────────┬───────────┘
                     │
        • Score: Correctness (0-10)
        • Score: Clarity (0-10)
        • Score: Depth (0-10)
        • Identify strengths
        • Identify weaknesses
        • Provide model answer
                     │
                     ▼
        ┌────────────────────────┐
        │  Personalized Roadmap  │
        │    Generator           │
        └────────────┬───────────┘
                     │
        • Identify gap analysis
        • Create daily study plan
        • Assign weak-topic videos
        • Recommend mock tests
                     │
                     ▼
        ┌────────────────────────┐
        │  Progress & Analytics  │
        │    Dashboard           │
        └────────────────────────┘
        
        • Track interview readiness score
        • Show improvement over time
        • Display company-wise preparation
```

### 1.2 New Modules to Create

| Module | Purpose | Key Components |
|--------|---------|-----------------|
| **placement_module** | Core placement logic | Resume analyzer, Question generator, Answer evaluator |
| **resume_intelligence** | Resume parsing & analysis | Extract skills, projects, classify profile |
| **question_engine** | Generate interview questions | RAG retrieval, LLM generation, caching |
| **evaluation_engine** | AI-powered answer scoring | Rubric-based scoring, feedback generation |
| **roadmap_generator** | Create personalized study plan | Gap analysis, topic recommendation |
| **company_database** | Store company profiles | Interview patterns, question bank |

### 1.3 Modified Existing Modules

| Module | Existing Feature | Modifications |
|--------|-----------------|----------------|
| **resume.py** | Resume Analyzer | Upgrade to extract skills, projects, experience level, profile classification |
| **rag_pipeline.py** | Knowledge Base | Add company-specific interview Q&A store, interview patterns |
| **routes.py** | API endpoints | Add new placement routes (see Section 2) |
| **db.py** | Database | Add new tables for placement workflow |
| **dashboard-chatbot.js** | Chatbot UI | Extend to act as interview coach |

---

## 2. BACKEND CHANGES (Flask)

### 2.1 New API Routes

#### **Resume Intelligence Routes**

```python
# Enhanced Resume Analysis
POST   /api/placement/resume/analyze
       Input: { resume_id, resume_file (optional re-upload) }
       Output: {
         skills: { technical: [...], soft: [...] },
         projects: [...],
         experience_level: "junior|mid|senior",
         profile_score: 0-100,
         resume_quality_feedback: "...",
         suggested_improvements: [...]
       }

GET    /api/placement/resume/profile
       Output: Current user's extracted profile data
```

#### **Company Selection Routes**

```python
GET    /api/placement/companies?search=&industry=&role=
       Output: {
         companies: [
           { id, name, industry, popular_roles, difficulty: 1-5 },
           ...
         ]
       }

POST   /api/placement/session/create
       Input: { company_id, role, difficulty_preference }
       Output: { session_id, interview_plan }
```

#### **Question Generation Routes**

```python
POST   /api/placement/questions/generate
       Input: { session_id, company_id, role, difficulty }
       Output: {
         session_id,
         questions: [
           {
             id, 
             type: "technical|hr|coding",
             question,
             difficulty: 1-5,
             expected_keywords: [...]
           },
           ...
         ]
       }

GET    /api/placement/questions/:session_id
       Output: List of questions for current session
```

#### **Answer Submission & Evaluation Routes**

```python
POST   /api/placement/answers/submit
       Input: { 
         session_id, 
         question_id, 
         answer_text,
         time_taken
       }
       Output: { submission_id, queued_for_evaluation: true }

GET    /api/placement/answers/:answer_id/evaluate
       Output: {
         score: {
           correctness: 0-10,
           clarity: 0-10,
           depth: 0-10,
           communication: 0-10,
           overall: 0-10
         },
         strengths: [...],
         weaknesses: [...],
         model_answer: "...",
         tips: [...]
       }

GET    /api/placement/session/:session_id/results
       Output: {
         session_summary: {...},
         all_answers_with_scores: [...],
         average_score: 0-10,
         improvement_areas: [...]
       }
```

#### **Roadmap & Progress Routes**

```python
POST   /api/placement/roadmap/generate
       Input: { user_id, company_id, target_date }
       Output: {
         roadmap_id,
         daily_plan: [...],
         weak_topics: [...],
         recommended_resources: [...],
         milestone_dates: [...]
       }

GET    /api/placement/roadmap/:roadmap_id
       Output: Current roadmap with progress tracking

PATCH  /api/placement/roadmap/:roadmap_id/update-progress
       Input: { task_id, status: "completed|in-progress|skipped" }
       Output: { updated_roadmap }

GET    /api/placement/progress/dashboard
       Output: {
         interview_readiness_score: 0-100,
         companies_targeted: [...],
         sessions_completed: N,
         average_score: 0-10,
         weak_topics: [...],
         next_steps: [...]
       }
```

#### **Coach Chatbot Route (Extension)**

```python
POST   /api/placement/coach/ask
       Input: { session_id, question_text, context: "resume|question|feedback" }
       Output: { answer_text, follow_up_suggestions: [...] }
```

### 2.2 Implementation Details

#### **`app/placement_module.py`** (NEW)

```python
"""
Core placement preparation module
Orchestrates all placement features
"""

from flask import Blueprint, request, jsonify, session
from app.resume_intelligence import ResumeIntelligence
from app.question_engine import QuestionEngine
from app.evaluation_engine import EvaluationEngine
from app.roadmap_generator import RoadmapGenerator
from app.db import db
from datetime import datetime
import logging

placement_bp = Blueprint('placement', __name__, url_prefix='/api/placement')
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# RESUME INTELLIGENCE
# ═══════════════════════════════════════════════════════════════

@placement_bp.route('/resume/analyze', methods=['POST'])
def analyze_resume():
    """Enhanced resume analysis for placement prep"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json(silent=True) or {}
        resume_id = data.get('resume_id')
        
        # Get resume from database
        from app.db import get_db
        db_conn = get_db()
        resume = db_conn.execute(
            'SELECT file_path FROM resumes WHERE id = ? AND user_email = ?',
            (resume_id, email)
        ).fetchone()
        
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Analyze resume
        ri = ResumeIntelligence()
        analysis = ri.analyze_full_resume(resume[0], email)
        
        # Save analysis to database
        db_conn.execute('''
            INSERT INTO resume_analysis 
            (user_email, resume_id, skills_technical, skills_soft, 
             projects, experience_level, profile_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email,
            resume_id,
            str(analysis['skills']['technical']),
            str(analysis['skills']['soft']),
            str(analysis['projects']),
            analysis['experience_level'],
            analysis['profile_score'],
            datetime.now()
        ))
        db_conn.commit()
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        logger.error(f"Resume analysis error: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500


@placement_bp.route('/resume/profile', methods=['GET'])
def get_resume_profile():
    """Get current user's resume profile"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from app.db import get_db
        db_conn = get_db()
        
        # Get latest analysis
        analysis = db_conn.execute('''
            SELECT skills_technical, skills_soft, projects, 
                   experience_level, profile_score
            FROM resume_analysis
            WHERE user_email = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (email,)).fetchone()
        
        if not analysis:
            return jsonify({'error': 'No resume analysis found'}), 404
        
        return jsonify({
            'skills': {
                'technical': eval(analysis[0]),
                'soft': eval(analysis[1])
            },
            'projects': eval(analysis[2]),
            'experience_level': analysis[3],
            'profile_score': analysis[4]
        })
    
    except Exception as e:
        logger.error(f"Profile fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch profile'}), 500


# ═══════════════════════════════════════════════════════════════
# COMPANY & SESSION MANAGEMENT
# ═══════════════════════════════════════════════════════════════

@placement_bp.route('/companies', methods=['GET'])
def list_companies():
    """Get companies for placement prep"""
    search = request.args.get('search', '').lower()
    industry = request.args.get('industry', '')
    role = request.args.get('role', '')
    
    try:
        from app.db import get_db
        db_conn = get_db()
        
        query = 'SELECT id, name, industry, popular_roles, difficulty_level FROM companies WHERE 1=1'
        params = []
        
        if search:
            query += ' AND name LIKE ?'
            params.append(f'%{search}%')
        
        if industry:
            query += ' AND industry = ?'
            params.append(industry)
        
        if role:
            query += ' AND popular_roles LIKE ?'
            params.append(f'%{role}%')
        
        query += ' LIMIT 50'
        
        companies = db_conn.execute(query, params).fetchall()
        
        return jsonify({
            'companies': [
                {
                    'id': c[0],
                    'name': c[1],
                    'industry': c[2],
                    'popular_roles': eval(c[3]) if c[3] else [],
                    'difficulty': c[4]
                }
                for c in companies
            ]
        })
    
    except Exception as e:
        logger.error(f"Company listing error: {str(e)}")
        return jsonify({'error': 'Failed to list companies'}), 500


@placement_bp.route('/session/create', methods=['POST'])
def create_interview_session():
    """Create new interview practice session"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json(silent=True) or {}
        company_id = data.get('company_id')
        role = data.get('role')
        difficulty = data.get('difficulty_preference', 3)
        
        from app.db import get_db
        import uuid
        
        db_conn = get_db()
        session_id = str(uuid.uuid4())
        
        db_conn.execute('''
            INSERT INTO interview_sessions
            (session_id, user_email, company_id, role, difficulty, 
             status, created_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?)
        ''', (session_id, email, company_id, role, difficulty, datetime.now()))
        
        db_conn.commit()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'role': role,
            'company_id': company_id
        })
    
    except Exception as e:
        logger.error(f"Session creation error: {str(e)}")
        return jsonify({'error': 'Failed to create session'}), 500


# ═══════════════════════════════════════════════════════════════
# QUESTION GENERATION
# ═══════════════════════════════════════════════════════════════

@placement_bp.route('/questions/generate', methods=['POST'])
def generate_questions():
    """Generate interview questions using RAG + LLM"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json(silent=True) or {}
        session_id = data.get('session_id')
        company_id = data.get('company_id')
        role = data.get('role')
        difficulty = data.get('difficulty', 3)
        
        qe = QuestionEngine()
        questions = qe.generate_interview_questions(
            company_id=company_id,
            role=role,
            difficulty=difficulty,
            num_questions=10
        )
        
        # Store questions in database
        from app.db import get_db
        db_conn = get_db()
        
        for q in questions:
            db_conn.execute('''
                INSERT INTO interview_questions
                (session_id, question_type, question_text, 
                 difficulty, expected_keywords, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                q['type'],
                q['question'],
                q['difficulty'],
                str(q.get('expected_keywords', [])),
                datetime.now()
            ))
        
        db_conn.commit()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'questions': questions,
            'total_count': len(questions)
        })
    
    except Exception as e:
        logger.error(f"Question generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate questions'}), 500


@placement_bp.route('/questions/<session_id>', methods=['GET'])
def get_session_questions(session_id):
    """Retrieve questions for a session"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from app.db import get_db
        db_conn = get_db()
        
        questions = db_conn.execute('''
            SELECT id, question_type, question_text, difficulty,
                   expected_keywords
            FROM interview_questions
            WHERE session_id = ?
            ORDER BY id
        ''', (session_id,)).fetchall()
        
        return jsonify({
            'questions': [
                {
                    'id': q[0],
                    'type': q[1],
                    'question': q[2],
                    'difficulty': q[3],
                    'expected_keywords': eval(q[4]) if q[4] else []
                }
                for q in questions
            ]
        })
    
    except Exception as e:
        logger.error(f"Question fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch questions'}), 500


# ═══════════════════════════════════════════════════════════════
# ANSWER SUBMISSION & EVALUATION
# ═══════════════════════════════════════════════════════════════

@placement_bp.route('/answers/submit', methods=['POST'])
def submit_answer():
    """Submit answer for evaluation"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json(silent=True) or {}
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        answer_text = data.get('answer_text', '')
        time_taken = data.get('time_taken', 0)
        
        if not answer_text.strip():
            return jsonify({'error': 'Answer cannot be empty'}), 400
        
        from app.db import get_db
        import uuid
        
        db_conn = get_db()
        answer_id = str(uuid.uuid4())
        
        db_conn.execute('''
            INSERT INTO user_answers
            (answer_id, session_id, question_id, user_email, 
             answer_text, time_taken, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'submitted', ?)
        ''', (
            answer_id, session_id, question_id, email,
            answer_text, time_taken, datetime.now()
        ))
        
        db_conn.commit()
        
        # Queue for evaluation (async in production)
        ee = EvaluationEngine()
        evaluation = ee.evaluate_answer_async(answer_id)
        
        return jsonify({
            'success': True,
            'answer_id': answer_id,
            'status': 'evaluating'
        })
    
    except Exception as e:
        logger.error(f"Answer submission error: {str(e)}")
        return jsonify({'error': 'Failed to submit answer'}), 500


@placement_bp.route('/answers/<answer_id>/evaluate', methods=['GET'])
def get_evaluation(answer_id):
    """Get evaluation for submitted answer"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from app.db import get_db
        db_conn = get_db()
        
        # Get evaluation
        eval_result = db_conn.execute('''
            SELECT score_correctness, score_clarity, score_depth,
                   score_communication, strengths, weaknesses,
                   model_answer, tips, status
            FROM evaluation_results
            WHERE answer_id = ?
        ''', (answer_id,)).fetchone()
        
        if not eval_result:
            return jsonify({'status': 'pending'}), 202  # Still evaluating
        
        overall_score = round(sum(eval_result[:4]) / 4, 1)
        
        return jsonify({
            'status': eval_result[8],
            'scores': {
                'correctness': eval_result[0],
                'clarity': eval_result[1],
                'depth': eval_result[2],
                'communication': eval_result[3],
                'overall': overall_score
            },
            'strengths': eval(eval_result[4]) if eval_result[4] else [],
            'weaknesses': eval(eval_result[5]) if eval_result[5] else [],
            'model_answer': eval_result[6],
            'tips': eval(eval_result[7]) if eval_result[7] else []
        })
    
    except Exception as e:
        logger.error(f"Evaluation fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch evaluation'}), 500


# ═══════════════════════════════════════════════════════════════
# ROADMAP & PROGRESS
# ═══════════════════════════════════════════════════════════════

@placement_bp.route('/roadmap/generate', methods=['POST'])
def generate_roadmap():
    """Generate personalized preparation roadmap"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json(silent=True) or {}
        company_id = data.get('company_id')
        target_date = data.get('target_date')  # Format: YYYY-MM-DD
        
        rg = RoadmapGenerator()
        roadmap = rg.generate_roadmap(
            user_email=email,
            company_id=company_id,
            target_date=target_date
        )
        
        from app.db import get_db
        import uuid
        
        db_conn = get_db()
        roadmap_id = str(uuid.uuid4())
        
        db_conn.execute('''
            INSERT INTO roadmap
            (roadmap_id, user_email, company_id, target_date,
             weak_topics, daily_plan, resources, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
        ''', (
            roadmap_id, email, company_id, target_date,
            str(roadmap['weak_topics']),
            str(roadmap['daily_plan']),
            str(roadmap['resources']),
            datetime.now()
        ))
        
        db_conn.commit()
        
        return jsonify({
            'success': True,
            'roadmap_id': roadmap_id,
            'roadmap': roadmap
        })
    
    except Exception as e:
        logger.error(f"Roadmap generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate roadmap'}), 500


@placement_bp.route('/roadmap/<roadmap_id>', methods=['GET'])
def get_roadmap(roadmap_id):
    """Get current roadmap"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from app.db import get_db
        db_conn = get_db()
        
        roadmap = db_conn.execute('''
            SELECT roadmap_id, company_id, target_date, weak_topics,
                   daily_plan, resources, status
            FROM roadmap
            WHERE roadmap_id = ? AND user_email = ?
        ''', (roadmap_id, email)).fetchone()
        
        if not roadmap:
            return jsonify({'error': 'Roadmap not found'}), 404
        
        return jsonify({
            'roadmap_id': roadmap[0],
            'company_id': roadmap[1],
            'target_date': roadmap[2],
            'weak_topics': eval(roadmap[3]) if roadmap[3] else [],
            'daily_plan': eval(roadmap[4]) if roadmap[4] else [],
            'resources': eval(roadmap[5]) if roadmap[5] else [],
            'status': roadmap[6]
        })
    
    except Exception as e:
        logger.error(f"Roadmap fetch error: {str(e)}")
        return jsonify({'error': 'Failed to fetch roadmap'}), 500


@placement_bp.route('/progress/dashboard', methods=['GET'])
def get_progress_dashboard():
    """Get overall progress and interview readiness"""
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from app.db import get_db
        db_conn = get_db()
        
        # Get all sessions and scores
        sessions = db_conn.execute('''
            SELECT COUNT(*) FROM interview_sessions WHERE user_email = ?
        ''', (email,)).fetchone()
        
        avg_score = db_conn.execute('''
            SELECT AVG(
                (score_correctness + score_clarity + score_depth + 
                 score_communication) / 4.0
            ) FROM evaluation_results
            WHERE answer_id IN (
                SELECT answer_id FROM user_answers WHERE user_email = ?
            )
        ''', (email,)).fetchone()
        
        companies = db_conn.execute('''
            SELECT DISTINCT company_id FROM interview_sessions
            WHERE user_email = ?
        ''', (email,)).fetchall()
        
        weak_topics = db_conn.execute('''
            SELECT weak_topics FROM roadmap
            WHERE user_email = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (email,)).fetchone()
        
        return jsonify({
            'interview_readiness_score': min(100, round((avg_score[0] or 0) * 10)),
            'sessions_completed': sessions[0] if sessions[0] else 0,
            'companies_targeted': len(companies),
            'average_score': round(avg_score[0], 1) if avg_score[0] else 0,
            'weak_topics': eval(weak_topics[0]) if weak_topics and weak_topics[0] else [],
            'next_steps': ['Continue practicing', 'Focus on weak topics', 'Take more mock tests']
        })
    
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard'}), 500
```

---

## 3. LLM PROMPT DESIGN

### 3.1 Resume Analysis Prompt

```python
RESUME_ANALYSIS_PROMPT = """
You are an expert HR recruiter analyzing a candidate's resume for placement preparation.

RESUME TEXT:
{resume_text}

TASK: Extract and analyze the following:

1. **Technical Skills**: List all programming languages, frameworks, tools, databases
2. **Soft Skills**: Communication, leadership, teamwork, problem-solving, etc.
3. **Projects**: Extract name, description, technologies used (max 5 most relevant)
4. **Experience Level**: Classify as "fresher/junior/mid/ senior" based on:
   - Years of experience (inferred from graduation year if available)
   - Project complexity
   - Skill level
5. **Profile Score**: Rate 0-100 based on:
   - Clarity and formatting (20%)
   - Technical depth (30%)
   - Project quality (25%)
   - Communication (15%)
   - Completeness (10%)

IMPORTANT: Be strict but fair. This is for competitive placement.

OUTPUT FORMAT (JSON):
{
  "technical_skills": ["Python", "React", "SQL", ...],
  "soft_skills": ["Leadership", "Communication", ...],
  "projects": [
    {
      "name": "...",
      "description": "...",
      "technologies": ["..."],
      "impact": "..."
    }
  ],
  "experience_level": "junior|mid|senior",
  "profile_score": 75,
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "improvements_needed": ["...", "..."]
}
"""
```

### 3.2 Interview Question Generation Prompt

```python
QUESTION_GENERATION_PROMPT = """
You are an expert technical interviewer for {company_name} preparing interview questions 
for the role of {role}.

CANDIDATE PROFILE:
- Experience Level: {experience_level}
- Technical Skills: {skills}
- Industry Experience: {industry_experience}

TARGET DIFFICULTY LEVEL: {difficulty} (1=Easy, 5=Expert)

TASK: Generate 10 diverse interview questions following this distribution:
- 4 technical/conceptual questions (role-specific)
- 3 behavioral/HR questions  
- 3 coding/problem-solving questions

For each question:
1. Tailor to candidate's skill level
2. Align with {company_name}'s tech stack
3. Highlight expected keywords/concepts

CONSTRAINTS:
- Questions should assess {role} competencies
- Avoid yes/no questions
- Include real-world scenarios
- Expected answer time: 3-5 minutes each

OUTPUT FORMAT (JSON):
{
  "questions": [
    {
      "id": 1,
      "type": "technical|behavioral|coding",
      "question": "...",
      "difficulty": 1-5,
      "expected_keywords": ["keyword1", "keyword2"],
      "expected_duration_minutes": 3,
      "scoring_criteria": ["Correctness", "Depth", "Communication"],
      "sample_structure": "Expected answer should cover..."
    }
  ]
}
"""
```

### 3.3 Answer Evaluation Prompt

```python
ANSWER_EVALUATION_PROMPT = """
You are an expert interviewer evaluating a candidate's answer to an interview question.

QUESTION: {question}
CANDIDATE ANSWER: {answer}
EXPECTED KEYWORDS: {expected_keywords}
DIFFICULTY LEVEL: {difficulty}

TASK: Evaluate the answer on 4 dimensions (0-10 each):

1. **CORRECTNESS (0-10)**
   - Is the answer technically accurate?
   - Are there misconceptions or errors?
   - Does it address the core question?

2. **CLARITY (0-10)**
   - Is the explanation easy to follow?
   - Does the candidate explain step-by-step?
   - Are examples provided?

3. **DEPTH (0-10)**
   - Does answer go beyond surface level?
   - Are edge cases/advanced concepts covered?
   - Is there critical thinking?

4. **COMMUNICATION (0-10)**
   - Is language professional and clear?
   - Good structure and organization?
   - Appropriate pace and detail level?

OUTPUT FORMAT (JSON):
{
  "scores": {
    "correctness": 7,
    "clarity": 8,
    "depth": 6,
    "communication": 8,
    "overall": 7.25
  },
  "strengths": [
    "Correctly identified the core concept",
    "Provided relevant example"
  ],
  "weaknesses": [
    "Missed handling edge case",
    "Could have discussed complexity analysis"
  ],
  "model_answer": "The ideal answer should cover: 1) ... 2) ... 3) ...",
  "tips_for_improvement": [
    "Study edge case handling",
    "Practice communicating complexity trade-offs"
  ],
  "follow_up_questions": [
    "How would you optimize this further?",
    "What if constraints change?"
  ]
}
"""
```

### 3.4 Roadmap Generation Prompt

```python
ROADMAP_GENERATION_PROMPT = """
You are a career coach creating a personalized interview preparation roadmap.

CANDIDATE PROFILE:
- Experience Level: {experience_level}
- Current Skills: {skills}
- Skill Gaps: {skill_gaps}
- Target Company: {company_name}
- Target Role: {role}
- Target Date: {target_date} (Days remaining: {days_remaining})

RECENT PERFORMANCE:
- Average Answer Score: {avg_score}/10
- Weak Areas: {weak_areas}
- Strong Areas: {strong_areas}

TASK: Create a structured {days_remaining}-day preparation roadmap

ROADMAP STRUCTURE:
1. **Weak Topics Identification**: Rank top 5 topics to focus on
2. **Daily Plan**: 
   - Week 1: Foundation building
   - Week 2: Advanced concepts + practice
   - Week 3: Full mocks + refinement
3. **Resources**: Videos, articles, practice problems (link to existing resources)
4. **Milestones**: Weekly targets and checkpoints

CONSTRAINTS:
- Realistically achievable in {days_remaining} days
- 3-4 hours daily study recommended
- Include breaks and review days
- Specific, measurable goals

OUTPUT FORMAT (JSON):
{
  "weak_topics": ["Topic 1", "Topic 2", ...],
  "strong_topics": ["Topic A", "Topic B"],
  "daily_plan": [
    {
      "day": 1,
      "date": "2024-04-10",
      "topic": "Data Structures Fundamentals",
      "tasks": [
        "Watch: Arrays & Linked Lists (45 min)",
        "Read: Algorithm analysis (30 min)",
        "Practice: 5 coding problems (1 hour)"
      ],
      "resources": ["YouTube link", "Article link"],
      "time_required": "2.25 hours"
    }
  ],
  "milestones": [
    {
      "week": 1,
      "target": "Score 6/10 on weak topics",
      "reviews": ["Day 4", "Day 7"]
    }
  ],
  "estimated_improvement": "Expected: 5/10 → 8/10 by target date"
}
"""
```

---

## 4. DATABASE SCHEMA UPDATES

### 4.1 New Tables

#### **`companies`** - Store company profiles

```sql
CREATE TABLE companies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  industry TEXT,
  popular_roles TEXT,  -- JSON array: ["SDE", "Data Engineer"]
  difficulty_level INTEGER DEFAULT 3,  -- 1-5
  tech_stack TEXT,  -- JSON array of technologies
  interview_patterns TEXT,  -- JSON: {rounds: [], avg_duration: 120}
  recent_questions BLOB,  -- Cached question data
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **`resume_analysis`** - Store resume parsing results

```sql
CREATE TABLE resume_analysis (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_email TEXT NOT NULL,
  resume_id INTEGER,
  skills_technical TEXT,  -- JSON array
  skills_soft TEXT,  -- JSON array
  projects TEXT,  -- JSON array
  experience_level TEXT,  -- "junior|mid|senior"
  profile_score INTEGER,  -- 0-100
  profile_feedback TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_email) REFERENCES user(email)
);

CREATE INDEX idx_resume_analysis_email ON resume_analysis(user_email, created_at DESC);
```

#### **`interview_sessions`** - Track interview practice sessions

```sql
CREATE TABLE interview_sessions (
  session_id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  role TEXT,
  difficulty INTEGER DEFAULT 3,
  status TEXT DEFAULT 'active',  -- "active|completed|abandoned"
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ended_at TIMESTAMP,
  total_score REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_email) REFERENCES user(email),
  FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_sessions_user ON interview_sessions(user_email, created_at DESC);
```

#### **`interview_questions`** - Store generated interview questions

```sql
CREATE TABLE interview_questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  question_type TEXT,  -- "technical|behavioral|coding"
  question_text TEXT NOT NULL,
  difficulty INTEGER,
  expected_keywords TEXT,  -- JSON array
  company_context TEXT,  -- JSON: {company_id, role}
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id)
);

CREATE INDEX idx_questions_session ON interview_questions(session_id);
```

#### **`user_answers`** - Store user submissions

```sql
CREATE TABLE user_answers (
  answer_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  question_id INTEGER NOT NULL,
  user_email TEXT NOT NULL,
  answer_text TEXT NOT NULL,
  time_taken INTEGER,  -- seconds
  status TEXT DEFAULT 'submitted',  -- "submitted|evaluated|reviewed"
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id),
  FOREIGN KEY (question_id) REFERENCES interview_questions(id),
  FOREIGN KEY (user_email) REFERENCES user(email)
);

CREATE INDEX idx_answers_session ON user_answers(session_id);
CREATE INDEX idx_answers_email ON user_answers(user_email);
```

#### **`evaluation_results`** - Store AI evaluation feedback

```sql
CREATE TABLE evaluation_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  answer_id TEXT NOT NULL UNIQUE,
  score_correctness REAL,  -- 0-10
  score_clarity REAL,
  score_depth REAL,
  score_communication REAL,
  overall_score REAL,  -- Average of above
  strengths TEXT,  -- JSON array
  weaknesses TEXT,  -- JSON array
  model_answer TEXT,
  tips TEXT,  -- JSON array
  follow_up_suggestions TEXT,  -- JSON array
  evaluation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status TEXT DEFAULT 'completed',
  FOREIGN KEY (answer_id) REFERENCES user_answers(answer_id)
);

CREATE INDEX idx_evaluation_answer ON evaluation_results(answer_id);
```

#### **`roadmap`** - Personalized preparation roadmaps

```sql
CREATE TABLE roadmap (
  roadmap_id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  target_date DATE,
  weak_topics TEXT,  -- JSON array of topics
  daily_plan TEXT,  -- JSON array of daily tasks
  resources TEXT,  -- JSON: {topic: [resources]}
  status TEXT DEFAULT 'active',  -- "active|completed|paused"
  progress REAL DEFAULT 0,  -- 0-100%
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_email) REFERENCES user(email),
  FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_roadmap_user ON roadmap(user_email, created_at DESC);
```

#### **`roadmap_progress`** - Track daily roadmap completion

```sql
CREATE TABLE roadmap_progress (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  roadmap_id TEXT NOT NULL,
  day_number INTEGER,
  task_id INTEGER,
  status TEXT,  -- "completed|pending|skipped"
  completed_at TIMESTAMP,
  FOREIGN KEY (roadmap_id) REFERENCES roadmap(roadmap_id)
);
```

---

## 5. FRONTEND FLOW

### 5.1 New Pages to Create

#### **Path 1: `/placement/dashboard` - Placement Hub**

```html
<!-- Placement Dashboard -->
Navigation:
├── My Resume Profile
├── Interview Sessions
├── Roadmap & Progress
└── Analytics

Components:
┌─────────────────────────────────────┐
│  Placement Dashboard                │
├─────────────────────────────────────┤
│ Interview Readiness Score: 72/100   │
│ ████████░░░░░░░░░░░░               │
│                                     │
│ Quick Stats:                        │
│  • Companies Targeted: 5            │
│  • Sessions Done: 12                │
│  • Avg Score: 7.2/10                │
│  • Days Prepared: 14                │
│                                     │
│ [Start New Session] [View Roadmap]  │
│                                     │
│ Recent Sessions:                    │
│ ┌─────────────────┐                 │
│ │ Google - SDE    │ Score: 8/10     │
│ │ 2 days ago      │ Progress: 100%  │
│ └─────────────────┘                 │
└─────────────────────────────────────┘
```

#### **Path 2: `/placement/resume-analysis` - Resume Intelligence**

```html
<!-- Resume Analysis & Profile Building -->

Step 1: Upload Resume
├── Input: PDF/DOCX file
└── Action: [Analyze]

Step 2: Extracted Profile
├── Technical Skills: [Python, React, SQL, ...]
├── Soft Skills: [Leadership, Communication]
├── Projects: [Project 1, Project 2, ...]
├── Experience Level: Mid-level (3-4 years)
├── Profile Score: 78/100
│   ├── Strengths: Good project portfolio
│   └── Gaps: AWS/Cloud skills missing
└── Action: [Use This Profile] [Re-upload]

Step 3: Skill Mapping
├── Your Skills: [Python, JavaScript, React]
├── Target Role (Google SDE):
│   ├── Required: [DSA, System Design, SQL]
│   ├── Matched: [Python, JavaScript]
│   └── Gaps: [System Design, Concurrency]
└── Action: [Start Preparation]
```

#### **Path 3: `/placement/company-select` - Company Selector**

```html
<!-- Company Selection & Role Mapping -->

┌──────────────────────────────────────┐
│ Select Your Target Company           │
├──────────────────────────────────────┤
│ Search: [____________________] 🔍    │
│ Industry: [Select ▼]                 │
│ Role: [Select ▼]                     │
│                                      │
│ Top Companies:                       │
│ ┌─────────────────────────────────┐ │
│ │ 🔵 Google                       │ │
│ │ Roles: SDE, ML Engineer         │ │
│ │ Difficulty: ⭐⭐⭐⭐⭐            │ │
│ │ [Select Role ▼]                 │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🔵 Amazon                       │ │
│ │ Roles: SDE, DevOps              │ │
│ │ Difficulty: ⭐⭐⭐⭐              │ │
│ │ [Select Role ▼]                 │ │
│ └─────────────────────────────────┘ │
│                                      │
│ [Create Interview Session]           │
└──────────────────────────────────────┘
```

#### **Path 4: `/placement/practice/<session_id>` - Interview Practice**

```html
<!-- Interview Practice Interface -->

┌──────────────────────────────────────────────┐
│ Interview: Google SDE (Question 3 of 10)    │
├──────────────────────────────────────────────┤
│ Time: 04:32 ⏱ | Score: ---- | Difficulty: ⭐⭐⭐│
├──────────────────────────────────────────────┤
│                                              │
│ QUESTION:                                    │
│ "Design a URL shortening service like       │
│  Bit.ly. Discuss scalability, storage,      │
│  and tradeoffs."                            │
│                                              │
│ [💻 Code Editor] [📝 Notes] [🎤 Dictate]   │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ Your Answer:                             │ │
│ │ (Text Input Area - Auto-save)            │ │
│ │ ...                                      │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ Suggested Topics: DB design, Caching        │
│                                              │
│ [Skip] [Submit Answer]                      │
└──────────────────────────────────────────────┘

After Submit → Loading evaluation...
  ⏳ Powered by AI evaluation
```

#### **Path 5: `/placement/feedback/<answer_id>` - Answer Feedback**

```html
<!-- AI Evaluation & Feedback -->

┌─────────────────────────────────────────┐
│ Your Answer Evaluation                  │
├─────────────────────────────────────────┤
│ OVERALL SCORE: 7.5 / 10  ✅ Good       │
│ ████████░░░░░░░░░░░░                  │
│                                         │
│ Breakdown:                              │
│ • Correctness: 8/10   ████████░░       │
│ • Clarity: 7/10       ███████░░░       │
│ • Depth: 7/10         ███████░░░       │
│ • Communication: 8/10 ████████░░       │
│                                         │
│ STRENGTHS ✅                            │
│ • Correctly identified scalability      │
│ • Good discussion of trade-offs         │
│ • Clear architecture explanation        │
│                                         │
│ AREAS TO IMPROVE 📈                     │
│ • Missing caching layer discussion      │
│ • Database partitioning not covered     │
│ • Could estimate QPS/storage better     │
│                                         │
│ MODEL ANSWER:                           │
│ "The ideal approach covers: 1) High     │
│  level design with components, 2)      │
│  Database sharding strategy..."         │
│                                         │
│ TIPS FOR NEXT TIME:                     │
│ • Practice system design templates      │
│ • Review distributed systems concepts   │
│                                         │
│ [Next Question] [View Roadmap]          │
└─────────────────────────────────────────┘
```

#### **Path 6: `/placement/roadmap/<roadmap_id>` - Preparation Roadmap**

```html
<!-- Personalized Preparation Roadmap -->

┌──────────────────────────────────────────┐
│ Your Roadmap: Google SDE Preparation    │
│ Target Date: May 30 (45 days)           │
├──────────────────────────────────────────┤
│ Progress: ██████░░░░░ 40% Complete      │
│                                          │
│ KEY METRICS:                             │
│ • Current Level: Mid (6.2/10)            │
│ • Target Level: Senior (8.5+/10)         │
│ • Estimated Time: 3 hours/day            │
│                                          │
│ WEAK TOPICS (Focus Areas):               │
│ 1. System Design        ⚠️ 35% mastery   │
│ 2. Database Optimization ⚠️ 40% mastery  │
│ 3. Concurrency          ⚠️ 45% mastery   │
│ 4. Distributed Systems  ✅ 70% mastery   │
│ 5. OOP Design Patterns  ✅ 75% mastery   │
│                                          │
│ WEEK 1 PLAN: Systems Fundamentals       │
│ ┌────────────────────────────────────┐  │
│ │ Day 1-2: Database Fundamentals     │ ✓ │
│ │ • Videos: [YouTube]                │   │
│ │ • Practice: 5 SQL problems         │   │
│ │ Status: ✅ Completed               │   │
│ └────────────────────────────────────┘  │
│ ┌────────────────────────────────────┐  │
│ │ Day 3-4: Indexing & Optimization   │ ⏳ │
│ │ • Videos: [YouTube]                │   │
│ │ • Practice: Query tuning           │   │
│ │ Status: 🔄 In Progress (60%)       │   │
│ └────────────────────────────────────┘  │
│ ┌────────────────────────────────────┐  │
│ │ Day 5-7: Sharding & Scaling        │ ⭕ │
│ │ • Videos: [YouTube]                │   │
│ │ • Practice: Design patterns        │   │
│ │ Status: ⭕ Pending                  │   │
│ └────────────────────────────────────┘  │
│                                          │
│ [Mark Complete] [Skip Day] [Adjust]     │
│ [Generate New Roadmap]                  │
└──────────────────────────────────────────┘
```

#### **Path 7: `/placement/coach` - Interview Coach Chatbot**

```html
<!-- Interview Coach - Chatbot Extension -->

┌─────────────────────────────────────────┐
│ Interview Coach Assistant               │
├─────────────────────────────────────────┤
│                                         │
│ Coach: "Hi! I'm your interview coach.  │
│ Need help preparing? Ask me anything!"  │
│                                         │
│ You: "How do I approach system design?"ี
│                                         │
│ Coach: "Great question! System design │
│ interviews have this structure:        │
│ 1) Clarify requirements               │
│ 2) High-level architecture            │
│ 3) Deep dive into components          │
│ 4) Discuss trade-offs                 │
│ 5) Optimization & scaling             │
│                                         │
│ Want me to give you a sample question?"│
│                                         │
│ [Yes] [No] [Show tips] [End]           │
│                                         │
│ Input: [________________] [Send 📤]    │
└─────────────────────────────────────────┘
```

### 5.2 UI Flow Description

```
COMPLETE INTERVIEW PREP WORKFLOW:

1. ENTRY POINT: Placement Dashboard
   └─→ View readiness score, recent sessions
   └─→ Choose action: Start session or view roadmap

2. RESUME SETUP (First time only)
   └─→ Upload resume
   └─→ AI extracts skills, projects, experience level
   └─→ Verify and confirm profile
   └─→ Save to account

3. SELECT COMPANY & ROLE
   └─→ Search from 1000+ companies
   └─→ View difficulty level
   └─→ Select target role
   └─→ Create interview session

4. INTERVIEW PRACTICE
   └─→ Receive 10 tailored questions
   └─→ Read question + context
   └─→ Type/dictate answer
   └─→ Submit for evaluation

5. GET FEEDBACK
   └─→ AI evaluates answer instantly
   └─→ Receive score breakdown (correctness, clarity, depth, communication)
   └─→ View strengths and improvements
   └─→ Read model answer

6. VIEW ROADMAP
   └─→ See personalized preparation plan
   └─→ Track daily tasks
   └─→ Mark tasks complete
   └─→ Get recommendations

7. TRACK PROGRESS
   └─→ View overall readiness score
   └─→ See improvement over time
   └─→ Compare company-wise scores
   └─→ Get next steps recommendation
```

---

## 6. STEP-BY-STEP IMPLEMENTATION PLAN

### Phase 1: Core Features (Days 1-3, Hackathon Ready)

**Day 1: Infrastructure & Resume Intelligence**

- [ ] Create database tables (companies, resume_analysis, interview_sessions)
- [ ] Build `app/resume_intelligence.py` module
  - Extract skills using regex + NLP
  - Classify experience level
  - Score resume quality
- [ ] Build `app/placement_module.py` with routes:
  - `POST /api/placement/resume/analyze`
  - `GET /api/placement/resume/profile`
- [ ] Create frontend: `/placement/dashboard`, `/placement/resume-analysis`
- [ ] **Deliverable:** Resume upload → profile extraction working

**Day 2: Question Generation & Company Selection**

- [ ] Seed `companies` table with 20-50 top companies
- [ ] Build `app/question_engine.py` module
  - Use RAG to retrieve company-specific questions
  - Generate tailored questions using LLM
  - Cache generated questions
- [ ] Create interview_questions table + indexing
- [ ] Build routes:
  - `GET /api/placement/companies?search=&industry=`
  - `POST /api/placement/session/create`
  - `POST /api/placement/questions/generate`
- [ ] Create frontend: `/placement/company-select`, `/placement/practice`
- [ ] **Deliverable:** Company selection → question generation working

**Day 3: Answer Evaluation & Roadmap**

- [ ] Build `app/evaluation_engine.py` module
  - LLM-powered answer evaluation
  - Score all 4 dimensions
  - Generate feedback and model answer
- [ ] Build `app/roadmap_generator.py` module
  - Gap analysis from resume vs company requirement
  - Generate daily study plan
  - Link to existing resources
- [ ] Build routes:
  - `POST /api/placement/answers/submit`
  - `GET /api/placement/answers/<answer_id>/evaluate`
  - `POST /api/placement/roadmap/generate`
  - `GET /api/placement/progress/dashboard`
- [ ] Create frontend: `/placement/feedback`, `/placement/roadmap`
- [ ] **Deliverable:** Complete workflow: Analyze → Practice → Feedback → Roadmap

### Phase 2: Enhancements (Days 4-7)

**Day 4: Optimization & Polish**

- [ ] Add caching for frequently generated questions
- [ ] Optimize database queries with proper indexing
- [ ] Add pagination to large result sets
- [ ] Implement real-time evaluation status updates
- [ ] Create comprehensive error handling

**Day 5: Analytics & Tracking**

- [ ] Build analytics module for performance tracking
- [ ] Add comparison charts (progress over time)
- [ ] Implement company-wise performance tracking
- [ ] Create export functionality (PDF reports)

**Day 6: Interview Coach Chatbot**

- [ ] Extend existing chatbot to be interview coach
- [ ] Add context-aware assistance based on user's session
- [ ] Provide tips for weak areas
- [ ] Mock interview mode (chatbot asks questions)

**Day 7: Testing & Deployment**

- [ ] Write unit tests for core modules
- [ ] Integration tests for complete workflow
- [ ] Load testing for concurrent users
- [ ] Deploy to production environment

### Phase 3: Advanced Features (Post-Hackathon)

**Week 2-3: Advanced Capabilities**

- [ ] **Voice Interview Simulation**
  - Speech-to-text for interview answers
  - AI evaluation of speech quality
  - Accent/fluency feedback

- [ ] **Real-Time Feedback During Practice**
  - Chatbot monitor listening and prompting for depth
  - Real-time feedback on clarity

- [ ] **Company-Wise Difficulty Levels**
  - Scrape recent interview patterns
  - Adjust difficulty based on company
  - Question bank expansion

- [ ] **Advanced Analytics**
  - Predictive score modeling
  - Company-wise success probability
  - Peer benchmarking (anonymous)

- [ ] **Integration with LeetCode/HackerRank**
  - Link coding problems
  - Track code submissions
  - Auto-evaluate solution quality

---

## 7. OPTIONAL ADVANCED FEATURES

### 7.1 Voice-Based Interview Simulation

```python
# app/voice_evaluation.py

from google.cloud import speech_v1
from google.cloud import language_v1

class VoiceInterviewEvaluator:
    """Evaluate interview performance from voice"""
    
    def __init__(self):
        self.speech_client = speech_v1.SpeechClient()
        self.language_client = language_v1.LanguageServiceClient()
    
    def transcribe_audio(self, audio_file_path):
        """Convert speech to text"""
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()
        
        audio = speech_v1.RecognitionAudio(content=content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        
        response = self.speech_client.recognize(config=config, audio=audio)
        return "".join(result.alternatives[0].transcript for result in response.results)
    
    def evaluate_speech_quality(self, transcript):
        """Evaluate speech quality metrics"""
        document = language_v1.Document(
            content=transcript,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )
        
        response = self.language_client.analyze_sentiment(request={"document": document})
        sentiment = response.document_sentiment
        
        # Calculate metrics
        metrics = {
            'confidence': sentiment.score * 10,  # Convert to 0-10
            'fluency': self._calculate_fluency(transcript),
            'clarity': self._calculate_clarity(transcript),
            'pace': self._calculate_pace(transcript),
            'filler_words': self._count_filler_words(transcript)
        }
        
        return metrics
    
    def _calculate_fluency(self, text):
        """Score based on sentence structure"""
        sentences = text.split('.')
        avg_length = len(text) / len(sentences) if sentences else 0
        # Ideal sentence: 10-20 words
        return min(10, (avg_length / 15) * 10)
    
    def _calculate_clarity(self, text):
        """Score based on vocabulary and coherence"""
        # Simple: word variety and repetition analysis
        words = text.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        return unique_ratio * 10
    
    def _calculate_pace(self, text):
        """Score based on speech rate"""
        # Ideal: 130-160 words per minute
        word_count = len(text.split())
        return min(10, (word_count / 2.5))
    
    def _count_filler_words(self, text):
        """Count umm, uh, like, you know"""
        filler_words = ['umm', 'uh', 'like', 'you know', 'actually', 'basically']
        text_lower = text.lower()
        count = sum(text_lower.count(word) for word in filler_words)
        return count
```

**API Endpoint:**

```python
@placement_bp.route('/practice/voice-submit', methods=['POST'])
def submit_voice_answer():
    """Submit voice answer and get evaluation"""
    audio_file = request.files['audio']
    session_id = request.form.get('session_id')
    question_id = request.form.get('question_id')
    
    # Transcribe
    voice_eval = VoiceInterviewEvaluator()
    transcript = voice_eval.transcribe_audio(audio_file)
    
    # Get voice metrics
    voice_metrics = voice_eval.evaluate_speech_quality(transcript)
    
    # Evaluate answer content
    ee = EvaluationEngine()
    content_eval = ee.evaluate_answer(transcript, question_id)
    
    # Combine scores
    combined_score = {
        'content': content_eval['overall'],
        'voice_quality': voice_metrics['confidence'],
        'clarity': voice_metrics['clarity'],
        'fluency': voice_metrics['fluency'],
        'pace': voice_metrics['pace'],
        'filler_words_count': voice_metrics['filler_words']
    }
    
    return jsonify(combined_score)
```

### 7.2 Real-Time Feedback Chatbot

```python
# app/interview_coach.py

class InterviewCoach:
    """Real-time coaching during interviews"""
    
    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline
    
    def analyze_answer_in_progress(self, partial_answer, question):
        """Provide real-time feedback while user is answering"""
        
        # Check coverage of expected topics
        expected_keywords = question.get('expected_keywords', [])
        covered = [kw for kw in expected_keywords if kw.lower() in partial_answer.lower()]
        missing = [kw for kw in expected_keywords if kw.lower() not in partial_answer.lower()]
        
        feedback = {
            'progress': len(covered) / len(expected_keywords) * 100 if expected_keywords else 0,
            'covered_topics': covered,
            'missing_topics': missing,
            'next_to_cover': missing[0] if missing else None
        }
        
        return feedback
    
    def provide_followup_questions(self, answer, original_question):
        """Generate follow-up questions based on answer"""
        
        prompt = f"""
        Based on this interview answer, generate 2-3 follow-up questions to deepen understanding:
        
        Original Question: {original_question}
        Candidate's Answer: {answer}
        
        Generate questions that:
        1. Test edge cases not mentioned
        2. Probe for deeper expertise
        3. Challenge assumptions made
        """
        
        followups = self.rag.query_with_openai(prompt)
        return followups
    
    def suggest_improvements(self, answer, expected_structure):
        """Suggest how to improve current answer"""
        
        prompt = f"""
        The candidate gave this answer: "{answer}"
        
        For this type of question, the ideal structure includes:
        {expected_structure}
        
        What's missing or could be improved?
        """
        
        suggestions = self.rag.query_with_openai(prompt)
        return suggestions
```

### 7.3 Company-Wise Difficulty Levels

```python
# app/difficulty_adapter.py

class DifficultyAdapter:
    """Adapt questions based on company difficulty"""
    
    COMPANY_DIFFICULTY_MAP = {
        'Google': 5,
        'Microsoft': 4,
        'Amazon': 4,
        'Facebook': 4,
        'Apple': 5,
        'TCS': 2,
        'Infosys': 2,
        'Accenture': 2,
        'JP Morgan': 4,
        'Goldman Sachs': 5
    }
    
    DIFFICULTY_ADJUSTMENTS = {
        1: "Focus on fundamentals and basic concepts",
        2: "Cover fundamentals + practical applications",
        3: "Mix of practical and advanced concepts",
        4: "Advanced concepts and edge cases",
        5: "Expert-level problem solving and system design"
    }
    
    def adjust_question_difficulty(self, base_question, company, target_level=None):
        """Adapt existing question to company difficulty"""
        
        if target_level is None:
            target_level = self.COMPANY_DIFFICULTY_MAP.get(company, 3)
        
        adjustment_prompt = f"""
        Adjust this interview question from difficulty 3 to difficulty {target_level}:
        
        Original Question: {base_question}
        
        Company: {company}
        Difficulty Level: {target_level}/5
        Guidance: {self.DIFFICULTY_ADJUSTMENTS[target_level]}
        
        Provide adjusted question appropriate for {target_level}/5 difficulty.
        """
        
        # Use LLM to adjust
        adjusted = self._call_llm(adjustment_prompt)
        return adjusted
    
    def get_company_interview_pattern(self, company):
        """Retrieve interview patterns for company"""
        
        # This would query external data or cached data
        patterns = {
            'Google': {
                'rounds': 4,
                'avg_duration': '4-5 hours',
                'focus': ['System Design', 'Algorithms', 'Behavioral'],
                'difficulty': 5,
                'acceptance_rate': '0.2%'
            },
            'TCS': {
                'rounds': 3,
                'avg_duration': '2-3 hours',
                'focus': ['SQL', 'Basic Coding', 'Aptitude'],
                'difficulty': 1.5,
                'acceptance_rate': '15%'
            }
        }
        
        return patterns.get(company, {})
```

### 7.4 Analytics Dashboard

```python
# New endpoint: GET /api/placement/analytics

@placement_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Comprehensive performance analytics"""
    email = session.get('user_email')
    
    analytics = {
        'interview_timeline': get_performance_timeline(email),
        'company_comparison': get_company_wise_scores(email),
        'topic_mastery': get_topic_performance(email),
        'prediction': predict_success_probability(email),
        'peer_benchmark': get_anonymous_peer_benchmark(email),
        'improvement_rate': calculate_improvement_rate(email),
        'recommended_focus': get_focus_recommendations(email)
    }
    
    return jsonify(analytics)
```

---

## QUICK START: Phase 1 Implementation Checklist

### Day 1

- [ ] Create 6 new database tables
- [ ] Build `resume_intelligence.py` (300-400 lines)
- [ ] Build `/placement/dashboard` page
- [ ] Build `/placement/resume-analysis` page
- [ ] Build 2 API routes for resume

### Day 2

- [ ] Seed companies table (50 companies)
- [ ] Build `question_engine.py` (400-500 lines)
- [ ] Build `/placement/company-select` page
- [ ] Build `/placement/practice` page
- [ ] Build 4 API routes for questions & sessions

### Day 3

- [ ] Build `evaluation_engine.py` (300-400 lines)
- [ ] Build `roadmap_generator.py` (300-400 lines)
- [ ] Build `/placement/feedback` page
- [ ] Build `/placement/roadmap` page
- [ ] Build 4 API routes for evaluation & roadmap

**Total code to write: ~2000-2500 lines (very manageable for hackathon)**

---

## KEY PROMPTS FOR LLM INTEGRATION

All 4 main prompts are provided in Section 3. Copy-paste these directly into your code.

---

## DEPLOYMENT CHECKLIST

- [ ] Test complete workflow end-to-end
- [ ] Optimize database queries
- [ ] Add error handling and logging
- [ ] Load test with 50+ concurrent users
- [ ] Seed comprehensive company database
- [ ] Configure caching for LLM responses
- [ ] Test LLM fallback (OpenAI → Gemini)
- [ ] Setup monitoring and alerting

---

## ESTIMATED TOKENS/COSTS

**Per Interview Session (10 questions):**
- Resume Analysis: ~2,000 tokens
- Question Generation: ~8,000 tokens
- 10x Answer Evaluation: ~15,000 tokens
- Roadmap Generation: ~5,000 tokens
- **Total: ~30,000 tokens ≈ $0.15-0.30 per session**

**Recommendation:** Cache frequently generated content + use Gemini for non-critical tasks

---

This architecture is production-ready and hackathon-optimized. Start with Phase 1 (3 days) and you'll have a fully functional AI Placement Assistant!
