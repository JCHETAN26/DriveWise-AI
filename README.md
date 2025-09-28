# DriveWise AI Platform

An AI-powered driving insights and insurance risk platform that combines real-world traffic and vehicle data with telematics to deliver fair, behavior-based insurance scoring.

## 🚀 Features

- **Data Ingestion**: Custom Fivetran connectors for TomTom (traffic) and NHTSA (vehicle safety) APIs
- **ML Pipeline**: BigQuery ML and Vertex AI for risk modeling and personalized safety scoring
- **Conversational Agent**: Natural language interface using Vertex AI Agent Builder + Gemini
- **Dashboard**: Real-time visualization of driving trends and risk hotspots
- **Insurance Integration**: Transparent behavior-based insurance scoring

## 🏗️ Architecture

```
├── backend/                 # Python FastAPI backend
├── frontend/               # React dashboard
├── data-pipeline/          # Data ingestion and ETL
├── ml-models/             # BigQuery ML and Vertex AI models
├── conversational-agent/  # Vertex AI agent configuration
├── infrastructure/        # GCP deployment configs
└── docs/                  # Documentation
```

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **Data**: BigQuery, Vertex AI, Fivetran
- **Cloud**: Google Cloud Platform
- **ML**: BigQuery ML, Vertex AI, TensorFlow

## 🚦 Getting Started

1. **Setup Environment**
   ```bash
   cp .env.example .env
   # Configure your API keys and GCP credentials
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Data Pipeline**
   ```bash
   cd data-pipeline
   python setup_bigquery.py
   python ingest_data.py
   ```

## 📊 Data Sources

- **TomTom Traffic API**: Real-time traffic data, congestion levels
- **NHTSA Vehicle API**: Vehicle safety ratings and recall information
- **Telematics**: GPS tracking, accelerometer data, driving patterns

## 🤖 ML Models

- **Risk Scoring Model**: Predicts insurance risk based on driving behavior
- **Safety Score Model**: Generates personalized driving safety scores
- **Anomaly Detection**: Identifies unusual driving patterns

## 💬 Conversational Agent

Ask natural language questions like:
- "How safe was my driving today?"
- "What's my current insurance risk score?"
- "Show me traffic hotspots in my area"

## 📈 Dashboard Features

- Real-time driving score tracking
- Risk hotspot visualization
- Behavioral trend analysis
- Insurance premium estimates

## 🚀 Deployment

The platform is designed for Google Cloud Platform deployment with:
- Cloud Run for backend services
- BigQuery for data warehousing
- Vertex AI for ML models
- Firebase for frontend hosting

## 📝 License

MIT License - see LICENSE file for details.