# DriveWise AI Platform

An AI-powered driving insights and insurance risk platform that combines real-world traffic and vehicle data with intelligent risk analysis to deliver fair, behavior-based insurance scoring.

## 🚀 Features

- **Real API Integration**: Direct integration with TomTom Traffic API and NHTSA Vehicle Safety API
- **Intelligent Risk Scoring**: Advanced algorithms for personalized driving risk assessment
- **AI Chat Assistant**: Interactive chat interface with personalized driving insights (enhanced mock responses using real user data)
- **Live Dashboard**: Real-time visualization of driving patterns, risk scores, and insurance portfolio data
- **Insurance Analytics**: Comprehensive insurance company dashboard with customer insights and risk distribution
- **Real-time Data Simulation**: Live traffic and driving data integration with dynamic updates

## 🏗️ Architecture

```
├── backend/                 # Python FastAPI backend with real API integrations
├── frontend/               # React dashboard with chat interface
├── data-pipeline/          # TomTom and NHTSA API connectors
└── docs/                   # Documentation and setup guides
```

### What's Actually Built ✅

- **Backend**: FastAPI with endpoints for risk scoring, insurance portfolio, live data, and AI chat
- **Frontend**: React dashboard with insurance portal, real-time data visualization, and floating AI chat widget
- **API Integrations**: Working TomTom Traffic API and NHTSA Vehicle Safety API connectors
- **AI Chat**: Personalized responses using real user data and intelligent pattern matching
- **Mock Data**: Realistic insurance and driving data for multiple user profiles

## 🛠️ Tech Stack

### Core Technologies Used
- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Frontend**: React 18, JavaScript, Tailwind CSS
- **APIs**: TomTom Traffic API, NHTSA Vehicle Safety API
- **AI**: Enhanced mock responses with real data integration (Vertex AI ready)
- **Development**: RESTful APIs, responsive design, real-time data simulation

## 🚦 Getting Started

### Quick Start (5 minutes)

1. **Backend Setup**
   ```bash
   cd backend
   pip install fastapi uvicorn requests
   uvicorn simple_main:app --host 0.0.0.0 --port 8005 --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   PORT=3000 npm start
   ```

3. **Access the Demo**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8005
   - Interactive chat widget in bottom-right corner

### With Real API Keys (Optional)

1. **Get API Keys**
   - TomTom: Sign up at developer.tomtom.com
   - No GCP setup required for basic demo

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add your TomTom API key
   ```

## 📊 Data Sources & Integration

### Real APIs Integrated ✅
- **TomTom Traffic API**: Real-time traffic data, congestion levels, city comparisons
- **NHTSA Vehicle API**: Vehicle safety ratings, recall information, manufacturer data
- **Live Data Simulation**: Real-time risk score updates and traffic condition monitoring

### Mock Data (For Demo) 📋
- **User Profiles**: 5 different driver personas with realistic data
- **Risk Metrics**: Dynamic risk scores based on driving behavior patterns
- **Safety Scores**: Comprehensive safety analysis with following distance, acceleration, speed adherence
- **Insurance Portfolio**: Complete insurance company dashboard with customer analytics

## 💬 AI Chat Assistant

### Personalized Responses Using Real Data
The AI chat uses actual user risk scores, safety metrics, and profile information to provide intelligent responses:

**Try asking:**
- "What is my safety score?" → Gets your actual score and breakdown
- "How risky is my driving?" → Analyzes your real risk factors
- "How can I save on insurance?" → Calculates potential savings based on your data
- "Give me tips to improve" → Personalized suggestions based on your weak areas
- "Hello there!" → Personalized greeting with your current stats

### Smart Features
- **Data-Driven**: Uses real user profiles (Sarah Chen, Mike Rodriguez, Emma Johnson, etc.)
- **Contextual**: Responses change based on actual risk scores and safety metrics
- **Personalized**: Addresses users by name and references their specific vehicle
- **Actionable**: Provides specific improvement tips based on actual driving patterns

## 📈 Dashboard Features

### Insurance Company Portal
- **Portfolio Overview**: Total customers, monthly revenue, risk distribution
- **Customer Analytics**: Individual customer risk profiles and premium calculations  
- **Real-time Updates**: Live data refresh with traffic and risk adjustments
- **Risk Management**: Visual risk distribution and trend analysis

### Individual User Dashboard
- **Risk Score Display**: Clear 0-100 scale with color-coded risk levels
- **Safety Metrics**: Following distance, smooth acceleration, speed adherence
- **Live Data Integration**: Real-time traffic impact on risk scores
- **Interactive Chat**: Floating AI assistant for instant insights

## 🎯 Demo Highlights

### What Makes This Special
1. **Real API Integration**: Actual TomTom and NHTSA data, not just mock APIs
2. **Intelligent AI Chat**: Uses real user data for personalized responses
3. **Live Data Simulation**: Real-time updates and traffic integration
4. **Professional UI**: Insurance-grade dashboard with comprehensive analytics
5. **Scalable Architecture**: Ready for production deployment

### Sample Users to Try
- **Sarah Chen** (user123): Excellent driver with low risk score
- **Mike Rodriguez** (user456): Average driver with room for improvement  
- **Emma Johnson** (user789): Tech-savvy driver with good safety habits
- **Lisa Thompson** (user202): Family driver with balanced metrics

## 🚀 Future Enhancements

### Vertex AI Integration Ready
- Code structure supports real Vertex AI integration
- Enhanced mock mode provides intelligent responses using actual user data
- Easy migration path to full Google Cloud deployment

### Expandable Features
- Additional API integrations (Smartcar, HERE Maps)
- BigQuery ML for advanced risk modeling
- Real telematics data integration
- Production insurance company features

## 📝 License

MIT License - Built for AI Accelerate Hackathon 2025