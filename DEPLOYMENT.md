# Aerulias AI - Deployment Guide

## 🚀 Quick Start: Deploy to Render.com

This guide walks you through deploying the Aerulias AI application to Render.com for free (free tier available).

---

## Prerequisites

- ✅ GitHub account (free)
- ✅ Render.com account (free tier available at https://render.com)
- ✅ OpenRouter API Key (get free credits at https://openrouter.ai)

---

## Step 1: Push Code to GitHub

### 1.1 Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `aerulias-ai`
3. Do NOT initialize with README/gitignore (we'll push existing code)
4. Click "Create repository"

### 1.2 Push Your Code

In your terminal (in the `aerulias_ai` directory):

```bash
git init
git add .
git commit -m "Initial commit: Aerulias AI production-ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aerulias-ai.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 2: Create Render Service

### 2.1 Connect GitHub to Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect account"** next to GitHub
4. Authorize Render to access GitHub
5. Select the `aerulias-ai` repository
6. Click **"Connect"**

### 2.2 Configure Service

Fill in the following details:

| Field | Value |
|-------|-------|
| **Name** | `aerulias-ai` |
| **Environment** | `Python 3` |
| **Region** | `(closest to you)` |
| **Branch** | `main` |
| **Build Command** | (auto-detected from render.yaml) |
| **Start Command** | (auto-detected from render.yaml) |
| **Plan** | `Free` (or Starter for better performance) |

### 2.3 Add Environment Variables

**IMPORTANT:** Before clicking "Deploy", add the following environment variables:

1. Click **"Advanced"** → **"Add Environment Variable"**

2. Add these variables:

   | Key | Value | Notes |
   |-----|-------|-------|
   | `OPENROUTER_API_KEY` | `[Your OpenRouter API Key]` | **REQUIRED** - Get from https://openrouter.ai/keys |
   | `OPENROUTER_SITE_URL` | `https://aerulias-ai-xxxx.onrender.com` | Will be created after deploy - update this after |
   | `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` | Default - usually correct |
   | `OPENROUTER_MODEL` | `openai/gpt-4o-mini` | Model to use (free tier friendly) |
   | `OPENROUTER_APP_NAME` | `aerulias_ai` | App identifier |
   | `PYTHONUNBUFFERED` | `1` | Enables real-time logging |
   | `LOG_LEVEL` | `info` | Logging verbosity |

### 2.4 Get Your OpenRouter API Key

1. Go to https://openrouter.ai
2. Sign up (free)
3. Go to **Settings** → **"API Keys"**
4. Copy your API key
5. Paste it in the `OPENROUTER_API_KEY` field in Render

### 2.5 Deploy

1. Click **"Create Web Service"**
2. Render will start building (takes 2-3 minutes)
3. Watch the build log for errors
4. Once live, you'll get a URL like: `https://aerulias-ai-xxxx.onrender.com`

---

## Step 3: Update OPENROUTER_SITE_URL (Important!)

After deployment completes:

1. Copy your Render URL (visible in dashboard)
2. Go back to **Environment** settings in Render
3. Update `OPENROUTER_SITE_URL` to your Render URL
4. Click **"Save"**
5. Service will auto-redeploy with updated URL

---

## Step 4: Verify Deployment

Once the deployment is live:

1. Open your Render URL in browser: `https://aerulias-ai-xxxx.onrender.com`
2. You should see the Aerulias AI dashboard

### Test the Application

1. **Fill the form:**
   - Query: "What is machine learning?"
   - Rounds: 2
   
2. **Click "Run Pipeline"**

3. **Verify Success:**
   - ✅ Spinner appears briefly
   - ✅ Results populate in the "Answer" panel
   - ✅ Metrics appear below (Quality Score, Time, Tokens)
   - ✅ Flow visualization shows agent steps
   - ✅ Analytics tab populates with chart data

### Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| **Blank white page** | Wait 30 seconds, refresh. Check browser console (F12) for errors. |
| **"Service is starting" message** | Free tier services sleep after 15 min inactivity. Wait 30-60 seconds, refresh. |
| **API error / No response** | Check that `OPENROUTER_API_KEY` is set correctly. Verify it in Render dashboard. |
| **502 Bad Gateway** | Check Render logs (bottom of dashboard). Service may be restarting. |
| **Deployment failed** | Click "Logs" tab. Look for Python errors. Common: missing dependencies (check requirements.txt). |

### View Production Logs

To debug issues in production:

1. In Render dashboard, click your service
2. Scroll down to **"Logs"** section
3. Search for error keywords or timestamps
4. Common log patterns:
   - `ERROR` - Something went wrong
   - `INFO` - Normal operation
   - `WARNING` - Non-critical issue

---

## Features Available

Once deployed, you can:

- ✅ **Run Pipeline** - Generate and refine answers
- ✅ **Analytics Tab** - View charts and metrics
- ✅ **Compare Tab** - Compare multiple runs
- ✅ **Export** - Download as JSON/CSV/HTML
- ✅ **Dark Mode** - Toggle theme (Ctrl+D)
- ✅ **Settings** - Configure API timeout
- ✅ **Memory/History** - View past queries and results
- ✅ **Keyboard Shortcuts:**
  - `Ctrl+E` - Focus query input
  - `Ctrl+Enter` - Run pipeline
  - `Ctrl+D` - Toggle dark mode
  - `Ctrl+S` - Open settings

---

## Managing Your Deployment

### Updating Code

After pushing changes to GitHub:

1. Render automatically detects push to `main` branch
2. Service redeploys automatically (~2-3 minutes)
3. Check "Deployments" tab to track status

### Monitoring Performance

- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- For production 24/7 uptime, upgrade to Starter plan

### Troubleshooting

**Common Issues:**

1. **Service keeps crashing:**
   - Check logs for Python errors
   - Verify all env vars are set
   - Ensure requirements.txt has all dependencies

2. **API not responding:**
   - Verify OpenRouter API key is valid
   - Check OpenRouter account has credits
   - Look for rate limiting errors in logs

3. **Frontend shows old version:**
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Clear browser cache

---

## Production Checklist

Before considering deployment "complete":

- [ ] Dashboard loads without errors
- [ ] Can run a test pipeline
- [ ] Results display correctly
- [ ] Analytics tab shows charts
- [ ] Export buttons work
- [ ] Dark mode toggles
- [ ] No console errors (F12)
- [ ] Render logs show "INFO" level messages
- [ ] OPENROUTER_SITE_URL is updated to Render URL
- [ ] Share link with users!

---

## Support & Resources

- **Render Docs:** https://render.com/docs
- **OpenRouter API:** https://openrouter.ai/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **GitHub Issues:** Report bugs in your repository

---

## Next Steps

1. ✅ Deploy to Render (this guide)
2. ✅ Monitor logs for errors
3. ✅ Share the live link with others
4. ✅ Add more AI models in settings
5. ✅ Collect user feedback for improvements

**Your Aerulias AI is now live! 🎉**
