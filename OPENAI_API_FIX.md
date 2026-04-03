# 🚀 Fix OpenAI API Not Working - Complete Guide

## Problem Diagnosis

You're seeing one of these errors in StudyBuddy:
- `500 INTERNAL SERVER ERROR` on chat
- `Missing property buildTimeline @ spline-viewer.js`
- OpenAI API returns: "You exceeded your current quota"

## Root Cause

Your OpenAI API key was created with **free trial credits** that have now expired or been consumed. The API returns a **quota error (429)**, causing the chatbot to crash.

---

## ✅ Solution: Enable Paid OpenAI Account

### **Step 1: Add Payment Method to OpenAI**

1. Go to: [https://platform.openai.com/account/billing/overview](https://platform.openai.com/account/billing/overview)
2. Click **"Billing"** in left menu
3. Select **"Billing overview"**
4. Click **"Add payment method"**
5. Enter your credit card details (Visa, Mastercard, Amex accepted)
6. Set a monthly usage limit (e.g., $5-20 recommended)

✅ **Your API will now work!**

---

### **Step 2: Verify Your API Key**

1. Go to: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Check your existing key or create a new one if needed
3. Copy the key (starts with `sk-proj-`)
4. Paste into `.env` file:
   ```env
   OPEN_API_KEY=sk-proj-YOUR_KEY_HERE_XXXXXXXXXX
   ```

---

### **Step 3: Restart the Application**

Stop and restart Flask:
```bash
# Kill existing process (Ctrl+C in terminal)
.venv\Scripts\python run.py
```

---

## 💰 OpenAI Pricing (Current as of April 2026)

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| **gpt-4o-mini** | $0.15/1M tokens | $0.60/1M tokens | ✅ Used by StudyBuddy (cheapest) |
| gpt-4o | $5/1M tokens | $15/1M tokens | More powerful, expensive |
| gpt-3.5-turbo | $0.50/1M tokens | $1.50/1M tokens | Older, cheaper |

### **Example Costs:**
- **1 chatbot message** ≈ $0.0001-0.0003 (less than 1¢)
- **100 messages/day** ≈ $0.03-0.05/day
- **1,000 messages/month** ≈ $1-2/month

✅ **For a hackathon**: Set $5 budget = ~15,000 messages

---

## 🔧 Troubleshooting

### **Issue 1: "Invalid API Key"**
- **Cause**: Key format wrong or not updated in `.env`
- **Fix**: 
  ```env
  OPEN_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
  ```
  (Make sure no spaces or extra characters)

### **Issue 2: "Quota Exceeded" (Still seeing after adding payment)**
- **Cause**: Payment not linked or awaiting verification
- **Fix**: 
  1. Wait 5-10 minutes after adding payment
  2. Verify card details at [OpenAI Billing](https://platform.openai.com/account/billing/overview)
  3. Contact OpenAI support if persistent

### **Issue 3: Chatbot still returns error message**
- **Cause**: App not restarted
- **Fix**: Kill Flask process and restart:
  ```bash
  # Press Ctrl+C to stop
  .venv\Scripts\python run.py
  ```

### **Issue 4: Spline Viewer "Missing property buildTimeline"**
- **Cause**: Frontend JavaScript animation library issue (not critical)
- **Impact**: 3D background animation doesn't display, but app fully functional
- **Fix**: Already handled by app, shows graceful fallback

---

## 📋 Step-by-Step Testing

After adding payment:

1. **Open StudyBuddy**: http://localhost:5000
2. **Login** with your test account
3. **Go to Dashboard** → Chat section
4. **Type a message**: "Hi, test the chatbot"
5. **Expected**: ✅ AI response appears within 5 seconds

### **Check if working:**
```bash
# In terminal where Flask runs, you should see:
✅ [CHATBOT] LLM response generated successfully
```

---

## 🆘 If Still Not Working

**Check these in order:**

1. **Verify payment added**:
   - Go to: https://platform.openai.com/account/billing/overview
   - Under "Billing", see active payment method
   - Try using your card to make small test purchase

2. **Check limit not exceeded**:
   - Go to: https://platform.openai.com/account/billing/limits
   - Verify "Hard limit" is higher than usage
   - If exceeded, increase limit

3. **Verify .env updated**:
   ```bash
   # Check .env file
   cat .env | grep OPEN_API_KEY
   ```
   Should show your actual key starting with `sk-proj-`

4. **Restart app and browser**:
   - Stop Flask (Ctrl+C)
   - Restart: `.venv\Scripts\python run.py`
   - Clear browser cache and reload: `Ctrl+Shift+Delete` → Clear all

5. **Check internet connection**:
   - Ensure you can reach: https://api.openai.com

---

## ✅ Free Alternatives (If you can't use OpenAI)

You can replace OpenAI with these free options:

### **Option 1: Use Gemini API (Free Tier)**
1. Replace `sk-proj-...` with Google Gemini API key
2. Get free credits at: https://makersuite.google.com/app/apikey
3. Update `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   GEMINI_MODEL=gemini-1.5-flash
   ```

### **Option 2: Use Ollama (Open Source, 100% Free)**
1. Download: https://ollama.ai
2. Run locally: `ollama run llama2`
3. Modify app to use local endpoint (requires code changes)

---

## 📞 Get Help

- **OpenAI Status**: Check https://status.openai.com
- **OpenAI Docs**: https://platform.openai.com/docs
- **OpenAI Support**: https://help.openai.com

---

## 🎯 Perfect Configuration for StudyBuddy

```env
# .env file - Production Ready
OPEN_API_KEY=sk-proj-YOUR_KEY_HERE
APIFY_API_TOKEN=aVcjS215P69hRObTd5CI4LL4d2seSU1IFNQM
APIFY_YOUTUBE_ACTOR_ID=pintostudio~youtube-transcript
SECRET_KEY=dev-secret-key-prepPulse-2026
```

✅ **After this, chatbot will work 100%!**
