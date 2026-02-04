#!/bin/bash

# Create .env files from examples
cp backend/.env.example backend/.env 2>/dev/null || true
cp frontend/.env.example frontend/.env 2>/dev/null || true

echo "✅ Created .env files"
echo ""
echo "⚠️  IMPORTANT: Edit the .env files with your actual values!"
echo ""
echo "Backend .env: backend/.env"
echo "Frontend .env: frontend/.env"
echo ""
echo "Generate a new SECRET_KEY with:"
echo "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
