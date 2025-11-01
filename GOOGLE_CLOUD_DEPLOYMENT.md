# 🚀 VeriFy - Complete Google Cloud Platform Deployment Guide

## ✅ YES! You Can Deploy Everything on Google Cloud!

This guide will show you how to deploy your **entire VeriFy application** (frontend, backend with all 5 AI models, and Chrome extension) on **Google Cloud Platform**.

---

## 📋 What We'll Deploy on GCP

1. **Frontend** → Cloud Run (Containerized React app)
2. **Backend** → Cloud Run (FastAPI with all 5 AI models)
3. **Database** → Cloud SQL (PostgreSQL for user data)
4. **Storage** → Cloud Storage (For model files and assets)
5. **CDN** → Cloud CDN (Fast content delivery)
6. **Domain** → Cloud DNS (Optional custom domain)

**Total Cost**: **~$20-50/month** (with free tier credits)

---

## 🎯 Architecture Overview

```
User Browser
    ↓
Cloud CDN (Frontend) → Cloud Run (React App)
    ↓
Cloud Load Balancer
    ↓
Cloud Run (Backend) → AI Models (RoBERTa, EfficientNet, Xception, Wav2Vec2)
    ↓
Cloud Storage (Model files, user uploads)
    ↓
Cloud SQL (User data, detection history)
```

---

## 📦 Prerequisites

### 1. Install Google Cloud CLI

```powershell
# Install gcloud CLI using winget
winget install Google.CloudSDK

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify installation
gcloud --version
```

### 2. Initialize and Login

```powershell
# Login to your Google account
gcloud auth login

# Set your project ID (or create new one)
gcloud projects create verify-ai-production --name="VeriFy AI"

# Set active project
gcloud config set project verify-ai-production

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable storage.googleapis.com
```

---

## 🐳 Step 1: Containerize Your Application

### A. Create Dockerfile for Backend

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_ai.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_ai.txt

# Copy application code
COPY . .

# Download models during build (optional - can also download at runtime)
ENV HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run the application
CMD ["uvicorn", "ai_server_sota:app", "--host", "0.0.0.0", "--port", "8080"]
```

### B. Create Dockerfile for Frontend

Create `Dockerfile` in root:

```dockerfile
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### C. Create nginx.conf

Create `nginx.conf` in root:

```nginx
server {
    listen 8080;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### D. Create .dockerignore

Create `.dockerignore`:

```
node_modules
.git
.env
*.md
backend/venv
backend/__pycache__
.vscode
```

---

## 🚀 Step 2: Deploy Backend to Cloud Run

### A. Build and Push Backend Container

```powershell
# Navigate to backend directory
cd backend

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/verify-ai-production/backend

# Deploy to Cloud Run
gcloud run deploy verify-backend \
    --image gcr.io/verify-ai-production/backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars "TAVILY_API_KEY=your_tavily_key,GEMINI_API_KEY=your_gemini_key,HUGGINGFACE_TOKEN=your_hf_token"
```

**Important**: Replace `your_*_key` with actual API keys

### B. Get Backend URL

```powershell
# Get the deployed URL
gcloud run services describe verify-backend --region us-central1 --format "value(status.url)"

# Example output: https://verify-backend-xyz123.run.app
```

**Save this URL** - you'll need it for the frontend!

---

## 🚀 Step 3: Deploy Frontend to Cloud Run

### A. Update API Configuration

Edit `src/config/api.ts`:

```typescript
export const API_BASE_URL = 'https://verify-backend-xyz123.run.app'; // Your backend URL
```

### B. Build and Deploy Frontend

```powershell
# Navigate back to root
cd ..

# Build and push frontend
gcloud builds submit --tag gcr.io/verify-ai-production/frontend

# Deploy to Cloud Run
gcloud run deploy verify-frontend \
    --image gcr.io/verify-ai-production/frontend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1
```

### C. Get Frontend URL

```powershell
# Get the deployed URL
gcloud run services describe verify-frontend --region us-central1 --format "value(status.url)"

# Example output: https://verify-frontend-abc456.run.app
```

🎉 **Your app is now LIVE on Google Cloud!**

---

## 💾 Step 4: Set Up Cloud Storage (Optional but Recommended)

### A. Create Storage Bucket

```powershell
# Create bucket for model files
gsutil mb -l us-central1 gs://verify-ai-models

# Create bucket for user uploads
gsutil mb -l us-central1 gs://verify-ai-uploads

# Make model bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://verify-ai-models
```

### B. Upload Model Files (Optional)

```powershell
# Upload pre-downloaded models to reduce startup time
gsutil cp -r backend/models/* gs://verify-ai-models/
```

### C. Update Backend to Use Cloud Storage

Edit `backend/ai_server_sota.py` to download models from Cloud Storage instead of HuggingFace at runtime (for faster startup).

---

## 🗄️ Step 5: Set Up Cloud SQL (Optional - for user data)

### A. Create PostgreSQL Instance

```powershell
# Create Cloud SQL instance
gcloud sql instances create verify-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create verifydb --instance=verify-db

# Create user
gcloud sql users create verify_user \
    --instance=verify-db \
    --password=your_secure_password
```

### B. Connect Backend to Cloud SQL

```powershell
# Update backend deployment with database connection
gcloud run services update verify-backend \
    --add-cloudsql-instances verify-ai-production:us-central1:verify-db \
    --set-env-vars "DATABASE_URL=postgresql://verify_user:your_secure_password@/verifydb?host=/cloudsql/verify-ai-production:us-central1:verify-db"
```

---

## 🚀 Step 6: Enable Auto-Scaling

Cloud Run automatically scales, but you can configure limits:

```powershell
# Set max instances for backend
gcloud run services update verify-backend \
    --max-instances 10 \
    --min-instances 1

# Set max instances for frontend
gcloud run services update verify-frontend \
    --max-instances 5 \
    --min-instances 0
```

---

## 🌐 Step 7: Set Up Custom Domain (Optional)

### A. Map Custom Domain

```powershell
# Map domain to frontend
gcloud run domain-mappings create \
    --service verify-frontend \
    --domain verify.yourdomain.com \
    --region us-central1

# Map API subdomain to backend
gcloud run domain-mappings create \
    --service verify-backend \
    --domain api.verify.yourdomain.com \
    --region us-central1
```

### B. Update DNS Records

Add the DNS records shown in the output to your domain registrar.

---

## 📊 Step 8: Set Up Monitoring

### A. Enable Cloud Monitoring

```powershell
# Install monitoring
gcloud services enable monitoring.googleapis.com
gcloud services enable logging.googleapis.com
```

### B. View Logs

```powershell
# Backend logs
gcloud run services logs read verify-backend --region us-central1

# Frontend logs
gcloud run services logs read verify-frontend --region us-central1

# Follow logs in real-time
gcloud run services logs tail verify-backend --region us-central1
```

---

## 💰 Step 9: Cost Optimization

### Free Tier Limits (Monthly):
- **Cloud Run**: 2 million requests free
- **Cloud Storage**: 5 GB free
- **Cloud Build**: 120 build-minutes free
- **Cloud SQL**: $0 (if using db-f1-micro in some regions)

### Cost Estimates (After Free Tier):
- **Frontend**: ~$5-10/month
- **Backend with AI Models**: ~$30-40/month (4GB RAM)
- **Cloud Storage**: ~$1-5/month
- **Cloud SQL**: ~$10/month (if needed)

### Reduce Costs:
```powershell
# Set min instances to 0 (cold start but no idle cost)
gcloud run services update verify-backend --min-instances 0
gcloud run services update verify-frontend --min-instances 0

# Use preemptible instances for non-critical workloads
gcloud run services update verify-backend --no-cpu-throttling
```

---

## 🔒 Step 10: Security Hardening

### A. Use Secret Manager for API Keys

```powershell
# Enable Secret Manager
gcloud services enable secretmanager.googleapis.com

# Create secrets
echo -n "your_tavily_key" | gcloud secrets create tavily-api-key --data-file=-
echo -n "your_gemini_key" | gcloud secrets create gemini-api-key --data-file=-
echo -n "your_hf_token" | gcloud secrets create huggingface-token --data-file=-

# Grant access to Cloud Run service account
gcloud secrets add-iam-policy-binding tavily-api-key \
    --member serviceAccount:verify-backend@verify-ai-production.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

# Update deployment to use secrets
gcloud run services update verify-backend \
    --update-secrets=TAVILY_API_KEY=tavily-api-key:latest \
    --update-secrets=GEMINI_API_KEY=gemini-api-key:latest \
    --update-secrets=HUGGINGFACE_TOKEN=huggingface-token:latest
```

### B. Enable Cloud Armor (DDoS Protection)

```powershell
# Create security policy
gcloud compute security-policies create verify-security-policy \
    --description "Security policy for VeriFy"

# Add rate limiting rule
gcloud compute security-policies rules create 1000 \
    --security-policy verify-security-policy \
    --expression "true" \
    --action "rate-based-ban" \
    --rate-limit-threshold-count 1000 \
    --rate-limit-threshold-interval-sec 60
```

---

## 🔄 Step 11: CI/CD with Cloud Build

Create `cloudbuild.yaml` in root:

```yaml
steps:
  # Build backend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/backend', './backend']
    id: 'build-backend'
  
  # Build frontend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/frontend', '.']
    id: 'build-frontend'
  
  # Push backend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/backend']
    id: 'push-backend'
  
  # Push frontend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/frontend']
    id: 'push-frontend'
  
  # Deploy backend
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'verify-backend'
      - '--image=gcr.io/$PROJECT_ID/backend'
      - '--region=us-central1'
      - '--platform=managed'
    id: 'deploy-backend'
  
  # Deploy frontend
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'verify-frontend'
      - '--image=gcr.io/$PROJECT_ID/frontend'
      - '--region=us-central1'
      - '--platform=managed'
    id: 'deploy-frontend'

timeout: '1200s'
```

### Set up auto-deploy from GitHub:

```powershell
# Connect GitHub repo
gcloud alpha builds triggers create github \
    --repo-name=VeriFy-AI \
    --repo-owner=DevDebjit83 \
    --branch-pattern="^main$" \
    --build-config=cloudbuild.yaml
```

Now every push to `main` auto-deploys! 🎉

---

## 🧪 Step 12: Testing Your Deployment

### Test Backend:

```powershell
# Test health endpoint
curl https://verify-backend-xyz123.run.app/health

# Test text detection
curl -X POST https://verify-backend-xyz123.run.app/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news: Water freezes at 0°C"}'
```

### Test Frontend:

Open your browser to: `https://verify-frontend-abc456.run.app`

---

## 📱 Chrome Extension Distribution

Your Chrome extension works with the deployed backend! Just update the API URL in the extension's configuration.

---

## 🎯 Quick Command Summary

```powershell
# 1. Install gcloud
winget install Google.CloudSDK

# 2. Initialize
gcloud auth login
gcloud config set project verify-ai-production

# 3. Deploy Backend
cd backend
gcloud builds submit --tag gcr.io/verify-ai-production/backend
gcloud run deploy verify-backend --image gcr.io/verify-ai-production/backend --platform managed --region us-central1 --allow-unauthenticated --memory 4Gi --cpu 2

# 4. Deploy Frontend
cd ..
gcloud builds submit --tag gcr.io/verify-ai-production/frontend
gcloud run deploy verify-frontend --image gcr.io/verify-ai-production/frontend --platform managed --region us-central1 --allow-unauthenticated

# 5. Get URLs
gcloud run services list
```

---

## ✅ Verification Checklist

- [ ] gcloud CLI installed
- [ ] Google Cloud project created
- [ ] APIs enabled
- [ ] Backend Dockerfile created
- [ ] Frontend Dockerfile created
- [ ] API keys added as environment variables
- [ ] Backend deployed to Cloud Run
- [ ] Frontend deployed to Cloud Run
- [ ] Frontend connected to backend
- [ ] All 5 detection models working
- [ ] Chrome extension updated with production URL
- [ ] Custom domain configured (optional)
- [ ] Monitoring enabled
- [ ] CI/CD pipeline set up
- [ ] 🎉 **APPLICATION LIVE ON GOOGLE CLOUD!**

---

## 💡 Pro Tips

1. **Use Cloud Build cache** to speed up builds
2. **Set up Cloud CDN** for faster global access
3. **Use Memorystore (Redis)** for caching frequent requests
4. **Enable Cloud Trace** for performance monitoring
5. **Set up alerting** for errors and high costs

---

## 🆘 Troubleshooting

### Issue: Container build fails
```powershell
# Check build logs
gcloud builds list
gcloud builds log <BUILD_ID>
```

### Issue: Service won't start
```powershell
# Check service logs
gcloud run services logs read verify-backend --region us-central1 --limit 100
```

### Issue: Out of memory
```powershell
# Increase memory
gcloud run services update verify-backend --memory 8Gi
```

---

## 📞 Need Help?

- **GCP Documentation**: https://cloud.google.com/run/docs
- **GitHub Repo**: https://github.com/DevDebjit83/VeriFy-AI
- **Email**: devdebjit83@gmail.com

---

## 🎊 Congratulations!

Your **entire VeriFy application** with all 5 AI models is now running on **Google Cloud Platform**!

- ✅ Scalable (auto-scales to millions of users)
- ✅ Reliable (99.95% uptime SLA)
- ✅ Secure (Google-grade security)
- ✅ Fast (global CDN)
- ✅ Cost-effective (pay only for what you use)

**Your app is production-ready on Google Cloud! 🚀**
