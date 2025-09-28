# 🚗 DriveWise AI Platform

**An AI-powered driving insights and insurance risk platform that combines real-world traffic and vehicle data with telematics to deliver fair, behavior-based insurance scoring.**

## 🎯 Project Overview

DriveWise AI revolutionizes the insurance industry by providing transparent, data-driven risk assessment based on actual driving behavior. The platform ingests real-world traffic data from TomTom and vehicle safety data from NHTSA, combines it with telematics, and uses advanced ML models to generate personalized driving safety scores and insurance risk assessments.

### Key Features

✅ **Real-time Data Ingestion**: Custom connectors for TomTom Traffic API and NHTSA Vehicle Safety API  
✅ **Advanced ML Pipeline**: BigQuery ML and Vertex AI for risk modeling and safety scoring  
✅ **Conversational AI Agent**: Natural language interface powered by Vertex AI + Gemini  
✅ **Interactive Dashboard**: Real-time visualization of driving trends and risk factors  
✅ **Transparent Insurance Scoring**: Behavior-based premium calculations  
✅ **Traffic Hotspot Analysis**: Geographic risk assessment and route optimization  

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          DriveWise AI Platform                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   TomTom    │    │    NHTSA    │    │ Telematics  │        │
│  │ Traffic API │    │Vehicle API  │    │    Data     │        │
│  └─────┬───────┘    └─────┬───────┘    └─────┬───────┘        │
│        │                  │                  │                │
│        └──────────────────┼──────────────────┘                │
│                           │                                   │
│  ┌─────────────────────────▼─────────────────────────┐        │
│  │              Custom Fivetran Connectors            │        │
│  └─────────────────────────┬─────────────────────────┘        │
│                           │                                   │
│  ┌─────────────────────────▼─────────────────────────┐        │
│  │                Google BigQuery                     │        │
│  │  • Raw data storage  • Feature engineering        │        │
│  │  • Data warehouse    • ML model training          │        │
│  └─────────────────────────┬─────────────────────────┘        │
│                           │                                   │
│  ┌─────────────────────────▼─────────────────────────┐        │
│  │            Vertex AI + BigQuery ML                 │        │
│  │  • Risk scoring models  • Safety score models     │        │
│  │  • Anomaly detection   • Predictive analytics     │        │
│  └─────────────────────────┬─────────────────────────┘        │
│                           │                                   │
│  ┌─────────────────────────▼─────────────────────────┐        │
│  │                FastAPI Backend                     │        │
│  │  • REST APIs        • Authentication              │        │
│  │  • Business logic   • Real-time processing       │        │
│  └─────────────────────────┬─────────────────────────┘        │
│                           │                                   │
│  ┌─────────────────────────▼─────────────────────────┐        │
│  │     React Dashboard + Conversational Agent         │        │
│  │  • Real-time visualization  • Natural language    │        │
│  │  • Risk trend analysis      • Query interface     │        │
│  └─────────────────────────────────────────────────────       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Cloud Platform account
- TomTom Developer API key
- Docker & Docker Compose (optional)

### 1. Clone and Setup

```bash
git clone <your-repo-url> drivewise-ai
cd drivewise-ai
./setup.sh
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your configuration
vim .env
```

**Required Configuration:**
- `GCP_PROJECT_ID`: Your Google Cloud Project ID
- `TOMTOM_API_KEY`: Your TomTom API key
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your GCP service account key

### 3. Start Services

**Development Mode:**
```bash
# Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm start

# Data Pipeline (new terminal)  
cd data-pipeline
source venv/bin/activate
python main.py
```

**Production Mode:**
```bash
docker-compose up -d
```

### 4. Access the Platform

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Jupyter Notebooks**: http://localhost:8888

## 📊 Data Sources & APIs

### TomTom Traffic API
- **Real-time traffic flow data**
- **Traffic incident information**
- **Route optimization data**
- **Congestion level analysis**

```python
# Example usage
from data_pipeline.tomtom_connector import TomTomConnector

connector = TomTomConnector()
traffic_data = connector.get_traffic_flow(37.7749, -122.4194)
incidents = connector.get_traffic_incidents(37.7749, -122.4194, radius=10)
```

### NHTSA Vehicle API
- **Vehicle safety ratings**
- **Recall information**
- **Crash test data**
- **Vehicle specifications**

```python
# Example usage
from data_pipeline.nhtsa_connector import NHTSAConnector

connector = NHTSAConnector()
vehicle_data = connector.get_vehicle_info("1HGBH41JXMN109186")
safety_rating = connector.get_safety_rating("Honda", "Civic", "2020")
```

## 🤖 Machine Learning Models

### Risk Scoring Model
- **Input Features**: Speeding events, hard braking, acceleration patterns, time of day, weather conditions
- **Model Type**: Logistic Regression (BigQuery ML)
- **Output**: Risk probability (0-1 scale)
- **Update Frequency**: Hourly

### Safety Scoring Model  
- **Input Features**: Following distance, smooth acceleration/braking, speed limit adherence
- **Model Type**: Linear Regression (BigQuery ML)
- **Output**: Safety score (0-100 scale)
- **Update Frequency**: Daily

### Anomaly Detection
- **Purpose**: Identify unusual driving patterns
- **Technology**: Vertex AI AutoML
- **Applications**: Fraud detection, emergency response

```sql
-- Example: Get risk score for a user
SELECT `drivewise_ai.predict_risk_score`('user123', 7) as risk_score;

-- Example: Get safety score for a user  
SELECT `drivewise_ai.predict_safety_score`('user123', 7) as safety_score;
```

## 💬 Conversational AI Agent

The DriveWise AI agent uses **Vertex AI Agent Builder + Gemini** to provide natural language interaction:

**Example Queries:**
- "How safe was my driving today?"
- "What's my current insurance risk score?"
- "Show me traffic hotspots in my area"
- "How can I improve my safety score?"
- "Compare my driving to others in my age group"

```python
# Backend integration
from services.vertex_ai_service import VertexAIService

ai_service = VertexAIService()
response = ai_service.chat(
    "How safe was my driving today?", 
    user_context=user_data
)
```

## 📈 Dashboard Features

### Real-time Metrics
- **Current risk score** with trend analysis
- **Safety score breakdown** by category
- **Recent trip analysis** with event highlighting
- **Comparative rankings** vs. peer groups

### Interactive Visualizations
- **Risk trend charts** over time
- **Geographic heatmaps** of driving patterns
- **Traffic hotspot maps** with incident data
- **Insurance premium calculator**

### Insights & Recommendations
- **Personalized improvement suggestions**
- **Route optimization recommendations**
- **Driving behavior alerts**
- **Insurance savings opportunities**

## 🔐 API Documentation

### Authentication
```bash
# Get JWT token
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password"
}
```

### Core Endpoints

#### Risk & Safety Scores
```bash
GET /api/v1/risk-score/{user_id}
GET /api/v1/safety-score/{user_id}
```

#### Driving Data
```bash
POST /api/v1/driving-data
GET /api/v1/dashboard/{user_id}
```

#### Conversational Agent
```bash
POST /api/v1/chat
{
  "user_id": "user123",
  "message": "How safe was my driving today?",
  "context": {}
}
```

#### Traffic Analysis
```bash
GET /api/v1/traffic-hotspots?lat=37.7749&lon=-122.4194&radius=25
```

## 🗄️ Database Schema

### Key Tables

**driving_data**: Raw telematics and trip data  
**traffic_data**: Real-time traffic information  
**vehicle_data**: Vehicle safety and specification data  
**risk_scores**: ML-generated risk assessments  
**safety_scores**: Driving safety evaluations  
**user_profiles**: User demographics and preferences  

### Views & Functions

**daily_driving_metrics**: Aggregated daily driving statistics  
**weekly_risk_trends**: Risk score trends over time  
**traffic_hotspots**: Geographic risk analysis  
**predict_risk_score()**: Real-time risk scoring function  
**predict_safety_score()**: Real-time safety scoring function  

## 🔧 Configuration

### Environment Variables

```bash
# Google Cloud Platform
GCP_PROJECT_ID=your-gcp-project-id
GCP_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# API Keys
TOMTOM_API_KEY=your-tomtom-api-key

# Database
BIGQUERY_DATASET_ID=drivewise_ai
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRATION_MINUTES=1440

# Features
ENABLE_REAL_TIME_SCORING=true
ENABLE_CONVERSATIONAL_AGENT=true
```

### BigQuery Setup

```bash
# Create dataset and tables
bq query --use_legacy_sql=false < ml-models/bigquery_schema.sql

# Load sample data
bq load --source_format=NEWLINE_DELIMITED_JSON \
  drivewise_ai.driving_data \
  data/sample_driving_data.json
```

## 🚀 Deployment

### Google Cloud Platform

```bash
# Deploy to Cloud Run
gcloud run deploy drivewise-api \
  --source ./backend \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend to Firebase
cd frontend
npm run build
firebase deploy
```

### Docker Deployment

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale backend=3
```

### Kubernetes (GKE)

```bash
# Deploy to Google Kubernetes Engine
kubectl apply -f infrastructure/k8s/
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=.
```

### Frontend Tests
```bash
cd frontend  
npm test -- --coverage
```

### Integration Tests
```bash
# Test data pipeline
cd data-pipeline
python -m pytest tests/

# Test ML models
cd ml-models
python test_models.py
```

## 📊 Monitoring & Observability

### Health Checks
- `/health` - Basic health check
- `/health/detailed` - Service status details
- BigQuery connection monitoring
- Vertex AI service monitoring

### Logging
- Structured JSON logging
- Google Cloud Logging integration
- Error tracking with Sentry
- Performance monitoring

### Metrics
- API response times
- ML model accuracy
- Data pipeline success rates
- User engagement analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Write comprehensive tests
- Update documentation
- Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

### Common Issues

**1. BigQuery Authentication Error**
```bash
# Set up service account
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
```

**2. TomTom API Rate Limiting**
```python
# Implement exponential backoff
import time
from random import random

def retry_with_backoff(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** i) + random()
            time.sleep(wait_time)
```

**3. Frontend Build Issues**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Getting Help

- 📧 Email: support@drivewise-ai.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 Discord: [DriveWise AI Community](https://discord.gg/drivewise-ai)
- 📖 Documentation: [Full Documentation](https://docs.drivewise-ai.com)

## 🔮 Roadmap

### Phase 2 Features
- [ ] Mobile app for iOS/Android
- [ ] Integration with more insurance providers
- [ ] Advanced weather data integration
- [ ] Fleet management dashboard
- [ ] Driver coaching and gamification

### Phase 3 Features
- [ ] Autonomous vehicle readiness scoring
- [ ] Predictive maintenance alerts
- [ ] Carbon footprint tracking
- [ ] Social driving features
- [ ] Insurance marketplace integration

---

**Built with ❤️ for safer roads and fairer insurance**

*DriveWise AI - Where good driving pays off* 🚗💨