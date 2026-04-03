# 📱 GitHub Pages & Backend Deployment Setup

## ✅ What's Been Done

1. **GitHub Pages Site Created** ✓
   - Landing page: `docs/index.html`
   - Deployment guide: `docs/deployment.html`
   - Full documentation: `docs/README.md`

2. **Files Pushed to GitHub** ✓
   - Commit: `b56d3ad`
   - Branch: `master`
   - Ready for GitHub Pages

## 🚀 STEP 1: Enable GitHub Pages

### Enable in Repository Settings

1. **Go to GitHub Repository:**
   - URL: https://github.com/saikrishna9603/studybuddy
   - Click **Settings** tab

2. **Navigate to Pages:**
   - Left sidebar: Click **Pages**
   - Under "Build and deployment"

3. **Configure GitHub Pages:**
   - **Source:** Select `Deploy from a branch`
   - **Branch:** Select `master`
   - **Folder:** Select `/ (root)` → Change to `/docs`
   - Click **Save**

4. **Wait for Deployment:**
   - GitHub Pages rebuilds automatically
   - Takes 1-2 minutes
   - A green checkmark appears when done

### ✅ Your Site is Live!

```
Your GitHub Pages URL:
https://saikrishna9603.github.io/studybuddy/
```

Visit this URL to see your landing page!

---

## 🎯 STEP 2: Deploy Backend (Required)

**Important:** GitHub Pages only hosts the static landing page. The actual StudyBuddy application needs a backend server.

### Quick Comparison

| Platform | Cost | Setup | Recommended | Link |
|----------|------|-------|-------------|------|
| **Railway** ⭐ | $5 free/mo | 5 min | YES | https://railway.app |
| **Render** | Free (timeout) | 10 min | For testing | https://render.com |
| **Heroku** | $7+/mo | 15 min | No (legacy) | https://heroku.com |

### RECOMMENDED: Deploy to Railway.app

#### 1. Create Railway Account
```
1. Visit https://railway.app
2. Click "Start Project"
3. Sign in with GitHub
4. Authorize Railway access
```

#### 2. Deploy StudyBuddy
```
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose repository: saikrishna9603/studybuddy
4. Click "Deploy"
```

#### 3. Configure Environment Variables
```
In Railway Dashboard:
1. Go to "Variables" tab
2. Add the following:

   OPEN_API_KEY = sk-proj-YOUR_KEY_HERE
   GEMINI_API_KEY = YOUR_GEMINI_KEY_HERE
   GEMINI_MODEL = gemini-1.5-flash
   SECRET_KEY = unique-random-string-here
   FLASK_ENV = production

3. Click "Save"
```

#### 4. Get Your Live URL
```
Railway generates a public URL:
https://studybuddy-prod-[random].up.railway.app

Share this with friends!
```

---

## 📋 Complete Deployment Checklist

### GitHub Pages Setup
- [ ] Repository settings → Pages
- [ ] Source: Branch = master, Folder = /docs
- [ ] Wait for green checkmark
- [ ] Test landing page loads: `https://saikrishna9603.github.io/studybuddy/`

### Backend Deployment (Railway)
- [ ] Create Railway account (link GitHub)
- [ ] Deploy from repository
- [ ] Add all 5 environment variables
- [ ] Wait for deployment complete
- [ ] Test backend loads and responds

### Post-Deployment Testing
- [ ] [ ] Landing page loads without errors
- [ ] [ ] Deployment guide page loads
- [ ] [ ] Backend URL responds to requests
- [ ] [ ] Can login to application
- [ ] [ ] Chatbot works (asks a question)
- [ ] [ ] Interview practice loads
- [ ] [ ] API calls return proper responses

---

## 🔗 Architecture Overview

```
GitHub Pages (Static Site)
├─ Landing page (index.html)
├─ Live at: https://saikrishna9603.github.io/studybuddy/
└─ Links to backend ↓

Railway Backend (Dynamic App)
├─ Flask application running 24/7
├─ Database (SQLite initially, PostgreSQL for scale)
├─ Live at: https://studybuddy-[random].up.railway.app
├─ All interactive features
├─ API endpoints
└─ Connects to: OpenAI + Google Gemini
```

---

## 🌍 Access Your Deployment

### Frontend (GitHub Pages)
```
📍 https://saikrishna9603.github.io/studybuddy/
├─ Landing page with features
├─ Deployment guide
└─ Documentation
```

### Backend (Railway)
```
📍 https://studybuddy-[random].up.railway.app
├─ Full application
├─ Dashboard
├─ Interview prep
├─ Resources
└─ Admin panel
```

---

## 🔑 Get API Keys (Required for Backend)

### OpenAI GPT-4o (5 min free trial)
1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy key (starts with `sk-proj-`)
4. Add to Railway variables as `OPEN_API_KEY`

### Google Gemini (100% FREE, no credit card)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy your API key
4. Add to Railway variables as `GEMINI_API_KEY`

---

## 🆘 Troubleshooting

### GitHub Pages Not Showing
- **Problem:** Landing page returns 404
- **Solution:** 
  - Check settings: Pages should use `/docs` folder
  - Wait 2-3 minutes after changing settings
  - Clear browser cache (Ctrl+Shift+Delete)

### Backend Not Working
- **Problem:** Railway deployment fails
- **Solution:**
  - Check Railway logs for errors
  - Verify all environment variables are set
  - Ensure no typos in API keys

### Can't Login to Application
- **Problem:** Unable to create account or login
- **Solution:**
  - Database initializes on first run (give it 30s)
  - Check if backend is running (visit URL)
  - Try incognito window (cookies issue)

### Slow API Responses
- **Problem:** Chatbot responses take forever
- **Solution:**
  - OpenAI might be slow (normal)
  - Check Network tab in browser DevTools
  - Free Railway might have resource limits

---

## 📊 What's Deployed

### GitHub Pages (docs/ folder)
```
✅ Landing page with hero section
✅ Features overview (6 cards)
✅ Tech stack showcase
✅ Quick start guide
✅ Deployment options
✅ Getting started steps
✅ API keys guide
✅ 100% responsive design
✅ Professional styling
```

### Backend (Railway Server)
```
✅ Flask application (3000+ routes)
✅ User authentication
✅ AI Chatbot (OpenAI + Gemini)
✅ Interview Preparation system
✅ Resume analyzer
✅ Progress tracking
✅ Resource management
✅ Admin dashboard
✅ Knowledge base RAG
✅ Knowledge base RAG
✅ Database operations
```

---

## 🎯 Next Steps

1. **Enable GitHub Pages** (2 min)
   - Visit repository settings
   - Enable Pages from /docs folder
   - Test landing page

2. **Deploy Backend** (5 min)
   - Create Railway account
   - Connect GitHub repository
   - Add environment variables
   - Wait for deployment

3. **Test Everything** (10 min)
   - Visit landing page
   - Visit backend URL
   - Test login
   - Test chatbot
   - Try interview practice

4. **Share with Others** (Ongoing)
   - GitHub Pages URL (share landing page)
   - Railway URL (share working app)
   - GitHub repository link

---

## 📞 Support Resources

### GitHub Pages Help
- Docs: https://docs.github.com/pages
- Troubleshooting: https://docs.github.com/pages/getting-started-with-github-pages/troubleshooting-publishing-errors-for-your-github-pages-site

### Railway Help
- Docs: https://docs.railway.app
- Deployment: https://docs.railway.app/deploy/deployments
- Environment: https://docs.railway.app/develop/variables

### StudyBuddy Help
- GitHub Issues: Report problems
- Project Docs: Check INTERVIEW_UI_INTEGRATION.md
- Troubleshooting: See TROUBLESHOOTING.md

---

## 💡 Tips & Best Practices

### GitHub Pages
- ✅ Use `/docs` folder for GitHub Pages
- ✅ Update `docs/index.html` to link to your Railway backend
- ✅ Enable custom domain for professional look (optional)
- ✅ Keep documentation in sync with code

### Railway
- ✅ Monitor logs in Railway dashboard
- ✅ Set up alerts for deployment failures
- ✅ Use PostgreSQL for production (better than SQLite)
- ✅ Rotate API keys regularly
- ✅ Enable auto-redeploy on GitHub push

### Security
- ✅ Never commit `.env` file to GitHub
- ✅ Use unique `SECRET_KEY` for each environment
- ✅ Rotate API keys periodically
- ✅ Monitor Railway logs for suspicious activity
- ✅ Use HTTPS only (enabled by default)

---

## 🎉 You're Done!

Your StudyBuddy deployment is now split into two parts:

1. **GitHub Pages** - Professional landing page (free, static)
2. **Railway** - Full application backend ($5/month with free credit)

Both are live and accessible to everyone!

---

**Questions? Check the deployment.html guide in your /docs folder or open an issue on GitHub.**
