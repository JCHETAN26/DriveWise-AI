#!/bin/bash

# Google Cloud Setup Script for DriveWise AI
# This script helps you set up Google Cloud Platform credentials and services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
  echo -e "${BLUE}===================================================${NC}"
  echo -e "${BLUE}$1${NC}"
  echo -e "${BLUE}===================================================${NC}"
}

print_step() {
  echo -e "${GREEN}[STEP]${NC} $1"
}

print_info() {
  echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
check_gcloud() {
  if ! command -v gcloud &> /dev/null; then
    print_error "Google Cloud CLI (gcloud) is not installed."
    echo
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    echo
    echo "For macOS:"
    echo "  curl https://sdk.cloud.google.com | bash"
    echo "  exec -l \$SHELL"
    echo
    echo "For Ubuntu/Debian:"
    echo "  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -"
    echo "  echo 'deb https://packages.cloud.google.com/apt cloud-sdk main' | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list"
    echo "  sudo apt-get update && sudo apt-get install google-cloud-sdk"
    exit 1
  fi
  
  print_success "Google Cloud CLI is installed: $(gcloud --version | head -n1)"
}

# Login to Google Cloud
gcloud_login() {
  print_step "Logging in to Google Cloud..."
  
  if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    print_info "No active Google Cloud authentication found. Starting login process..."
    gcloud auth login
  else
    ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
    print_success "Already logged in as: $ACTIVE_ACCOUNT"
  fi
}

# Set or create Google Cloud project
setup_project() {
  print_step "Setting up Google Cloud Project..."
  
  # Get current project
  CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
  
  if [ -z "$CURRENT_PROJECT" ]; then
    print_info "No project set. Let's create or select one."
    echo
    echo "Options:"
    echo "1. Create a new project"
    echo "2. Use existing project"
    echo
    read -p "Choose option (1 or 2): " choice
    
    if [ "$choice" = "1" ]; then
      read -p "Enter new project ID (e.g., drivewise-ai-12345): " PROJECT_ID
      print_info "Creating project: $PROJECT_ID"
      gcloud projects create $PROJECT_ID
      gcloud config set project $PROJECT_ID
    else
      print_info "Available projects:"
      gcloud projects list
      echo
      read -p "Enter project ID to use: " PROJECT_ID
      gcloud config set project $PROJECT_ID
    fi
  else
    PROJECT_ID=$CURRENT_PROJECT
    print_success "Using current project: $PROJECT_ID"
  fi
  
  # Update .env file with project ID
  if [ -f .env ]; then
    sed -i.bak "s/GCP_PROJECT_ID=.*/GCP_PROJECT_ID=$PROJECT_ID/" .env
    print_success "Updated .env file with project ID: $PROJECT_ID"
  fi
}

# Enable required APIs
enable_apis() {
  print_step "Enabling required Google Cloud APIs..."
  
  APIS=(
    "bigquery.googleapis.com"
    "aiplatform.googleapis.com" 
    "storage.googleapis.com"
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "logging.googleapis.com"
  )
  
  for api in "${APIS[@]}"; do
    print_info "Enabling $api..."
    gcloud services enable $api --quiet
  done
  
  print_success "All required APIs enabled!"
}

# Create service account
create_service_account() {
  print_step "Creating service account for DriveWise AI..."
  
  SERVICE_ACCOUNT_NAME="drivewise-ai-service"
  SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"
  KEY_FILE="./gcp-service-account-key.json"
  
  # Check if service account already exists
  if gcloud iam service-accounts describe $SERVICE_ACCOUNT_EMAIL &>/dev/null; then
    print_info "Service account already exists: $SERVICE_ACCOUNT_EMAIL"
  else
    print_info "Creating service account: $SERVICE_ACCOUNT_NAME"
    gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
      --display-name="DriveWise AI Service Account" \
      --description="Service account for DriveWise AI platform"
  fi
  
  # Grant necessary roles
  print_info "Granting IAM roles to service account..."
  
  ROLES=(
    "roles/bigquery.admin"
    "roles/aiplatform.user"
    "roles/storage.admin"
    "roles/logging.logWriter"
    "roles/monitoring.metricWriter"
  )
  
  for role in "${ROLES[@]}"; do
    gcloud projects add-iam-policy-binding $PROJECT_ID \
      --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
      --role="$role" \
      --quiet
  done
  
  # Create and download key file
  print_info "Creating service account key file..."
  
  if [ -f "$KEY_FILE" ]; then
    print_info "Key file already exists. Creating backup..."
    mv "$KEY_FILE" "$KEY_FILE.backup.$(date +%Y%m%d_%H%M%S)"
  fi
  
  gcloud iam service-accounts keys create $KEY_FILE \
    --iam-account=$SERVICE_ACCOUNT_EMAIL
  
  print_success "Service account key created: $KEY_FILE"
  
  # Update .env file
  if [ -f .env ]; then
    ABS_KEY_PATH=$(realpath $KEY_FILE)
    sed -i.bak "s|GOOGLE_APPLICATION_CREDENTIALS=.*|GOOGLE_APPLICATION_CREDENTIALS=$ABS_KEY_PATH|" .env
    print_success "Updated .env file with credentials path"
  fi
  
  # Set environment variable for current session
  export GOOGLE_APPLICATION_CREDENTIALS=$(realpath $KEY_FILE)
  
  print_success "Google Cloud setup complete!"
  echo
  print_info "Service Account: $SERVICE_ACCOUNT_EMAIL"
  print_info "Key File: $(realpath $KEY_FILE)"
  print_info "Project ID: $PROJECT_ID"
}

# Create BigQuery dataset
setup_bigquery() {
  print_step "Setting up BigQuery dataset..."
  
  DATASET_ID="drivewise_ai"
  
  # Check if dataset exists
  if bq ls -d $PROJECT_ID:$DATASET_ID &>/dev/null; then
    print_info "BigQuery dataset already exists: $DATASET_ID"
  else
    print_info "Creating BigQuery dataset: $DATASET_ID"
    bq mk --dataset --location=US $PROJECT_ID:$DATASET_ID
  fi
  
  print_success "BigQuery dataset ready: $PROJECT_ID:$DATASET_ID"
}

# Test the setup
test_setup() {
  print_step "Testing Google Cloud setup..."
  
  # Test authentication
  print_info "Testing authentication..."
  if gcloud auth application-default print-access-token &>/dev/null; then
    print_success "✓ Authentication working"
  else
    print_error "✗ Authentication failed"
    return 1
  fi
  
  # Test BigQuery access
  print_info "Testing BigQuery access..."
  if bq ls &>/dev/null; then
    print_success "✓ BigQuery access working"
  else
    print_error "✗ BigQuery access failed"
    return 1
  fi
  
  # Test Vertex AI access (basic check)
  print_info "Testing Vertex AI access..."
  if gcloud ai models list --region=us-central1 &>/dev/null; then
    print_success "✓ Vertex AI access working"
  else
    print_info "⚠ Vertex AI access check skipped (may require additional setup)"
  fi
  
  print_success "Google Cloud setup test completed!"
}

# Main function
main() {
  print_header "Google Cloud Setup for DriveWise AI"
  
  check_gcloud
  gcloud_login
  setup_project
  enable_apis
  create_service_account
  setup_bigquery
  test_setup
  
  print_header "Setup Complete!"
  
  echo -e "${GREEN}🎉 Google Cloud Platform is now configured for DriveWise AI!${NC}"
  echo
  echo -e "${BLUE}What was created:${NC}"
  echo "• Service Account: drivewise-ai-service@$PROJECT_ID.iam.gserviceaccount.com"
  echo "• Service Account Key: ./gcp-service-account-key.json"
  echo "• BigQuery Dataset: $PROJECT_ID:drivewise_ai"
  echo "• Required APIs enabled"
  echo
  echo -e "${BLUE}Next steps:${NC}"
  echo "1. Copy .env.example to .env (if not done already)"
  echo "2. The .env file has been updated with your project ID and credentials path"
  echo "3. Get your TomTom API key from: https://developer.tomtom.com/"
  echo "4. Run: ./setup.sh to complete the platform setup"
  echo
  echo -e "${YELLOW}Important:${NC}"
  echo "• Keep your service account key file secure"
  echo "• Add *.json to your .gitignore to avoid committing credentials"
  echo "• The key file is already in the correct location for the DriveWise AI platform"
}

# Run the main function
main "$@"