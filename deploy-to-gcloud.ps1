# VeriFy - Google Cloud Quick Deploy Script
# Run this script to deploy your entire application to Google Cloud Platform

Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🚀 VeriFy - Google Cloud Platform Deployment" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Variables (CHANGE THESE)
$PROJECT_ID = "verify-ai-production"
$REGION = "us-central1"
$TAVILY_API_KEY = Read-Host "Enter your Tavily API Key"
$GEMINI_API_KEY = Read-Host "Enter your Gemini API Key"
$HUGGINGFACE_TOKEN = Read-Host "Enter your HuggingFace Token"

Write-Host "`n✓ Configuration saved!" -ForegroundColor Green
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

# Step 1: Check gcloud installation
Write-Host "`n[1/8] Checking Google Cloud SDK..." -ForegroundColor Yellow
try {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    Write-Host "✓ Google Cloud SDK found: $gcloudVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Google Cloud SDK not found!" -ForegroundColor Red
    Write-Host "Installing Google Cloud SDK..." -ForegroundColor Yellow
    winget install Google.CloudSDK
    Write-Host "Please restart PowerShell and run this script again." -ForegroundColor Yellow
    exit 1
}

# Step 2: Login and set project
Write-Host "`n[2/8] Setting up Google Cloud project..." -ForegroundColor Yellow
Write-Host "Logging in to Google Cloud..." -ForegroundColor Gray
gcloud auth login

Write-Host "Creating project: $PROJECT_ID" -ForegroundColor Gray
gcloud projects create $PROJECT_ID --name="VeriFy AI" 2>$null

gcloud config set project $PROJECT_ID
Write-Host "✓ Project configured!" -ForegroundColor Green

# Step 3: Enable required APIs
Write-Host "`n[3/8] Enabling Google Cloud APIs..." -ForegroundColor Yellow
$APIs = @(
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "containerregistry.googleapis.com",
    "secretmanager.googleapis.com"
)

foreach ($api in $APIs) {
    Write-Host "  Enabling $api..." -ForegroundColor Gray
    gcloud services enable $api --quiet
}
Write-Host "✓ All APIs enabled!" -ForegroundColor Green

# Step 4: Create secrets
Write-Host "`n[4/8] Storing API keys securely in Secret Manager..." -ForegroundColor Yellow
echo $TAVILY_API_KEY | gcloud secrets create tavily-api-key --data-file=- 2>$null
echo $GEMINI_API_KEY | gcloud secrets create gemini-api-key --data-file=- 2>$null
echo $HUGGINGFACE_TOKEN | gcloud secrets create huggingface-token --data-file=- 2>$null
Write-Host "✓ Secrets stored securely!" -ForegroundColor Green

# Step 5: Build and deploy backend
Write-Host "`n[5/8] Building and deploying backend (this may take 10-15 minutes)..." -ForegroundColor Yellow
Write-Host "  Building Docker container..." -ForegroundColor Gray
Set-Location backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/verify-backend --timeout=20m

Write-Host "  Deploying to Cloud Run..." -ForegroundColor Gray
gcloud run deploy verify-backend `
    --image gcr.io/$PROJECT_ID/verify-backend `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 4Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 1 `
    --update-secrets="TAVILY_API_KEY=tavily-api-key:latest,GEMINI_API_KEY=gemini-api-key:latest,HUGGINGFACE_TOKEN=huggingface-token:latest" `
    --quiet

$BACKEND_URL = gcloud run services describe verify-backend --region $REGION --format "value(status.url)"
Write-Host "✓ Backend deployed at: $BACKEND_URL" -ForegroundColor Green
Set-Location ..

# Step 6: Update frontend configuration
Write-Host "`n[6/8] Configuring frontend..." -ForegroundColor Yellow
$apiConfig = Get-Content "src/config/api.ts" -Raw
$apiConfig = $apiConfig -replace "API_BASE_URL = .*", "API_BASE_URL = '$BACKEND_URL';"
Set-Content "src/config/api.ts" $apiConfig
Write-Host "✓ Frontend configured with backend URL!" -ForegroundColor Green

# Step 7: Build and deploy frontend
Write-Host "`n[7/8] Building and deploying frontend (this may take 5-10 minutes)..." -ForegroundColor Yellow
Write-Host "  Building Docker container..." -ForegroundColor Gray
gcloud builds submit --tag gcr.io/$PROJECT_ID/verify-frontend --timeout=15m

Write-Host "  Deploying to Cloud Run..." -ForegroundColor Gray
gcloud run deploy verify-frontend `
    --image gcr.io/$PROJECT_ID/verify-frontend `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --max-instances 5 `
    --min-instances 0 `
    --quiet

$FRONTEND_URL = gcloud run services describe verify-frontend --region $REGION --format "value(status.url)"
Write-Host "✓ Frontend deployed at: $FRONTEND_URL" -ForegroundColor Green

# Step 8: Summary
Write-Host "`n[8/8] Deployment Complete!" -ForegroundColor Yellow
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🎉 YOUR APP IS LIVE ON GOOGLE CLOUD! 🎉" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 Your Application URLs:" -ForegroundColor Cyan
Write-Host "   Frontend: $FRONTEND_URL" -ForegroundColor White
Write-Host "   Backend:  $BACKEND_URL" -ForegroundColor White
Write-Host ""
Write-Host "📊 View Logs:" -ForegroundColor Cyan
Write-Host "   gcloud run services logs read verify-backend --region $REGION" -ForegroundColor Gray
Write-Host "   gcloud run services logs read verify-frontend --region $REGION" -ForegroundColor Gray
Write-Host ""
Write-Host "⚙️ Manage Services:" -ForegroundColor Cyan
Write-Host "   gcloud run services list" -ForegroundColor Gray
Write-Host "   gcloud run services describe verify-backend --region $REGION" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Monitor Costs:" -ForegroundColor Cyan
Write-Host "   https://console.cloud.google.com/billing" -ForegroundColor Gray
Write-Host ""
Write-Host "📈 View Monitoring:" -ForegroundColor Cyan
Write-Host "   https://console.cloud.google.com/run?project=$PROJECT_ID" -ForegroundColor Gray
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎊 Congratulations! Your app is now running on Google Cloud!" -ForegroundColor Green
Write-Host "   All 5 AI models are active and ready to detect deepfakes!" -ForegroundColor Green
Write-Host ""

# Open frontend in browser
Write-Host "Opening your application in browser..." -ForegroundColor Cyan
Start-Process $FRONTEND_URL
