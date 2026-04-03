# StudyBuddy - AI Learning and Resource Platform

**StudyBuddy** is a Flask-based AI-powered learning platform that provides intelligent tutoring, collaborative resource sharing, AI-powered note generation, YouTube transcript analysis, resume evaluation, progress tracking, and comprehensive admin tools. Built with dual-LLM support (OpenAI + Google Gemini) for maximum uptime and cost efficiency.

## What Is Live Now

✅ **AI Chatbot System**
- Multi-LLM support: OpenAI GPT-4o-mini with automatic Gemini fallback
- Intelligent RAG (Retrieval-Augmented Generation) from local knowledge-base
- Comprehensive prompt injection protection
- Chat history with pagination and deletion
- Optional speech synthesis

✅ **Learning Features**
- Instant Note Maker with AI-powered content generation, PDF export, and resource submission
- Resume upload and intelligent analysis (PDF/DOCX support)
- Skill checklist tracking with progress visualization
- Mock test creation and performance tracking
- Progress tracker with habits, velocity metrics, and engagement scoring
- Leaderboard for competitive learning

✅ **Resource Management**
- Resource upload with content deduplication (prevents duplicates)
- Review workflow with admin approval queue
- Advanced filtering, preview, and download capabilities
- Resource comments and threaded discussions
- AI-powered refinement (summaries, Q&A generation, mindmaps)

✅ **Admin Tools**
- User management (view, edit, delete, analytics)
- Resource moderation dashboard with pending approvals pagination (3 per page)
- Live resources management with edit/delete capabilities
- Database explorer and SQL console
- Statistics and analytics dashboard

✅ **Authentication & User Management**
- Secure registration and login with email validation
- Password reset with token-based security
- Onboarding flow for new users
- Optional SMTP for email notifications

✅ **Knowledge Base System**
- Auto-loaded knowledge-base with 5 JSON files (40,656+ characters)
- Structured data: courses, assessments, certifications, learning paths, progress metrics
- API endpoints for KB management and refinement

## Core Features

### Authentication & Security
- User registration with email validation
- Secure login with session management
- Password reset flow with token-based security
- Prompt injection detection and prevention
- CSRF protection through secret key configuration

### AI Chatbot (Dual-LLM)
- **Primary:** OpenAI GPT-4o-mini for high-quality responses
- **Fallback:** Google Gemini (free tier) when OpenAI quota exceeded
- RAG (Retrieval-Augmented Generation) context from knowledge base
- Knowledge-aware responses with structured learning content
- Optional speech synthesis with fallback error handling
- Comprehensive error handling and user feedback

### Learning & Study Tools
- **Note Maker:** AI-powered content generation, PDF export, resource submission
- **Resume Analyzer:** Parse PDF/DOCX, extract info, provide AI analysis
- **Skill Checklist:** Track learning progress with visual indicators
- **Mock Tests:** Create custom tests, track performance, measure improvement
- **Progress Tracker:** Monitor completion %, velocity, engagement metrics
- **Habits System:** Daily habit tracking with history and logs
- **Leaderboard:** Competitive ranking based on points and engagement

### Resource Management
- Upload resources (PDF, DOCX, links) with metadata
- Content-based deduplication by hash (prevents duplicate uploads)
- Admin approval workflow (pending → approved)
- User-owned resource management (edit/delete own uploads)
- Resource comments and community discussions
- AI-powered refinement: summaries, Q&A generation, mindmap creation
- Pagination support for large resource collections

### Admin Panel
- Complete user management system
- Resource moderation with approval queue
- Database explorer with SQL console
- Analytics and statistics dashboard
- System health monitoring

### Knowledge Base System
- Auto-loaded structured KB with 5 JSON files (40,656+ characters)
- Included: Courses, assessments, certifications, learning paths, progress metrics
- Intent detection for contextual matching
- API endpoints for KB addition and retrieval
- Keyword-based and semantic search

## Tech Stack

- **Backend:** Flask 3.1.3, Python 3.11.9
- **Database:** SQLite with vector table for RAG
- **AI/ML:**
  - OpenAI GPT-4o-mini (primary chatbot LLM)
  - Google Gemini 1.5-flash (free fallback LLM)
  - LangChain for LLM orchestration
  - RAG pipeline with keyword matching & embedding support
- **API Integrations:**
  - Apify API for YouTube transcript extraction
  - youtube-transcript-api as fallback
- **Frontend:**
  - Jinja2 templates (server-side rendering)
  - Vanilla JavaScript (ES6+)
  - Responsive CSS with dark/light theme support
  - Spline 3D for avatar visualization
- **File Processing:**
  - PyPDF2 (PDF reading/writing)
  - python-docx (DOCX document handling)
  - reportlab (PDF generation)
- **Dependencies:**
  - requests (HTTP client)
  - itsdangerous (token serialization)
  - werkzeug (password hashing)
  - python-dotenv (environment configuration)

## Project Layout

```
StudyBuddy/
├── run.py                          # Flask application entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API keys, secrets)
├── README.md                       # Project documentation
├── FEATURE_SUMMARY.md              # Detailed feature documentation
├── RAG_README.md                   # RAG pipeline documentation
│
├── app/                            # Flask application package
│   ├── __init__.py                 # App factory and initialization
│   ├── db.py                       # Database operations (SQLite)
│   ├── routes.py                   # All API endpoints (3000+ lines)
│   ├── rag_pipeline.py             # RAG system & knowledge base logic
│   ├── kb_manager.py               # Knowledge base management
│   ├── email_utils.py              # SMTP/email functionality
│   ├── static/                     # Frontend assets
│   │   ├── css/                    # Stylesheets
│   │   │   ├── styles.css          # Main stylesheet
│   │   │   ├── auth.css            # Authentication pages
│   │   │   ├── admin.css           # Admin panel
│   │   │   ├── resources.css       # Resources module
│   │   │   ├── progress.css        # Progress tracker
│   │   │   └── resume.css          # Resume analyzer
│   │   └── js/                     # JavaScript files
│   │       ├── script.js           # Main application logic
│   │       ├── dashboard-chatbot.js# Chatbot interface
│   │       ├── admin.js            # Admin panel interactions
│   │       ├── resources.js        # Resource management
│   │       ├── resume-analyzer.js  # Resume analyzer UI
│   │       ├── progress-tracker.js # Progress tracking UI
│   │       ├── skill-checklist.js  # Skill checklist UI
│   │       ├── note-maker.js       # Note generation UI
│   │       ├── mock-tests.js       # Mock tests UI
│   │       └── page-transition.js  # Page navigation effects
│   └── templates/                  # Jinja2 HTML templates
│       ├── index.html              # Landing page
│       ├── login.html              # Login page
│       ├── register.html           # Registration page
│       ├── forgot_password.html    # Password recovery
│       ├── reset_password.html     # Password reset
│       ├── onboarding.html         # Onboarding flow
│       ├── dashboard.html          # Main dashboard
│       ├── progress.html           # Progress tracker
│       ├── mock_tests.html         # Mock tests page
│       ├── resume.html             # Resume analyzer
│       ├── note_maker.html         # Note maker page
│       ├── resources.html          # Resources page
│       └── admin.html              # Admin panel
│
├── Knowledge base/                 # Structured learning content (JSON)
│   ├── course_structure.json       # Courses & modules
│   ├── assessments.json            # Quizzes & tests
│   ├── certifications.json         # Certifications
│   ├── learning_paths.json         # Learning journeys
│   └── progress_tracking.json      # Tracking metrics
│
├── data/                           # Runtime data directory
│   ├── preppulse.db                # SQLite database
│   ├── resources/                  # Uploaded resource files
│   └── resumes/                    # Uploaded resume files
│
├── scripts/                        # Utility scripts
│   └── migrate_sqlite_to_postgres.py# Database migration helper
│
└── tests/                          # Test files
    ├── test_api_keys.py            # API configuration tests
    ├── test_kb_refinement.py       # KB system tests
    ├── test_self_learning_kb.py    # Self-learning tests
    └── test_resources_integration.py# Resource integration tests
```

## Setup

### Prerequisites

- Python 3.11+ (tested on 3.11.9)
- pip (Python package manager)
- **Required APIs:**
  - OpenAI API key (get free trial credits at https://platform.openai.com/api-keys)
  - Google Gemini API key (100% free at https://makersuite.google.com/app/apikey)
- **Optional APIs:**
  - Apify API token for enhanced YouTube transcript extraction
  - SMTP credentials for email notifications (optional)

### Install

```bash
# Clone the repository
git clone <repo-url>
cd StudyBuddy

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with the following configuration:

```env
# ============================================
# SECURITY & CONFIG
# ============================================
SECRET_KEY=your-random-secret-key-here
RESET_TOKEN_MAX_AGE=900

# ============================================
# AI/LLM CONFIGURATION (REQUIRED)
# ============================================
# OpenAI - Get free trial at: https://platform.openai.com/api-keys
OPEN_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# Google Gemini (FREE!) - Get at: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=AIzaSyBbGjqMlxpi-Ts1Ri2hcY39CC-ww5_1XEM
GEMINI_MODEL=gemini-1.5-flash

# ============================================
# EMAIL CONFIGURATION (OPTIONAL)
# ============================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

# ============================================
# EXTERNAL APIs (OPTIONAL)
# ============================================
# Apify - Get at: https://console.apify.com
APIFY_API_TOKEN=optional-apify-token
APIFY_YOUTUBE_ACTOR_ID=pintostudio~youtube-transcript
```

**⚠️ SECURITY NOTICE:**
- Never commit `.env` to version control
- Keep API keys private and secure
- Use different keys for development and production
- Rotate keys periodically
- `.env` is included in `.gitignore` for safety

**🎉 Getting Started Quickly:**
1. Get OpenAI key: https://platform.openai.com/api-keys
2. Get Gemini key (free!): https://makersuite.google.com/app/apikey
3. Add both keys to `.env`
4. Run `python run.py`
5. Visit http://localhost:5000

### Run Locally

```bash
# Start the Flask development server
python run.py
```

The application will start on: **http://127.0.0.1:5000**

**First Run:**
- The database (`preppulse.db`) will be created automatically
- Knowledge base files will be loaded from `Knowledge base/` directory
- RAG pipeline will initialize with 40,656+ characters of content
- All 12+ HTML templates will be ready

**Debug Mode:**
- Flask debug mode is enabled for development
- Auto-reload on file changes
- Flask debugger PIN displayed in terminal

## Main Routes and APIs

### Pages

- GET /
- GET or POST /login
- GET or POST /register
- GET or POST /forgot-password
- GET or POST /reset-password/<token>
- GET or POST /onboarding
- GET /dashboard
- GET /progress
- GET /mock-tests
- GET /resume
- GET /note-maker
- GET /resources

- GET /admin

### Chat

- POST /chat
- GET /api/chat-history
- DELETE /api/chat-history/delete
- DELETE /api/chat-history/<message_id>

### Notes

- POST /api/notes/generate
- POST /api/notes/create-pdf
- POST /api/notes/upload-to-resources

### Resources (User)

- GET /api/resources
- GET /api/resources/mine
- POST /api/resources/upload
- PUT /api/resources/<resource_id>
- DELETE /api/resources/<resource_id>
- GET /api/resources/<resource_id>/download
- GET /api/resources/<resource_id>/comments
- POST /api/resources/<resource_id>/refine
- GET /api/resources/<resource_id>/refinement

### Resources (Admin)

- GET /api/admin/resources/pending?page=1&page_size=3
- GET /api/admin/resources/live?page=1&page_size=5
- GET /api/admin/resources/stats
- PUT /api/admin/resources/<resource_id>/approve
- PUT /api/admin/resources/<resource_id>/reject
- PUT /api/admin/resources/<resource_id>
- DELETE /api/admin/resources/<resource_id>
- POST /api/admin/resources/<resource_id>/comment
- GET /api/admin/resources/<resource_id>/comments



### Resume

- POST /api/resume/upload
- POST /api/resume/analyze
- GET /api/resume/latest
- GET /api/resume/file/<resume_id>
- GET /api/resume/file

### Progress and Tests

- GET or POST /api/mock-tests
- PUT or DELETE /api/mock-tests/<test_id>
- GET or POST /api/habits
- PUT or DELETE /api/habits/<habit_id>
- POST /api/habits/toggle
- GET /api/habits/logs
- GET /api/leaderboard

### Knowledge Base Management

- POST /api/kb/add-course
- POST /api/kb/add-assessment
- POST /api/kb/add-certification
- GET /api/kb/search
- GET /api/kb/status

## Project Status

### ✅ Completed Features (95% Ready)

**Core Infrastructure:**
- ✅ Flask application running on `http://localhost:5000`
- ✅ SQLite database with vector tables for RAG
- ✅ Virtual environment fully configured
- ✅ All 24 dependencies installed

**AI & Chatbot System:**
- ✅ OpenAI GPT-4o-mini integration (primary LLM)
- ✅ Google Gemini 1.5-flash integration (free fallback)
- ✅ Automatic LLM failover when API quota exceeded
- ✅ RAG pipeline with knowledge base retrieval
- ✅ Prompt injection detection & prevention
- ✅ Error handling with graceful degradation

**Student Features:**
- ✅ AI Chatbot with chat history
- ✅ Note Maker with PDF export
- ✅ Resume Analyzer (PDF/DOCX support)
- ✅ Skill Checklist tracking
- ✅ Mock Tests with scoring
- ✅ Progress Tracker with metrics
- ✅ Habits system with daily logs
- ✅ Leaderboard with rankings

**Resource Management:**
- ✅ Upload & manage resources
- ✅ Admin approval workflow
- ✅ Resource deduplication
- ✅ Comments and discussions
- ✅ AI-powered refinement
- ✅ Resource search & filtering

**Admin Tools:**
- ✅ User management (view, edit, delete)
- ✅ Resource moderation dashboard
- ✅ Database explorer & SQL console
- ✅ Analytics & statistics
- ✅ User activity monitoring

**Frontend:**
- ✅ 12+ responsive HTML templates
- ✅ Complete StudyBuddy branding (27+ replacements)
- ✅ Vanilla JavaScript interactivity
- ✅ CSS animations & transitions
- ✅ Mobile-friendly design

### ⏳ Optional Features (Not Critical)

- SMTP Email configuration (optional password resets)
- Database migration to PostgreSQL (script available)
- API rate limiting (can add later)
- Performance optimization (caching, indexing)
- Production deployment configuration

## Quick Start Guide

### 1. Get Your API Keys (2 minutes)

**OpenAI (Free Trial):**
1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key starting with `sk-proj-`

**Google Gemini (100% Free):**
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy your Gemini API key

### 2. Setup Your Project

```bash
# Clone and enter directory
git clone <repo-url>
cd StudyBuddy

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure .env File

```env
OPEN_API_KEY=sk-proj-YOUR_KEY_HERE
GEMINI_API_KEY=YOUR_GEMINI_KEY_HERE
SECRET_KEY=your-secret-key-12345
```

### 4. Start the Application

```bash
python run.py
```

Visit: http://localhost:5000

## Testing Checklist

- [ ] Register a new account
- [ ] Login with test credentials
- [ ] Ask chatbot a question (uses Gemini if OpenAI fails)
- [ ] Upload a PDF to resources
- [ ] Create a mock test
- [ ] Generate notes from a topic
- [ ] Check skill checklist progress
- [ ] View leaderboard
- [ ] Test admin panel (create another admin account manually)

## AI System Architecture

```
User Message
    ↓
Prompt Injection Check → Block if suspicious
    ↓
Try OpenAI API
    ↓
    ├─ Success? → Return response
    └─ Fail? → Try Gemini (fallback)
        ↓
        ├─ Gemini Success? → Return response with * note
        └─ Both Fail? → Return helpful error message

RAG Context:
    ↓
Knowledge Base (40,656+ chars)
    ├─ Course Structure
    ├─ Assessments
    ├─ Certifications
    ├─ Learning Paths
    └─ Progress Metrics
```

## Troubleshooting

### "StudyBuddy AI is temporarily unavailable"

This means both OpenAI and Gemini APIs failed. Check:

1. **Internet Connection:** Ensure you're connected
2. **API Keys:** Verify keys in `.env` are correct
3. **API Status:**
   - OpenAI: https://status.openai.com
   - Google: https://status.cloud.google.com
4. **Quota:** Check your API usage in respective dashboards

### Chat responses show errors

- **OpenAI Quota (429):** The fallback system will use Gemini
- **API Key Invalid (401):** Update `.env` and restart
- **Network Error:** Check internet connection and firewall

### Database Issues

The database is auto-created on first run. If you encounter issues:

```bash
# Delete the old database
rm data/preppulse.db

# Restart the application (creates fresh DB)
python run.py
```

## Deployment

StudyBuddy is ready for production deployment. Options:

1. **Heroku:** `git push heroku main`
2. **Railway.app:** Connect your GitHub repo
3. **AWS/GCP:** Use Docker containerization
4. **DigitalOcean:** Deploy with App Platform

Add production environment variables before deploying:

```env
DEBUG=False
FLASK_ENV=production
SECRET_KEY=<generate-new-strong-key>
```

## Documentation

- [FEATURE_SUMMARY.md](FEATURE_SUMMARY.md) - Detailed feature documentation
- [RAG_README.md](RAG_README.md) - RAG and knowledge base system
- [KB_REFINEMENT.md](KB_REFINEMENT.md) - Knowledge base refinement guide

## Notes for Maintainers

- Database path: `data/preppulse.db` (auto-created)
- RAG pipeline initializes during app startup: Loads 40,656+ chars
- Knowledge base files must be valid JSON in `Knowledge base/` directory
- To update knowledge base: Modify JSON files and restart app
- Chat endpoints: All stored in `/chat` and `/api/chat-*` routes
- Admin panel: Accessible at `/admin` (requires admin account)

## License

Built for a hackathon and ongoing internal development.
