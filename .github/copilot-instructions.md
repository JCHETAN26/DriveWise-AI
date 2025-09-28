# DriveWise AI Project Instructions

This is a comprehensive AI-powered driving insights and insurance risk platform.

## Project Structure
- **Backend**: Python FastAPI for APIs and data processing
- **Data Pipeline**: Custom connectors for TomTom and NHTSA APIs
- **ML/AI**: BigQuery ML and Vertex AI for risk modeling
- **Frontend**: React dashboard for visualization
- **Agent**: Vertex AI conversational agent

## Development Guidelines
- Use environment variables for API keys and credentials
- Follow clean architecture patterns
- Implement proper error handling and logging
- Use type hints in Python code
- Follow React best practices for frontend

## Checklist Status:
- [x] Project structure created
- [x] Dependencies and requirements defined
- [x] Configuration setup (.env.example, docker-compose.yml)
- [x] Backend API structure (FastAPI with services)
- [x] Frontend scaffolding (React with TypeScript)
- [x] Data pipeline components (TomTom & NHTSA connectors)
- [x] BigQuery schema and ML models
- [x] Deployment configuration (Docker, setup script)
- [x] Comprehensive documentation
- [x] Project ready for development

## Next Steps:
1. Set up Google Cloud Project and service accounts
2. Configure API keys (TomTom, GCP credentials)
3. Run ./setup.sh to initialize the project
4. Start development with individual services
5. Test data ingestion and ML model training