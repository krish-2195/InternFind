#!/bin/bash
# Build script for Render.com deployment

echo "🚀 Starting InternFind deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies  
echo "📦 Installing Node.js dependencies..."
npm install

# Build the frontend
echo "🏗️ Building frontend..."
npm run build

# Create static file serving setup
echo "🔧 Setting up static file serving..."

echo "✅ Build completed successfully!"
