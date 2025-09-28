# 🚀 Quick Setup Guide

## Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- TomTom API key (optional for demo)

## Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd AI-Accelerate-Hackathon
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Add your API keys (optional for demo)
# TOMTOM_API_KEY=your_key_here
# GCP_PROJECT_ID=your_project_id
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn simple_main:app --host 0.0.0.0 --port 8005 --reload
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 5. Access the Application
- **User Dashboard**: http://localhost:3000
- **Insurance Portal**: Click "🏢 Insurance Portal" button
- **Live Data**: Click "🔴 Start Live Data" button
- **API Docs**: http://localhost:8005/docs

## Features
- ✅ Multi-user risk assessment
- ✅ NHTSA vehicle safety integration
- ✅ Real-time data streaming simulation
- ✅ Insurance company analytics portal
- ✅ TomTom traffic data integration (with API key)

## Demo Users
- Sarah Chen (Honda Civic) - Excellent driver
- Mike Rodriguez (Ford F-150) - Average driver  
- Emma Johnson (Tesla Model 3) - Tech-savvy driver
- David Kim (BMW 330i) - Experienced driver
- Lisa Thompson (Subaru Outback) - Family driver

## Architecture
- **Backend**: Python FastAPI + NHTSA API + TomTom API
- **Frontend**: React + Tailwind CSS
- **Data**: Mock profiles + real-time simulation
- **APIs**: RESTful with OpenAPI documentation