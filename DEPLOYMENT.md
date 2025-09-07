# InternFind Deployment Guide

## 🚀 Quick Deploy to Render.com (Free)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Connect your GitHub repository

### Step 2: Deploy Your Application
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `KaranPatel001/InternFind`
3. Configure the deployment:
   - **Name**: `internfind-app`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `python backend/app.py`
   - **Instance Type**: `Free`

### Step 3: Environment Configuration
No additional environment variables needed - your app is ready to go!

### Step 4: Access Your Live Application
After deployment (5-10 minutes), you'll get a URL like:
`https://internfind-app.onrender.com`

## 🌐 Alternative Deployment Options

### Railway (Also Free)
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy with one click

### Vercel (Frontend Only)
- Best for React frontend
- Automatic deployments from GitHub

### Heroku (Paid)
- Classic platform
- Requires credit card

## 📱 Share Your Portfolio
Once deployed, add the live URL to:
- Your resume
- LinkedIn profile
- GitHub repository README
- Job applications

## 🔧 Troubleshooting
If deployment fails:
1. Check build logs in Render dashboard
2. Ensure all dependencies are in requirements.txt
3. Verify Python version compatibility

## 📞 Support
Contact the team:
- Krish Patel: krishvp27@gmail.com
- Karan Patel: karanhpatel167@gmail.com
