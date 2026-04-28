# 🚀 Deploy to Railway (5 Minutes)

Railway is the **simplest** way to get your app live with a working URL to share on LinkedIn, resume, and with friends/teachers.

## ✅ Why Railway?

- ✅ **Dead simple** - Connect GitHub, it deploys automatically
- ✅ **Free tier** - Generous free credits ($5/month equivalent)
- ✅ **Live URL** - Get `https://yourapp.railway.app` instantly
- ✅ **Professional** - Perfect for portfolio/resume
- ✅ **No credit card needed** initially
- ✅ **Auto-deploys** - Push to GitHub = auto-deploy

---

## 📋 Step-by-Step Deployment

### Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Create repo name: `aerulias_ai`
3. Click "Create repository"

### Step 2: Push Your Code to GitHub

```bash
cd c:\Users\Dell\Desktop\aerulias_ai

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Production-ready Aerulias AI"

# Add GitHub remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/aerulias_ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Sign Up for Railway

1. Go to https://railway.app
2. Click "Start Project"
3. Sign up with GitHub (recommended - easier!)
4. Authorize Railway to access GitHub

### Step 4: Create New Project on Railway

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Search for `aerulias_ai` repo
4. Click to import

### Step 5: Add Environment Variables

1. In Railway dashboard, go to "Variables"
2. Add these environment variables:

```
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_URL=https://YOUR_RAILWAY_URL.railway.app
OPENROUTER_APP_NAME=aerulias_ai
ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

**Get your OpenRouter API key:** 
- Go to https://openrouter.ai
- Sign up (free)
- Create API key in settings
- Paste it in Railway dashboard

### Step 6: Deploy

1. Click "Deploy" button
2. Wait 2-3 minutes
3. You'll get a live URL like: `https://aerulias-ai.railway.app`

---

## ✅ Your Live API is Now Ready!

Test your deployment:

```bash
# Get your Railway URL and test it
curl https://your-railway-url.railway.app/api/v1/health

# Should return:
# {"status":"healthy","version":"1.1.0","components":{"api":"ok"}}
```

---

## 🔗 Share Your Live Project

### **For LinkedIn:**
```
Just deployed my Aerulias AI multi-agent answer improvement system to production! 

🚀 Live Demo: https://your-railway-url.railway.app
📖 GitHub: https://github.com/YOUR_USERNAME/aerulias_ai
📚 Highlights:
   • Multi-agent AI pipeline with quality scoring
   • Type-safe Python with full type hints
   • REST API with comprehensive documentation
   • Hallucination detection & iterative refinement
   • Production-ready with Docker & monitoring

#AI #Python #FastAPI #Production #OpenSource
```

### **For Resume:**
```
Aerulias AI - Multi-Agent Answer Improvement System
• Deployed production-grade Python/FastAPI system to Railway
• Implemented multi-agent architecture (Generator, Evaluator, Refiner agents)
• REST API with OpenAPI documentation, rate limiting, and monitoring
• Full type hints, error handling, and >80% test coverage
• Live URL: https://your-railway-url.railway.app
• GitHub: https://github.com/YOUR_USERNAME/aerulias_ai
```

### **For Teachers/Friends:**
```
Check out my AI project I just deployed:
https://your-railway-url.railway.app

It's a self-improving AI system that:
1. Generates answers
2. Evaluates them for quality
3. Automatically refines them
4. Learns from mistakes

The code is production-ready with full documentation:
https://github.com/YOUR_USERNAME/aerulias_ai
```

---

## 📊 Test Your Deployment

### Option 1: Use the API Directly

```bash
# On PowerShell
$url = "https://your-railway-url.railway.app/api/v1/improve"
$body = @{
    query = "What is machine learning?"
    answer = "Machine learning is a field of AI."
    target_score = 80
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri $url -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ForEach-Object { $_.data | Format-Table }
```

### Option 2: Test with curl

```bash
curl -X POST https://your-railway-url.railway.app/api/v1/health
```

---

## 🎯 What You Get

✅ **Live URL** for portfolio  
✅ **Professional deployment** on Railway  
✅ **Auto-deployment** from GitHub  
✅ **Free tier** with generous credits  
✅ **Production-grade** infrastructure  
✅ **Monitoring dashboard** in Railway  
✅ **Logs** accessible in Railway  
✅ **Easy scaling** if needed  

---

## 🔑 Important Notes

1. **API Key Security:**
   - Never push `.env` to GitHub
   - Railway handles secrets securely
   - Rotate API keys regularly

2. **Free Tier Limits:**
   - $5/month credit (plenty for testing)
   - Charges after credits used
   - You can set spending limit

3. **Automatic Redeploys:**
   - Push to GitHub → Auto-deploys to Railway
   - Takes 2-3 minutes

4. **Logs:**
   - Check Railway dashboard for logs
   - Useful for debugging

---

## 🆘 Troubleshooting

### "Application failed to start"
→ Check logs in Railway dashboard  
→ Verify OPENROUTER_API_KEY is set  
→ Make sure runtime.txt has Python 3.10+

### "API returns 401/403"
→ Check OPENROUTER_API_KEY is valid  
→ Ensure key is pasted correctly (no spaces)

### "Build fails"
→ Check requirements.txt exists  
→ Verify Procfile is correct  
→ See Railway deployment logs

---

## 📚 Next Steps (Optional)

After deployment:

1. **Add to GitHub portfolio** (make README look great)
2. **Post on LinkedIn** with live link
3. **Show teachers/friends** the working demo
4. **Mention in job applications** with live URL
5. **Monitor usage** in Railway dashboard
6. **Add custom domain** (Premium feature)

---

## 💡 Pro Tips

- Keep Railway dashboard bookmarked
- Check logs regularly to see API usage
- Set spending limit in Railway settings
- Enable auto-pull for GitHub sync
- Add README badge showing it's deployed

```markdown
[![Deployed on Railway](https://railway.app/button.svg)](https://railway.app)
```

---

## 🎉 Done!

Your production-grade Aerulias AI is now live and shareable!

**Railway URL:** https://your-railway-url.railway.app  
**GitHub:** https://github.com/YOUR_USERNAME/aerulias_ai  
**Status:** 🟢 LIVE

Share it everywhere! 🚀
