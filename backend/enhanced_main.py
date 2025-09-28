"""
Enhanced backend with real-time traffic integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import json
import os
import requests
import asyncio

# Import our real-time connector
import sys
sys.path.append('.')
from real_time_traffic import RealTimeTomTomConnector, MAJOR_CITIES

# Initialize FastAPI app
app = FastAPI(
    title="DriveWise AI API - Real-Time Enhanced",
    description="AI-powered driving insights with live traffic data",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize real-time traffic connector
try:
    traffic_connector = RealTimeTomTomConnector()
    REAL_TIME_ENABLED = True
    print("✅ Real-time traffic data enabled!")
except Exception as e:
    traffic_connector = None
    REAL_TIME_ENABLED = False
    print(f"⚠️ Real-time traffic disabled: {e}")

# Enhanced user profiles with locations
ENHANCED_USERS = {
    "user123": {
        "name": "Sarah Chen",
        "email": "sarah.chen@email.com",
        "vehicle": "2020 Honda Civic",
        "age": 32,
        "location": "San Francisco, CA",
        "coordinates": (37.7749, -122.4194),
        "driving_experience": 14,
        "profile_type": "safe_driver"
    },
    "user456": {
        "name": "Mike Rodriguez",
        "email": "mike.rodriguez@email.com", 
        "vehicle": "2018 Ford F-150",
        "age": 28,
        "location": "Austin, TX",
        "coordinates": (30.2672, -97.7431),
        "driving_experience": 10,
        "profile_type": "average_driver"
    },
    "user789": {
        "name": "Emma Johnson",
        "email": "emma.johnson@email.com",
        "vehicle": "2022 Tesla Model 3",
        "age": 26,
        "location": "Seattle, WA",
        "coordinates": (47.6062, -122.3321),
        "driving_experience": 8,
        "profile_type": "tech_savvy_driver"
    },
    "user101": {
        "name": "David Kim",
        "email": "david.kim@email.com",
        "vehicle": "2019 BMW 330i",
        "age": 45,
        "location": "New York, NY",
        "coordinates": (40.7128, -74.0060),
        "driving_experience": 27,
        "profile_type": "experienced_driver"
    },
    "user202": {
        "name": "Lisa Thompson",
        "email": "lisa.thompson@email.com",
        "vehicle": "2021 Subaru Outback",
        "age": 35,
        "location": "Denver, CO",
        "coordinates": (39.7392, -104.9903),
        "driving_experience": 17,
        "profile_type": "family_driver"
    }
}

async def get_real_time_enhanced_risk_score(user_id: str) -> Dict[str, Any]:
    """Enhanced risk scoring with real-time traffic data"""
    user = ENHANCED_USERS.get(user_id, {})
    profile_type = user.get("profile_type", "average_driver")
    coordinates = user.get("coordinates", (37.7749, -122.4194))
    
    # Base risk profiles
    base_risk_profiles = {
        "safe_driver": {"overall": (0.10, 0.20), "speeding": (0.05, 0.15)},
        "average_driver": {"overall": (0.20, 0.35), "speeding": (0.15, 0.30)},
        "tech_savvy_driver": {"overall": (0.12, 0.25), "speeding": (0.08, 0.20)},
        "experienced_driver": {"overall": (0.15, 0.28), "speeding": (0.10, 0.22)},
        "family_driver": {"overall": (0.18, 0.30), "speeding": (0.12, 0.25)}
    }
    
    profile = base_risk_profiles.get(profile_type, base_risk_profiles["average_driver"])
    base_score = random.uniform(*profile["overall"])
    
    # Get real-time traffic data if available
    traffic_adjustment = 0.0
    real_time_data = None
    
    if REAL_TIME_ENABLED and traffic_connector:
        try:
            lat, lon = coordinates
            real_time_data = await traffic_connector.get_live_traffic_flow(lat, lon)
            
            # Adjust risk based on current traffic conditions
            congestion = real_time_data.get("congestion_level", 0.0)
            
            # Higher congestion = higher risk (more stress, aggressive driving)
            traffic_adjustment = congestion * 0.05  # Up to 5% increase
            
        except Exception as e:
            print(f"Real-time data error: {e}")
    
    final_score = min(1.0, base_score + traffic_adjustment)
    
    return {
        "user_id": user_id,
        "overall_score": round(final_score, 3),
        "risk_factors": {
            "speeding_score": round(random.uniform(*profile.get("speeding", (0.1, 0.3))), 3),
            "hard_braking_score": round(random.uniform(0.15, 0.4), 3),
            "acceleration_score": round(random.uniform(0.12, 0.28), 3),
            "distraction_score": round(random.uniform(0.05, 0.2), 3),
            "time_of_day_score": round(random.uniform(0.15, 0.35), 3),
            "weather_score": round(random.uniform(0.20, 0.40), 3),
            "traffic_score": round(traffic_adjustment, 3)
        },
        "real_time_data": real_time_data,
        "traffic_adjustment": round(traffic_adjustment, 3),
        "confidence": round(random.uniform(0.82, 0.94), 2),
        "timestamp": datetime.now().isoformat(),
        "data_source": "live_traffic" if real_time_data else "historical"
    }

# API Routes
@app.get("/")
async def root():
    return {
        "message": "DriveWise AI API - Real-Time Traffic Enhanced!",
        "status": "healthy",
        "real_time_enabled": REAL_TIME_ENABLED,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/api/v1/users")
async def list_all_users():
    """Get all demo users"""
    return {
        "users": [
            {
                "user_id": user_id,
                **{k: v for k, v in user_data.items() if k != "coordinates"}  # Hide coordinates from frontend
            }
            for user_id, user_data in ENHANCED_USERS.items()
        ],
        "total_users": len(ENHANCED_USERS),
        "real_time_enabled": REAL_TIME_ENABLED
    }

@app.get("/api/v1/risk-score/{user_id}")
async def get_enhanced_risk_score(user_id: str):
    """Get enhanced risk score with real-time traffic data"""
    if user_id not in ENHANCED_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await get_real_time_enhanced_risk_score(user_id)

@app.get("/api/v1/live-traffic/{user_id}")
async def get_user_live_traffic(user_id: str):
    """Get live traffic data for user's location"""
    if user_id not in ENHANCED_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not REAL_TIME_ENABLED:
        return {"error": "Real-time traffic data not available", "enabled": False}
    
    user = ENHANCED_USERS[user_id]
    lat, lon = user["coordinates"]
    
    try:
        traffic_data = await traffic_connector.get_live_traffic_flow(lat, lon)
        incidents = await traffic_connector.get_live_incidents(lat, lon, 10.0)
        
        return {
            "user_id": user_id,
            "location": user["location"],
            "traffic_flow": traffic_data,
            "incidents": incidents,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live traffic: {str(e)}")

@app.get("/api/v1/city-traffic-comparison")
async def get_city_traffic_comparison():
    """Compare live traffic across all major cities"""
    if not REAL_TIME_ENABLED:
        return {"error": "Real-time traffic data not available", "enabled": False}
    
    city_traffic = {}
    
    for user_id, user_data in ENHANCED_USERS.items():
        city = user_data["location"].split(",")[0]
        lat, lon = user_data["coordinates"]
        
        try:
            traffic_data = await traffic_connector.get_live_traffic_flow(lat, lon)
            city_traffic[city] = {
                "user_example": user_data["name"],
                "current_speed": traffic_data["current_speed"],
                "congestion_level": traffic_data["congestion_level"],
                "source": traffic_data["source"]
            }
        except Exception as e:
            city_traffic[city] = {"error": str(e)}
        
        # Be nice to the API
        await asyncio.sleep(0.5)
    
    return {
        "cities": city_traffic,
        "timestamp": datetime.now().isoformat(),
        "data_source": "tomtom_live"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚗 Starting DriveWise AI Backend with Real-Time Traffic...")
    print("📊 Dashboard: http://localhost:3004")  
    print("🔗 API docs: http://localhost:8004/docs")
    print(f"🌐 Real-time traffic: {'✅ ENABLED' if REAL_TIME_ENABLED else '❌ DISABLED'}")
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=True)