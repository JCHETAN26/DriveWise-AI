from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DrivingEventType(str, Enum):
    HARD_BRAKE = "hard_brake"
    RAPID_ACCELERATION = "rapid_acceleration"
    SHARP_TURN = "sharp_turn"
    SPEEDING = "speeding"
    PHONE_USAGE = "phone_usage"
    DISTRACTED_DRIVING = "distracted_driving"

class LocationData(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: Optional[float] = None
    accuracy: Optional[float] = None

class VehicleData(BaseModel):
    make: str
    model: str
    year: int = Field(..., ge=1900, le=2030)
    vin: Optional[str] = None
    safety_rating: Optional[float] = Field(None, ge=0, le=5)

class DrivingEvent(BaseModel):
    event_type: DrivingEventType
    timestamp: datetime
    location: LocationData
    severity: float = Field(..., ge=0, le=1)
    speed: Optional[float] = Field(None, ge=0)
    metadata: Optional[Dict[str, Any]] = None

class TripData(BaseModel):
    trip_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    start_location: LocationData
    end_location: LocationData
    distance: float = Field(..., ge=0)  # in kilometers
    duration: float = Field(..., ge=0)  # in seconds
    avg_speed: float = Field(..., ge=0)
    max_speed: float = Field(..., ge=0)
    events: List[DrivingEvent] = []
    weather_conditions: Optional[str] = None
    traffic_conditions: Optional[str] = None

class DrivingData(BaseModel):
    user_id: str
    vehicle: VehicleData
    trip: TripData
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class RiskFactors(BaseModel):
    speeding_score: float = Field(..., ge=0, le=1)
    hard_braking_score: float = Field(..., ge=0, le=1)
    acceleration_score: float = Field(..., ge=0, le=1)
    distraction_score: float = Field(..., ge=0, le=1)
    time_of_day_score: float = Field(..., ge=0, le=1)
    weather_score: float = Field(..., ge=0, le=1)
    traffic_score: float = Field(..., ge=0, le=1)

class RiskScore(BaseModel):
    user_id: str
    overall_score: float = Field(..., ge=0, le=1)
    risk_factors: RiskFactors
    confidence: float = Field(..., ge=0, le=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class SafetyMetrics(BaseModel):
    safe_following_distance: float = Field(..., ge=0, le=1)
    smooth_acceleration: float = Field(..., ge=0, le=1)
    smooth_braking: float = Field(..., ge=0, le=1)
    speed_limit_adherence: float = Field(..., ge=0, le=1)
    defensive_driving: float = Field(..., ge=0, le=1)
    attention_level: float = Field(..., ge=0, le=1)

class SafetyScore(BaseModel):
    user_id: str
    overall_score: float = Field(..., ge=0, le=100)
    safety_metrics: SafetyMetrics
    improvement_suggestions: List[str] = []
    comparative_ranking: Optional[int] = None  # percentile ranking
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class InsuranceQuote(BaseModel):
    user_id: str
    base_premium: float = Field(..., ge=0)
    risk_adjustment: float = Field(..., ge=-1, le=1)
    final_premium: float = Field(..., ge=0)
    discount_percentage: float = Field(..., ge=0, le=100)
    quote_valid_until: datetime
    factors_explanation: Dict[str, str] = {}

class UserProfile(BaseModel):
    user_id: str
    age: int = Field(..., ge=16, le=120)
    driving_experience_years: int = Field(..., ge=0)
    license_type: str
    annual_mileage: Optional[float] = Field(None, ge=0)
    primary_vehicle: VehicleData
    location: LocationData
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)