# Create .env files from examples
Copy-Item -Path "backend\.env.example" -Destination "backend\.env" -ErrorAction SilentlyContinue
Copy-Item -Path "frontend\.env.example" -Destination "frontend\.env" -ErrorAction SilentlyContinue

Write-Host "✅ Created .env files" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANT: Edit the .env files with your actual values!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend .env: backend\.env" -ForegroundColor Cyan
Write-Host "Frontend .env: frontend\.env" -ForegroundColor Cyan
Write-Host ""
Write-Host "Generate a new SECRET_KEY with:" -ForegroundColor Yellow
Write-Host "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'" -ForegroundColor Gray
