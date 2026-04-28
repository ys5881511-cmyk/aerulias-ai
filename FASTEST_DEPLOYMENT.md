# 🚀 Railway Deployment (FASTEST - 2 MINUTES)

## Step 1: Install GitHub CLI & Login (1 min)
```powershell
# If you have scoop or chocolatey:
choco install gh
# OR download from https://github.com/cli/cli

gh auth login
```

## Step 2: Initialize Git & Push to GitHub (1 min)
```powershell
cd C:\Users\Dell\Desktop\aerulias_ai
git init
git add .
git commit -m "Aerulias AI - Production Ready"
gh repo create aerulias_ai --source=. --remote=origin --push
```

## Step 3: Deploy to Railway (30 seconds)
1. Go to https://railway.app
2. Click "New Project"
3. Connect GitHub → Select aerulias_ai repo
4. Railway auto-detects Python + builds + deploys
5. Live URL ready in ~2 minutes

## Your Live URL
```
https://aerulias_ai-<random>.railway.app
```

## Test It
```powershell
curl https://aerulias_ai-<random>.railway.app/api/v1/health
```

---

## OR: Continue with Docker Desktop (if you want local)

If you have Docker downloaded, you need to:
1. **Run the installer** (Docker-Desktop-Installer.exe)
2. **Restart Windows** after installation
3. **Start Docker Desktop** (it runs in system tray)
4. Then run: `docker build -t aerulias:latest . && docker run -p 8000:8000 --env-file .env aerulias:latest`

Which path do you prefer?
- **Railway** = Fastest, live URL immediately ✅
- **Docker** = Local testing first, then deploy

---
