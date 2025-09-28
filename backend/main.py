from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime, timedelta
import logging

from services.data_service import DataService
from services.ml_service import MLService
from services.bigquery_service import BigQueryService
from services.vertex_ai_service import VertexAIService
from models.driving_data import DrivingData, RiskScore, SafetyScore
from utils.auth import verify_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DriveWise AI API",
    description="AI-powered driving insights and insurance risk platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://drivewise-ai.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Services
data_service = DataService()
ml_service = MLService()
bigquery_service = BigQueryService()
vertex_ai_service = VertexAIService()

# Pydantic models
class DrivingQuery(BaseModel):
    user_id: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ChatQuery(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class RiskScoreRequest(BaseModel):
    user_id: str
    driving_data: Dict[str, Any]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "DriveWise AI API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {
            "bigquery": await bigquery_service.health_check(),
            "vertex_ai": await vertex_ai_service.health_check()
        }
    }

@app.post("/api/v1/driving-data")
async def upload_driving_data(
    data: DrivingData,
    background_tasks: BackgroundTasks,
    token: str = Depends(security)
):
    """Upload driving data for processing"""
    try:
        user_id = verify_token(token.credentials)
        
        # Store data in BigQuery
        result = await bigquery_service.insert_driving_data(data.dict())
        
        # Trigger ML processing in background
        background_tasks.add_task(
            ml_service.process_driving_data, 
            user_id, 
            data.dict()
        )
        
        return {"status": "success", "message": "Data uploaded successfully"}
    
    except Exception as e:
        logger.error(f"Error uploading driving data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/risk-score/{user_id}")
async def get_risk_score(
    user_id: str,
    token: str = Depends(security)
):
    """Get current risk score for a user"""
    try:
        # Verify user access
        verified_user = verify_token(token.credentials)
        if verified_user != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get risk score from ML service
        risk_score = await ml_service.get_risk_score(user_id)
        
        return {
            "user_id": user_id,
            "risk_score": risk_score,
            "timestamp": datetime.utcnow()
        }
    
    except Exception as e:
        logger.error(f"Error getting risk score: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/safety-score/{user_id}")
async def get_safety_score(
    user_id: str,
    token: str = Depends(security)
):
    """Get personalized safety score for a user"""
    try:
        verified_user = verify_token(token.credentials)
        if verified_user != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        safety_score = await ml_service.get_safety_score(user_id)
        
        return {
            "user_id": user_id,
            "safety_score": safety_score,
            "timestamp": datetime.utcnow()
        }
    
    except Exception as e:
        logger.error(f"Error getting safety score: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/chat")
async def chat_with_agent(
    query: ChatQuery,
    token: str = Depends(security)
):
    """Chat with the DriveWise AI conversational agent"""
    try:
        verified_user = verify_token(token.credentials)
        if verified_user != query.user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get user context
        user_context = await data_service.get_user_context(query.user_id)
        
        # Query Vertex AI agent
        response = await vertex_ai_service.chat(
            query.message, 
            user_context, 
            query.context
        )
        
        return {
            "response": response,
            "timestamp": datetime.utcnow()
        }
    
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/dashboard/{user_id}")
async def get_dashboard_data(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    token: str = Depends(security)
):
    """Get dashboard data for visualization"""
    try:
        verified_user = verify_token(token.credentials)
        if verified_user != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Set default date range if not provided
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Get dashboard data
        dashboard_data = await data_service.get_dashboard_data(
            user_id, start_date, end_date
        )
        
        return dashboard_data
    
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/traffic-hotspots")
async def get_traffic_hotspots(
    lat: float,
    lon: float,
    radius: float = 10.0,
    token: str = Depends(security)
):
    """Get traffic hotspots in a geographic area"""
    try:
        verify_token(token.credentials)
        
        hotspots = await data_service.get_traffic_hotspots(lat, lon, radius)
        
        return {
            "hotspots": hotspots,
            "center": {"lat": lat, "lon": lon},
            "radius": radius
        }
    
    except Exception as e:
        logger.error(f"Error getting traffic hotspots: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/batch-process")
async def batch_process_data(
    background_tasks: BackgroundTasks,
    token: str = Depends(security)
):
    """Trigger batch processing of data"""
    try:
        verify_token(token.credentials)
        
        background_tasks.add_task(data_service.batch_process_data)
        
        return {"status": "success", "message": "Batch processing started"}
    
    except Exception as e:
        logger.error(f"Error starting batch process: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)