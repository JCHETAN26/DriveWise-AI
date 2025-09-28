#!/bin/bash

# DriveWise AI Setup Script
# This script sets up the complete DriveWise AI platform

set -e

echo "🚗 Setting up DriveWise AI Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
  echo -e "${BLUE}===================================================${NC}"
  echo -e "${BLUE}$1${NC}"
  echo -e "${BLUE}===================================================${NC}"
}

# Check if required tools are installed
check_requirements() {
  print_header "Checking Requirements"
  
  # Check Python
  if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed."
    exit 1
  fi
  print_status "Python 3: $(python3 --version)"
  
  # Check Node.js
  if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed."
    exit 1
  fi
  print_status "Node.js: $(node --version)"
  
  # Check Docker
  if ! command -v docker &> /dev/null; then
    print_warning "Docker not found. Some features may not work."
  else
    print_status "Docker: $(docker --version)"
  fi
  
  # Check gcloud CLI
  if ! command -v gcloud &> /dev/null; then
    print_warning "Google Cloud CLI not found. You'll need it for GCP features."
  else
    print_status "Google Cloud CLI: $(gcloud --version | head -n1)"
  fi
}

# Setup environment
setup_environment() {
  print_header "Setting Up Environment"
  
  # Create .env file if it doesn't exist
  if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your actual configuration values"
  else
    print_status ".env file already exists"
  fi
  
  # Create necessary directories
  mkdir -p logs
  mkdir -p data
  mkdir -p ml-models/notebooks
  mkdir -p infrastructure/ssl
  
  print_status "Environment setup complete"
}

# Setup Python backend
setup_backend() {
  print_header "Setting Up Python Backend"
  
  cd backend
  
  # Create virtual environment
  if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
  fi
  
  # Activate virtual environment and install dependencies
  print_status "Installing Python dependencies..."
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  
  # Run database migrations (if applicable)
  # python manage.py migrate
  
  cd ..
  print_status "Backend setup complete"
}

# Setup React frontend
setup_frontend() {
  print_header "Setting Up React Frontend"
  
  cd frontend
  
  # Install Node.js dependencies
  print_status "Installing Node.js dependencies..."
  npm install
  
  # Build for production (optional)
  # npm run build
  
  cd ..
  print_status "Frontend setup complete"
}

# Setup data pipeline
setup_data_pipeline() {
  print_header "Setting Up Data Pipeline"
  
  cd data-pipeline
  
  # Create virtual environment for data pipeline
  if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment for data pipeline..."
    python3 -m venv venv
  fi
  
  # Install dependencies
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  
  cd ..
  print_status "Data pipeline setup complete"
}

# Setup BigQuery
setup_bigquery() {
  print_header "Setting Up BigQuery"
  
  if command -v gcloud &> /dev/null; then
    print_status "Setting up BigQuery dataset and tables..."
    
    # Load environment variables
    if [ -f .env ]; then
      export $(cat .env | grep -v '#' | awk '{print $1}')
    fi
    
    # Create BigQuery dataset and tables
    print_status "Creating BigQuery schema..."
    bq query --use_legacy_sql=false < ml-models/bigquery_schema.sql
    
    print_status "BigQuery setup complete"
  else
    print_warning "Google Cloud CLI not available. Skipping BigQuery setup."
    print_warning "You'll need to manually run the SQL in ml-models/bigquery_schema.sql"
  fi
}

# Setup Docker containers
setup_docker() {
  print_header "Setting Up Docker Environment"
  
  if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    print_status "Building Docker containers..."
    docker-compose build
    
    print_status "Docker setup complete"
    print_status "To start all services, run: docker-compose up -d"
  else
    print_warning "Docker or Docker Compose not available. Skipping Docker setup."
  fi
}

# Create sample data
create_sample_data() {
  print_header "Creating Sample Data"
  
  # Create sample driving data
  cat > data/sample_driving_data.json << 'EOF'
{
  "user_id": "user123",
  "vehicle": {
    "make": "Honda",
    "model": "Civic",
    "year": 2020,
    "vin": "1HGBH41JXMN109186"
  },
  "trip": {
    "trip_id": "trip001",
    "start_time": "2024-01-15T08:30:00Z",
    "end_time": "2024-01-15T09:15:00Z",
    "start_location": {"latitude": 37.7749, "longitude": -122.4194},
    "end_location": {"latitude": 37.4419, "longitude": -122.1430},
    "distance": 45.2,
    "duration": 2700,
    "avg_speed": 60.3,
    "max_speed": 85.0,
    "events": [
      {
        "event_type": "hard_brake",
        "timestamp": "2024-01-15T08:45:00Z",
        "location": {"latitude": 37.6879, "longitude": -122.3017},
        "severity": 0.7,
        "speed": 45.0
      }
    ],
    "weather_conditions": "clear",
    "traffic_conditions": "moderate"
  }
}
EOF
  
  print_status "Sample data created in data/ directory"
}

# Print final instructions
print_final_instructions() {
  print_header "Setup Complete!"
  
  echo -e "${GREEN}✅ DriveWise AI platform has been set up successfully!${NC}"
  echo
  echo -e "${BLUE}Next Steps:${NC}"
  echo "1. Edit the .env file with your API keys and configuration"
  echo "2. Set up your Google Cloud Project and service account"
  echo "3. Configure your TomTom API key for traffic data"
  echo "4. Start the services:"
  echo
  echo -e "${YELLOW}Development Mode:${NC}"
  echo "  Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
  echo "  Frontend: cd frontend && npm start"
  echo
  echo -e "${YELLOW}Production Mode (Docker):${NC}"
  echo "  docker-compose up -d"
  echo
  echo -e "${BLUE}Access Points:${NC}"
  echo "  Frontend: http://localhost:3000"
  echo "  Backend API: http://localhost:8000"
  echo "  API Docs: http://localhost:8000/docs"
  echo "  Jupyter Notebooks: http://localhost:8888"
  echo
  echo -e "${BLUE}Important Files:${NC}"
  echo "  .env - Environment configuration"
  echo "  ml-models/bigquery_schema.sql - Database setup"
  echo "  data/sample_driving_data.json - Sample data"
  echo
  echo -e "${GREEN}Happy driving! 🚗💨${NC}"
}

# Main execution
main() {
  print_header "DriveWise AI Platform Setup"
  
  check_requirements
  setup_environment
  setup_backend
  setup_frontend
  setup_data_pipeline
  setup_bigquery
  setup_docker
  create_sample_data
  print_final_instructions
}

# Run main function
main "$@"