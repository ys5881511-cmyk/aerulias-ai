# 🚀 QUICK START: Deploy in 5 Minutes

**Most important file:** Read this first, then do the 6 steps below.

---

## 📋 What You'll Do

1. Create GitHub account & repo (2 min)
2. Push code to GitHub (1 min)  
3. Sign up for Railway (1 min)
4. Connect GitHub to Railway (1 min)

**Total: ~5 minutes → Live URL ready to share! ✅**

---

## 🎯 6 Simple Steps

### **Step 1: Setup GitHub** 
```
1. Go to https://github.com/new
2. Enter repo name: aerulias_ai
3. Click "Create repository"
4. Copy the HTTPS URL
```

### **Step 2: Push Your Code**

Open PowerShell in your project folder and run:

```powershell
cd C:\Users\Dell\Desktop\aerulias_ai

# Setup git
git init
git add .
git commit -m "Aerulias AI - Production Ready"

# Add your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/aerulias_ai.git
git branch -M main
git push -u origin main
```

### **Step 3: Create Railway Account**

1. Go to https://railway.app
2. Click "Start Project"
3. Sign up with GitHub (easiest!)
4. Click "Authorize railway-app" when asked

### **Step 4: Import Your GitHub Repo**

1. After login, click "New Project"
2. Select "Deploy from GitHub repo"
3. Find your `aerulias_ai` repo
4. Click "Deploy"

### **Step 5: Add Your API Key**

1. In Railway dashboard, click "Variables"
2. Add this ONE important variable:

```
OPENROUTER_API_KEY = your_api_key_here
```

**How to get API key:**
- Go to https://openrouter.ai
- Sign up (takes 1 minute)
- Create API key in settings
- Copy and paste into Railway

### **Step 6: Wait & Get Your Live URL**

1. Railway starts deploying automatically
2. Wait 2-3 minutes
3. You'll see a URL like: `https://aerulias-ai-abc123.railway.app`
4. **That's your live project! 🎉**

---

## ✅ Test It's Working

Click this link (replace with your Railway URL):
```
https://your-railway-url.railway.app/api/v1/health
```

You should see:
```json
{"status":"healthy","version":"1.1.0","components":{"api":"ok"}}
```

---

## 🔗 Share Your Live Project

### LinkedIn Post:
```
🚀 Just deployed Aerulias AI to production!

A multi-agent AI system that automatically 
evaluates and improves answers using LLMs.

✨ Live Demo: https://your-railway-url.railway.app
💻 Code: https://github.com/YOUR_USERNAME/aerulias_ai

#AI #Python #FastAPI #Production
```

### Resume:
```
Deployed Aerulias AI production system to Railway
• Multi-agent architecture with quality scoring
• Live URL: https://your-railway-url.railway.app  
• GitHub: https://github.com/YOUR_USERNAME/aerulias_ai
```

### Share with Friends/Teachers:
```
Check this out: https://your-railway-url.railway.app

It's an AI system I built and deployed.
The code is on GitHub if you want to see it.
```

---

## 🎓 Show Your Teachers

Email them:
```
Subject: Aerulias AI - Production Deployment Project

I just deployed my AI project to production on Railway.
It's a multi-agent system that evaluates and improves AI answers.

Live Demo: https://your-railway-url.railway.app
GitHub: https://github.com/YOUR_USERNAME/aerulias_ai
Documentation: See README for full architecture details

The project includes:
- Production-grade Python code with full type hints
- REST API with comprehensive documentation
- Multi-agent architecture (Generator, Evaluator, Refiner)
- Deployed on Railway with auto-deployment from GitHub
- >80% test coverage with pytest

Let me know if you'd like me to explain the architecture!
```

---

## ❓ Common Issues

**"Build failed"** → Check Railway logs, verify requirements.txt exists

**"API returns error"** → Verify OPENROUTER_API_KEY is correct in Railway

**"Page not found"** → Try health endpoint: `/api/v1/health`

---

## 💡 What You Have Now

✅ Live working project URL  
✅ Can share on LinkedIn  
✅ Can show to friends/teachers  
✅ Can add to resume/portfolio  
✅ Auto-deploys when you push to GitHub  
✅ Completely free (for testing)  

---

**Next:** See `RAILWAY_DEPLOYMENT.md` for detailed instructions.

**Done!** Your project is live! 🚀
