# Deployment Guide: Transcript Insight & LinkedIn Icebreaker

This guide will walk you through deploying your application to GitHub, Render (backend), and Netlify (frontend).

## 🚀 **Step 1: GitHub Repository Setup**

### 1.1 Initialize Git Repository
```bash
# Navigate to your project directory
cd /Users/vivek/Desktop/Transcript

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Transcript Insight & LinkedIn Icebreaker app"

# Add your GitHub repository as remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/transcript-insight.git

# Push to GitHub
git push -u origin main
```

### 1.2 Repository Structure
Your repository should have this structure:
```
transcript-insight/
├── app/                    # Next.js app directory
├── components/             # React components
├── lib/                    # Utility functions
├── backend/                # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── database/               # Database schema
├── package.json            # Frontend dependencies
├── next.config.js          # Next.js configuration
├── netlify.toml           # Netlify configuration
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🎯 **Step 2: Backend Deployment on Render**

### 2.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Connect your GitHub repository

### 2.2 Deploy Backend Service
1. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

2. **Configure Service Settings**
   ```
   Name: transcript-insight-backend
   Root Directory: backend
   Runtime: Docker
   Branch: main
   Build Command: (leave empty - Docker handles this)
   Start Command: (leave empty - Docker handles this)
   ```

3. **Environment Variables**
   Add these environment variables in Render:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_anon_key_here
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your backend
   - Note the URL (e.g., `https://your-app-name.onrender.com`)

### 2.3 Verify Backend Deployment
Test your backend endpoints:
```bash
# Health check
curl https://your-app-name.onrender.com/health

# Test transcript endpoint
curl -X POST https://your-app-name.onrender.com/transcripts \
  -H "Content-Type: application/json" \
  -d '{"company_name":"Test","attendees":"John","date":"2024-01-01","transcript_content":"Test meeting"}'
```

## 🌐 **Step 3: Frontend Deployment on Netlify**

### 3.1 Create Netlify Account
1. Go to [netlify.com](https://netlify.com)
2. Sign up with your GitHub account
3. Connect your GitHub repository

### 3.2 Deploy Frontend
1. **Create New Site from Git**
   - Click "New site from Git"
   - Choose GitHub
   - Select your repository

2. **Configure Build Settings**
   ```
   Build command: npm run build
   Publish directory: .next
   Base directory: (leave empty - deploy from root)
   ```

3. **Environment Variables**
   Add this environment variable in Netlify:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com
   ```
   (Replace with your actual Render backend URL)

4. **Deploy**
   - Click "Deploy site"
   - Netlify will build and deploy your frontend
   - Note the URL (e.g., `https://your-app-name.netlify.app`)

### 3.3 Update API Configuration
After deployment, update the API URL in your code:

1. **Update `lib/api.ts`**
   ```typescript
   // Replace this line:
   return process.env.NEXT_PUBLIC_API_URL || 'https://your-backend-app.onrender.com';
   
   // With your actual Render URL:
   return process.env.NEXT_PUBLIC_API_URL || 'https://your-actual-backend.onrender.com';
   ```

2. **Redeploy**
   - Commit and push the changes
   - Netlify will automatically redeploy

## 🔧 **Step 4: Environment Setup**

### 4.1 Backend Environment Variables (Render)
In your Render dashboard, add these environment variables:

```
GOOGLE_API_KEY=your_google_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 4.2 Frontend Environment Variables (Netlify)
In your Netlify dashboard, add this environment variable:

```
NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com
```

## 🧪 **Step 5: Testing Deployment**

### 5.1 Test Backend
```bash
# Health check
curl https://your-backend-app.onrender.com/health

# Test transcript analysis
curl -X POST https://your-backend-app.onrender.com/transcripts \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Corp",
    "attendees": "John Doe, Jane Smith",
    "date": "2024-01-15",
    "transcript_content": "Meeting discussion about Q4 results..."
  }'
```

### 5.2 Test Frontend
1. Visit your Netlify URL
2. Test both features:
   - Upload a transcript
   - Generate a LinkedIn icebreaker
3. Verify the API calls work correctly

## 🔄 **Step 6: Continuous Deployment**

### 6.1 Automatic Deployments
Both Render and Netlify will automatically deploy when you push to your main branch:

```bash
# Make changes to your code
git add .
git commit -m "Update feature X"
git push origin main

# Both services will automatically redeploy
```

### 6.2 Manual Deployments
If needed, you can trigger manual deployments:
- **Render**: Go to your service dashboard → "Manual Deploy"
- **Netlify**: Go to your site dashboard → "Deploys" → "Trigger deploy"

## 🛠️ **Troubleshooting**

### Common Issues

1. **Backend Build Failures**
   - Check Render logs for build errors
   - Verify `requirements.txt` is in the backend directory
   - Ensure Dockerfile is correct

2. **Frontend Build Failures**
   - Check Netlify build logs
   - Verify all dependencies are in `package.json`
   - Check for TypeScript errors

3. **API Connection Issues**
   - Verify `NEXT_PUBLIC_API_URL` is set correctly
   - Check CORS settings in backend
   - Test backend endpoints directly

4. **Environment Variable Issues**
   - Ensure all required environment variables are set
   - Check variable names match exactly
   - Verify API keys are valid

### Debug Commands
```bash
# Test backend locally
cd backend
python -m uvicorn main:app --reload

# Test frontend locally
npm run dev

# Check build locally
npm run build
```

## 📊 **Monitoring & Analytics**

### 1. Render Monitoring
- View logs in Render dashboard
- Monitor resource usage
- Set up alerts for downtime

### 2. Netlify Analytics
- View site analytics in Netlify dashboard
- Monitor build times
- Check form submissions

### 3. Custom Domain (Optional)
Both services support custom domains:
- **Render**: Add custom domain in service settings
- **Netlify**: Add custom domain in site settings

## 🔒 **Security Considerations**

1. **Environment Variables**
   - Never commit API keys to Git
   - Use environment variables for all secrets
   - Rotate API keys regularly

2. **CORS Configuration**
   - Configure CORS in backend to allow only your frontend domain
   - Use HTTPS in production

3. **Rate Limiting**
   - Consider adding rate limiting to API endpoints
   - Monitor API usage

## 📈 **Performance Optimization**

1. **Backend**
   - Enable caching where appropriate
   - Optimize database queries
   - Use connection pooling

2. **Frontend**
   - Optimize bundle size
   - Enable compression
   - Use CDN for static assets

## 🎉 **Deployment Complete!**

Your application is now deployed and accessible at:
- **Frontend**: `https://your-app-name.netlify.app`
- **Backend**: `https://your-backend-app.onrender.com`

Remember to:
- Test all features thoroughly
- Monitor performance and errors
- Keep dependencies updated
- Backup your database regularly

For support, check the documentation for each service:
- [Render Documentation](https://render.com/docs)
- [Netlify Documentation](https://docs.netlify.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com) 