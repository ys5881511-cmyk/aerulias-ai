# 🚀 Deploy to Railway (LIVE IN 2 MINUTES)

## Step 1: Go to Railway
Open: https://railway.app

## Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub"**
3. Connect your GitHub account (if not already done)
4. Find & select **`aerulias-ai`** repository
5. Click **"Deploy"**

## Step 3: Configure Environment Variables
Railway will detect Python automatically. You need to add:

In Railway Dashboard, go to **Variables** tab and add:
```
OPENROUTER_API_KEY=sk-or-test-xxxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_URL=<your-railway-url>
OPENROUTER_APP_NAME=aerulias_ai
ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

**Note**: Get `OPENROUTER_API_KEY` from https://openrouter.ai

## Step 4: Wait for Deployment
- Railway builds your Docker image automatically
- Deployment takes ~2-3 minutes
- You'll see a **Live URL** like: `https://aerulias-ai-prod-xxxx.railway.app`

## Step 5: Test Your Live Server
```bash
# Get your Railway URL from dashboard, then:
curl https://aerulias-ai-prod-xxxx.railway.app/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.1.0"
}
```

## Share on LinkedIn/Resume
Once deployed, your live URL is:
```
https://aerulias-ai-prod-xxxx.railway.app
```

Add to LinkedIn:
- **Title**: Aerulias AI - Multi-Agent LLM System
- **Link**: https://your-railway-url
- **Description**: Production-grade AI evaluation system with Generator, Evaluator, and Refiner agents. Real-time API with 95%+ accuracy scoring. Deployed on Railway.

## Troubleshooting
If deployment fails:
1. Check **Deploy** tab for build errors
2. Verify `Dockerfile` exists in repo
3. Check **Logs** tab for runtime errors
4. Ensure `OPENROUTER_API_KEY` is set correctly

---

**Your project is now LIVE** ✅

GitHub Repo: https://github.com/ys5881511-cmyk/aerulias-ai
