# ClickPesa Integration Setup Script
# Run this script after updating the .env file with your credentials

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ClickPesa Payment Gateway Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and add your ClickPesa credentials" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ .env file found" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path "env\Scripts\Activate.ps1") {
    & .\env\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "WARNING: Virtual environment not found at .\env\" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv env
    & .\env\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment created and activated" -ForegroundColor Green
}
Write-Host ""

# Install dependencies
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Package installation failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Migrations completed successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Migration failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Static files collected" -ForegroundColor Green
} else {
    Write-Host "WARNING: Static files collection had issues" -ForegroundColor Yellow
}
Write-Host ""

# Check if superuser exists
Write-Host "Checking for superuser..." -ForegroundColor Yellow
$result = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"
if ($result -match "True") {
    Write-Host "✓ Superuser already exists" -ForegroundColor Green
} else {
    Write-Host "No superuser found. Creating one..." -ForegroundColor Yellow
    python manage.py createsuperuser
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Update your .env file with ClickPesa credentials:" -ForegroundColor White
Write-Host "   - CLICKPESA_CLIENT_ID" -ForegroundColor Gray
Write-Host "   - CLICKPESA_API_KEY" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Access the application at:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Admin panel at:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Read CLICKPESA_INTEGRATION.md for full documentation" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
