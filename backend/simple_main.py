#!/usr/bin/env python3

"""
DriveWise AI - Simple FastAPI Backend for Hackathon Demo
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import json
import os
from nhtsa_connector import NHTSAConnector

# Initialize FastAPI app
app = FastAPI(
    title="DriveWise AI API",
    description="AI-powered driving insights and insurance risk platform with NHTSA integration",
    version="1.1.0"
)

# Initialize NHTSA connector
nhtsa = NHTSAConnector()

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class DrivingQuery(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str

class RiskScore(BaseModel):
    user_id: str
    overall_score: float
    risk_factors: Dict[str, float]
    timestamp: str

class SafetyScore(BaseModel):
    user_id: str
    overall_score: float
    safety_metrics: Dict[str, float]
    timestamp: str

# Mock data for demo - Multiple realistic user profiles
MOCK_USERS = {
    "user123": {
        "name": "Sarah Chen",
        "email": "sarah.chen@email.com",
        "vehicle": "2020 Honda Civic",
        "age": 32,
        "location": "San Francisco, CA",
        "driving_experience": 14,
        "profile_type": "safe_driver"
    },
    "user456": {
        "name": "Mike Rodriguez",
        "email": "mike.rodriguez@email.com", 
        "vehicle": "2018 Ford F-150",
        "age": 28,
        "location": "Austin, TX",
        "driving_experience": 10,
        "profile_type": "average_driver"
    },
    "user789": {
        "name": "Emma Johnson",
        "email": "emma.johnson@email.com",
        "vehicle": "2022 Tesla Model 3",
        "age": 26,
        "location": "Seattle, WA", 
        "driving_experience": 8,
        "profile_type": "tech_savvy_driver"
    },
    "user101": {
        "name": "David Kim",
        "email": "david.kim@email.com",
        "vehicle": "2019 BMW 330i",
        "age": 45,
        "location": "New York, NY",
        "driving_experience": 27,
        "profile_type": "experienced_driver"
    },
    "user202": {
        "name": "Lisa Thompson",
        "email": "lisa.thompson@email.com",
        "vehicle": "2021 Subaru Outback",
        "age": 35,
        "location": "Denver, CO",
        "driving_experience": 17,
        "profile_type": "family_driver"
    }
}

def get_mock_risk_score(user_id: str) -> Dict[str, Any]:
    """Generate mock risk score data based on user profile"""
    # Get user profile to determine risk characteristics
    user_profile = MOCK_USERS.get(user_id, {}).get("profile_type", "average_driver")
    
    # Define risk ranges based on driver profile
    risk_profiles = {
        "safe_driver": {
            "overall": (0.10, 0.20),
            "speeding": (0.05, 0.15),
            "braking": (0.08, 0.18),
            "acceleration": (0.06, 0.16),
            "distraction": (0.02, 0.12)
        },
        "average_driver": {
            "overall": (0.20, 0.35),
            "speeding": (0.15, 0.30),
            "braking": (0.18, 0.35),
            "acceleration": (0.12, 0.28),
            "distraction": (0.08, 0.22)
        },
        "tech_savvy_driver": {
            "overall": (0.12, 0.25),
            "speeding": (0.08, 0.20),
            "braking": (0.10, 0.22),
            "acceleration": (0.08, 0.20),
            "distraction": (0.03, 0.15)
        },
        "experienced_driver": {
            "overall": (0.15, 0.28),
            "speeding": (0.10, 0.22),
            "braking": (0.12, 0.25),
            "acceleration": (0.10, 0.24),
            "distraction": (0.05, 0.18)
        },
        "family_driver": {
            "overall": (0.18, 0.30),
            "speeding": (0.12, 0.25),
            "braking": (0.15, 0.28),
            "acceleration": (0.10, 0.22),
            "distraction": (0.06, 0.20)
        }
    }
    
    profile = risk_profiles.get(user_profile, risk_profiles["average_driver"])
    
    return {
        "user_id": user_id,
        "overall_score": round(random.uniform(*profile["overall"]), 3),
        "risk_factors": {
            "speeding_score": round(random.uniform(*profile["speeding"]), 3),
            "hard_braking_score": round(random.uniform(*profile["braking"]), 3),
            "acceleration_score": round(random.uniform(*profile["acceleration"]), 3),
            "distraction_score": round(random.uniform(*profile["distraction"]), 3),
            "time_of_day_score": round(random.uniform(0.15, 0.35), 3),
            "weather_score": round(random.uniform(0.20, 0.40), 3),
            "traffic_score": round(random.uniform(0.25, 0.45), 3)
        },
        "confidence": round(random.uniform(0.82, 0.94), 2),
        "timestamp": datetime.now().isoformat()
    }

def get_mock_safety_score(user_id: str) -> Dict[str, Any]:
    """Generate mock safety score data based on user profile"""
    user_profile = MOCK_USERS.get(user_id, {}).get("profile_type", "average_driver")
    user_name = MOCK_USERS.get(user_id, {}).get("name", "User")
    
    # Define safety score ranges based on driver profile
    safety_profiles = {
        "safe_driver": {
            "overall": (85, 95),
            "following_distance": (0.85, 0.95),
            "smooth_acceleration": (0.88, 0.98),
            "smooth_braking": (0.86, 0.96),
            "speed_adherence": (0.80, 0.92),
            "defensive_driving": (0.85, 0.95),
            "attention": (0.90, 0.98),
            "ranking": (80, 95),
            "suggestions": [
                "Excellent driving! Consider sharing tips with other drivers",
                "Your safety habits are exemplary",
                "Keep up the outstanding defensive driving"
            ]
        },
        "average_driver": {
            "overall": (70, 85),
            "following_distance": (0.70, 0.85),
            "smooth_acceleration": (0.75, 0.90),
            "smooth_braking": (0.72, 0.87),
            "speed_adherence": (0.65, 0.80),
            "defensive_driving": (0.70, 0.85),
            "attention": (0.75, 0.90),
            "ranking": (50, 75),
            "suggestions": [
                "Maintain greater following distance on highways",
                "Reduce speed variations during city driving", 
                "Practice smoother braking in traffic"
            ]
        },
        "tech_savvy_driver": {
            "overall": (78, 92),
            "following_distance": (0.80, 0.92),
            "smooth_acceleration": (0.82, 0.94),
            "smooth_braking": (0.80, 0.93),
            "speed_adherence": (0.75, 0.88),
            "defensive_driving": (0.78, 0.90),
            "attention": (0.85, 0.96),
            "ranking": (65, 88),
            "suggestions": [
                "Use your vehicle's safety features more consistently",
                "Your tech awareness translates to safer driving",
                "Consider eco-driving modes for smoother acceleration"
            ]
        },
        "experienced_driver": {
            "overall": (75, 88),
            "following_distance": (0.78, 0.90),
            "smooth_acceleration": (0.80, 0.92),
            "smooth_braking": (0.82, 0.94),
            "speed_adherence": (0.72, 0.86),
            "defensive_driving": (0.85, 0.95),
            "attention": (0.80, 0.92),
            "ranking": (60, 82),
            "suggestions": [
                "Your experience shows in defensive driving",
                "Consider adapting to modern traffic patterns",
                "Excellent hazard recognition skills"
            ]
        },
        "family_driver": {
            "overall": (72, 86),
            "following_distance": (0.75, 0.88),
            "smooth_acceleration": (0.78, 0.90),
            "smooth_braking": (0.76, 0.89),
            "speed_adherence": (0.70, 0.84),
            "defensive_driving": (0.80, 0.92),
            "attention": (0.78, 0.90),
            "ranking": (55, 78),
            "suggestions": [
                "Great job prioritizing passenger safety",
                "Your cautious approach benefits your family",
                "Consider practicing emergency maneuvers"
            ]
        }
    }
    
    profile = safety_profiles.get(user_profile, safety_profiles["average_driver"])
    
    return {
        "user_id": user_id,
        "overall_score": round(random.uniform(*profile["overall"]), 1),
        "safety_metrics": {
            "safe_following_distance": round(random.uniform(*profile["following_distance"]), 3),
            "smooth_acceleration": round(random.uniform(*profile["smooth_acceleration"]), 3),
            "smooth_braking": round(random.uniform(*profile["smooth_braking"]), 3),
            "speed_limit_adherence": round(random.uniform(*profile["speed_adherence"]), 3),
            "defensive_driving": round(random.uniform(*profile["defensive_driving"]), 3),
            "attention_level": round(random.uniform(*profile["attention"]), 3)
        },
        "improvement_suggestions": profile["suggestions"],
        "comparative_ranking": random.randint(*profile["ranking"]),
        "timestamp": datetime.now().isoformat()
    }

def get_mock_dashboard_data(user_id: str) -> Dict[str, Any]:
    """Generate mock dashboard data based on user profile"""
    user_profile = MOCK_USERS.get(user_id, {}).get("profile_type", "average_driver")
    user_location = MOCK_USERS.get(user_id, {}).get("location", "Unknown")
    
    # Define trip patterns based on driver profile and location
    trip_patterns = {
        "safe_driver": {
            "events_likelihood": 0.1,
            "speed_range": (40, 70),
            "distance_range": (15, 35),
            "common_events": ["smooth_drive"],
            "routes": ["Home to Work", "Work to Grocery", "Weekend Errands"]
        },
        "average_driver": {
            "events_likelihood": 0.3,
            "speed_range": (45, 85),
            "distance_range": (18, 45),
            "common_events": ["hard_brake", "speeding", "rapid_acceleration"],
            "routes": ["Daily Commute", "Shopping Trip", "Social Visit"]
        },
        "tech_savvy_driver": {
            "events_likelihood": 0.15,
            "speed_range": (42, 75),
            "distance_range": (20, 40),
            "common_events": ["eco_driving", "adaptive_cruise"],
            "routes": ["Tech Campus Commute", "Coffee Run", "Gym Visit"]
        },
        "experienced_driver": {
            "events_likelihood": 0.2,
            "speed_range": (38, 78),
            "distance_range": (25, 50),
            "common_events": ["defensive_driving", "weather_adjusted"],
            "routes": ["Long Commute", "Business Meeting", "Family Visit"]
        },
        "family_driver": {
            "events_likelihood": 0.25,
            "speed_range": (35, 70),  
            "distance_range": (12, 30),
            "common_events": ["school_zone_slow", "careful_parking"],
            "routes": ["School Drop-off", "Soccer Practice", "Family Outing"]
        }
    }
    
    pattern = trip_patterns.get(user_profile, trip_patterns["average_driver"])
    
    # Generate 3 recent trips
    recent_trips = []
    base_date = datetime.now()
    
    for i in range(3):
        trip_date = base_date - timedelta(days=i+1, hours=random.randint(0, 12))
        distance = round(random.uniform(*pattern["distance_range"]), 1)
        avg_speed = round(random.uniform(*pattern["speed_range"]), 1)
        max_speed = round(avg_speed * random.uniform(1.1, 1.4), 1)
        duration = int((distance / avg_speed) * 60)  # Convert to minutes
        
        # Determine events based on profile likelihood
        events = []
        if random.random() < pattern["events_likelihood"]:
            events = random.sample(pattern["common_events"], min(2, len(pattern["common_events"])))
        
        trip = {
            "trip_id": f"trip_{user_id}_{i+1:03d}",
            "timestamp": trip_date.isoformat() + "Z",
            "distance_km": distance,
            "avg_speed_kmh": avg_speed,
            "max_speed_kmh": max_speed,
            "duration_minutes": duration,
            "events": events,
            "route_description": random.choice(pattern["routes"]),
            "location": user_location.split(",")[0]  # City only
        }
        recent_trips.append(trip)
    
    return {
        "recent_trips": recent_trips,
        "trends": [
            {"date": "2024-01-08", "risk_score": 0.28, "safety_score": 75},
            {"date": "2024-01-09", "risk_score": 0.25, "safety_score": 78},
            {"date": "2024-01-10", "risk_score": 0.22, "safety_score": 82},
            {"date": "2024-01-11", "risk_score": 0.24, "safety_score": 79},
            {"date": "2024-01-12", "risk_score": 0.21, "safety_score": 84},
            {"date": "2024-01-13", "risk_score": 0.23, "safety_score": 81},
            {"date": "2024-01-14", "risk_score": 0.20, "safety_score": 86}
        ],
        "insurance_quote": {
            "base_premium": 1200.00,
            "risk_adjustment": -0.18,
            "final_premium": 984.00,
            "savings": 216.00,
            "savings_percentage": 18.0,
            "quote_valid_until": "2024-02-15T00:00:00Z"
        }
    }

def generate_ai_response(message: str, user_id: str) -> str:
    """Generate mock AI responses based on message content"""
    message_lower = message.lower()
    
    responses = {
        "safety": f"Your current safety score is 84/100! You're doing great with smooth acceleration (91%) and following distance (82%). To improve further, try maintaining more consistent speeds during city driving.",
        
        "risk": f"Your risk score is 0.23 (lower is better), which puts you in the 'low risk' category. Your strongest area is distraction management, but watch out for hard braking events - you've had 3 this week.",
        
        "insurance": f"Based on your driving pattern, you could save $216 annually! Your safe driving habits qualify you for an 18% discount. Keep up the good work with defensive driving.",
        
        "today": f"Today's driving summary: 2 trips, 43.4 km total distance. Your safety score improved by 2 points! I noticed smoother braking in traffic - excellent improvement.",
        
        "improve": f"Here are 3 ways to boost your scores: 1) Increase following distance on highways, 2) Reduce speed variations in city driving, 3) Practice gentler acceleration from stops.",
        
        "compare": f"You're driving safer than 78% of similar drivers in your area! Your speed limit adherence (76%) is above average, and your smooth acceleration (91%) is in the top 20%.",
        
        "hotspots": f"I've identified 3 high-risk areas on your common routes: Highway 101 near downtown (heavy congestion), Market Street intersection (frequent hard braking), and the Van Ness merge point.",
        
        "default": f"I'm your DriveWise AI assistant! I can help you understand your driving patterns, safety scores, and ways to save on insurance. What would you like to know about your driving?"
    }
    
    # Match keywords to responses
    for keyword, response in responses.items():
        if keyword in message_lower and keyword != "default":
            return response
    
    return responses["default"]

# API Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "DriveWise AI API is running!",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "mock_data": "available"
        }
    }

@app.get("/api/v1/risk-score/{user_id}")
async def get_risk_score(user_id: str):
    """Get risk score for a user"""
    return get_mock_risk_score(user_id)

@app.get("/api/v1/safety-score/{user_id}")
async def get_safety_score(user_id: str):
    """Get safety score for a user"""
    return get_mock_safety_score(user_id)

@app.get("/api/v1/dashboard/{user_id}")
async def get_dashboard_data(user_id: str):
    """Get dashboard data for a user"""
    return get_mock_dashboard_data(user_id)

@app.post("/api/v1/chat")
async def chat_with_ai(query: DrivingQuery):
    """Chat with DriveWise AI assistant"""
    response_text = generate_ai_response(query.message, query.user_id)
    
    return {
        "response": response_text,
        "timestamp": datetime.now().isoformat(),
        "user_id": query.user_id
    }

@app.get("/api/v1/traffic-hotspots")
async def get_traffic_hotspots(lat: float = 37.7749, lon: float = -122.4194, radius: float = 25.0):
    """Get traffic hotspots in a geographic area"""
    return {
        "hotspots": [
            {
                "lat": 37.7849,
                "lon": -122.4094,
                "congestion_level": 0.85,
                "incident_count": 12,
                "avg_speed": 15.2,
                "description": "Highway 101 - Downtown SF"
            },
            {
                "lat": 37.7649,
                "lon": -122.4294,
                "congestion_level": 0.72,
                "incident_count": 8,
                "avg_speed": 22.8,
                "description": "Market Street - Financial District"
            },
            {
                "lat": 37.7549,
                "lon": -122.4394,
                "congestion_level": 0.68,
                "incident_count": 5,
                "avg_speed": 28.5,
                "description": "Van Ness Avenue - Civic Center"
            }
        ],
        "center": {"lat": lat, "lon": lon},
        "radius": radius,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/users")
async def list_all_users():
    """Get all demo users for presentation"""
    return {
        "users": [
            {
                "user_id": user_id,
                **user_data
            }
            for user_id, user_data in MOCK_USERS.items()
        ],
        "total_users": len(MOCK_USERS)
    }

@app.get("/api/v1/user/{user_id}")
async def get_user_info(user_id: str):
    """Get user information"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    return MOCK_USERS[user_id]

@app.get("/api/v1/insurance/portfolio")
async def get_insurance_portfolio():
    """Get insurance company portfolio overview"""
    # Calculate portfolio metrics from all users
    total_customers = len(MOCK_USERS)
    total_premiums = 0
    risk_distribution = {"excellent": 0, "good": 0, "average": 0, "high_risk": 0}
    
    customer_details = []
    
    for user_id, user_data in MOCK_USERS.items():
        # Get scores for each user
        risk_data = get_mock_risk_score(user_id)
        safety_data = get_mock_safety_score(user_id)
        
        # Calculate premium based on risk
        base_premium = 120
        risk_score = risk_data["overall_score"]
        discount_percent = round((1 - risk_score) * 25)
        current_premium = round(base_premium * (1 - discount_percent / 100))
        total_premiums += current_premium
        
        # Determine risk tier
        if risk_score < 0.2:
            tier = "excellent"
        elif risk_score < 0.25:
            tier = "good" 
        elif risk_score < 0.35:
            tier = "average"
        else:
            tier = "high_risk"
        
        risk_distribution[tier] += 1
        
        customer_details.append({
            "id": user_id,
            "name": user_data["name"],
            "vehicle": user_data["vehicle"],
            "location": user_data["location"],
            "risk_score": risk_score,
            "safety_score": round(safety_data["overall_score"]),
            "current_premium": current_premium,
            "standard_premium": base_premium,
            "discount_percent": discount_percent if discount_percent > 0 else 0,
            "surcharge_percent": abs(discount_percent) if discount_percent < 0 else 0,
            "risk_tier": tier,
            "months_tracked": random.randint(6, 12),
            "total_trips": random.randint(150, 500),
            "claims": 1 if tier == "high_risk" and random.random() < 0.3 else 0,
            "last_update": datetime.now().date().isoformat()
        })
    
    return {
        "company": "Insurance Co.",
        "total_customers": total_customers,
        "monthly_premiums": total_premiums,
        "claims_ratio": 0.68,
        "profit_margin": 0.24,
        "risk_distribution": risk_distribution,
        "customers": customer_details,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/insurance/analytics", response_model=Dict[str, Any])
async def get_insurance_analytics():
    """
    Advanced analytics for State Farm presentation
    """
    return {
        "market_insights": {
            "competitive_advantage": {
                "claims_reduction": 23,  # percent
                "retention_improvement": 15,  # percent
                "annual_savings_per_10k": 2400000,  # dollars
                "processing_time_reduction": 67  # percent
            },
            "industry_benchmarks": {
                "traditional_claims_ratio": 0.85,
                "ai_enhanced_claims_ratio": 0.68,
                "traditional_retention": 82,
                "ai_enhanced_retention": 94
            }
        },
        "predictive_models": {
            "claim_prediction_accuracy": 89.3,
            "risk_assessment_confidence": 92.1,
            "premium_optimization_success": 87.8
        },
        "operational_metrics": {
            "policies_processed_daily": 1247,
            "automated_underwriting_rate": 78,
            "customer_satisfaction_score": 4.6,
            "agent_efficiency_improvement": 34
        },
        "revenue_projections": {
            "next_quarter_growth": 18.5,
            "customer_lifetime_value_increase": 23.2,
            "new_policy_acquisition_rate": 156  # per week
        },
        "risk_mitigation": {
            "fraud_detection_improvement": 67,
            "high_risk_customer_identification": 94,
            "proactive_intervention_success": 82
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/vehicle-safety/{user_id}", response_model=Dict[str, Any])
async def get_vehicle_safety(user_id: str):
    """
    Get NHTSA safety rating for user's vehicle
    """
    # Get user data first
    user_data = MOCK_USERS.get(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Parse vehicle info
    vehicle_parts = user_data["vehicle"].split()
    if len(vehicle_parts) >= 3:
        year = int(vehicle_parts[0])
        make = vehicle_parts[1]
        model = " ".join(vehicle_parts[2:])
    else:
        # Fallback parsing
        year = 2020
        make = "Honda"
        model = "Civic"
    
    # Get NHTSA safety data
    safety_data = nhtsa.get_vehicle_safety_rating(year, make, model)
    
    # Add user context
    safety_data["user_id"] = user_id
    safety_data["user_vehicle"] = user_data["vehicle"]
    safety_data["timestamp"] = datetime.now().isoformat()
    
    return safety_data

@app.get("/api/v1/enhanced-risk-score/{user_id}", response_model=Dict[str, Any])
async def get_enhanced_risk_score(user_id: str):
    """
    Get risk score enhanced with NHTSA safety data
    """
    # Get base risk score
    base_risk = get_mock_risk_score(user_id)
    
    # Get NHTSA safety impact
    safety_data = await get_vehicle_safety(user_id)
    safety_adjustment = safety_data["risk_impact"]["risk_reduction"]
    
    # Calculate enhanced risk score
    enhanced_score = max(0.05, base_risk["overall_score"] - safety_adjustment)
    
    return {
        "user_id": user_id,
        "base_risk_score": base_risk["overall_score"],
        "safety_adjustment": safety_adjustment,
        "enhanced_risk_score": enhanced_score,
        "nhtsa_rating": safety_data["nhtsa_data"]["overall_rating"],
        "premium_benefit": safety_data["risk_impact"]["premium_adjustment"],
        "safety_factors": {
            "vehicle_safety_rating": safety_data["nhtsa_data"]["overall_rating"],
            "rollover_rating": safety_data["nhtsa_data"]["rollover_rating"],
            "crash_ratings": {
                "frontal": safety_data["nhtsa_data"]["frontal_crash_rating"],
                "side": safety_data["nhtsa_data"]["side_crash_rating"]
            }
        },
        "risk_improvement": f"{((base_risk['overall_score'] - enhanced_score) / base_risk['overall_score'] * 100):.1f}%",
        "data_sources": ["Driving Behavior", "TomTom Traffic", "NHTSA Safety Database"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/live-data-status", response_model=Dict[str, Any])
async def get_live_data_status():
    """
    Get current live data streaming status and simulate real-time changes
    """
    # Simulate slight variations in traffic conditions
    traffic_multiplier = random.uniform(0.95, 1.15)  # ±15% variation
    current_time = datetime.now()
    
    return {
        "live_mode": True,
        "last_update": current_time.isoformat(),
        "traffic_conditions": {
            "san_francisco": random.choice(["Light", "Moderate", "Heavy"]),
            "austin": random.choice(["Light", "Moderate", "Heavy"]),
            "seattle": random.choice(["Light", "Moderate", "Heavy"]),
            "new_york": random.choice(["Light", "Heavy", "Severe"]),
            "denver": random.choice(["Light", "Moderate", "Heavy"]),
        },
        "active_incidents": random.randint(2, 8),
        "weather_alerts": random.randint(0, 3),
        "risk_adjustments": {
            "traffic_impact": round((traffic_multiplier - 1) * 100, 1),
            "weather_impact": random.uniform(-5, 10),
            "time_of_day_impact": random.uniform(-3, 8)
        },
        "api_calls_made": random.randint(1, 3),
        "data_sources": ["TomTom Traffic API", "NHTSA Safety Database", "Weather API"],
        "next_update_in": 6  # seconds
    }

if __name__ == "__main__":
    import uvicorn
    print("🚗 Starting DriveWise AI Backend...")
    print("📊 Dashboard will be available at: http://localhost:3000")
    print("🔗 API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)