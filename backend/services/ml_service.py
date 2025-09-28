from typing import Dict, List, Any, Optional
import logging
import numpy as np
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class MLService:
    """Machine Learning service for risk and safety scoring"""
    
    def __init__(self):
        self.models_loaded = False
        self._load_models()
    
    def _load_models(self):
        """Load ML models (mock implementation)"""
        try:
            # In real implementation, load actual ML models
            self.risk_model = {"version": "1.0", "type": "logistic_regression"}
            self.safety_model = {"version": "1.0", "type": "linear_regression"}
            self.models_loaded = True
            logger.info("ML models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading ML models: {e}")
            self.models_loaded = False
    
    async def get_risk_score(self, user_id: str) -> Dict[str, Any]:
        """Get risk score for a user"""
        try:
            if not self.models_loaded:
                self._load_models()
            
            # Mock risk scoring logic
            # In real implementation, use actual ML model prediction
            base_risk = np.random.beta(2, 5)  # Skewed towards lower risk
            
            risk_factors = {
                "speeding_score": min(1.0, max(0.0, np.random.normal(0.2, 0.1))),
                "hard_braking_score": min(1.0, max(0.0, np.random.normal(0.15, 0.08))),
                "acceleration_score": min(1.0, max(0.0, np.random.normal(0.18, 0.09))),
                "distraction_score": min(1.0, max(0.0, np.random.normal(0.12, 0.06))),
                "time_of_day_score": min(1.0, max(0.0, np.random.normal(0.25, 0.1))),
                "weather_score": min(1.0, max(0.0, np.random.normal(0.3, 0.12))),
                "traffic_score": min(1.0, max(0.0, np.random.normal(0.35, 0.15)))
            }
            
            # Calculate overall score as weighted average
            weights = {
                "speeding_score": 0.25,
                "hard_braking_score": 0.20,
                "acceleration_score": 0.15,
                "distraction_score": 0.15,
                "time_of_day_score": 0.10,
                "weather_score": 0.08,
                "traffic_score": 0.07
            }
            
            overall_score = sum(risk_factors[factor] * weight for factor, weight in weights.items())
            
            return {
                "user_id": user_id,
                "overall_score": round(overall_score, 3),
                "risk_factors": {k: round(v, 3) for k, v in risk_factors.items()},
                "confidence": 0.87,
                "timestamp": datetime.utcnow(),
                "model_version": "1.0"
            }
            
        except Exception as e:
            logger.error(f"Error calculating risk score for user {user_id}: {e}")
            return {
                "user_id": user_id,
                "error": "Unable to calculate risk score",
                "timestamp": datetime.utcnow()
            }
    
    async def get_safety_score(self, user_id: str) -> Dict[str, Any]:
        """Get safety score for a user"""
        try:
            if not self.models_loaded:
                self._load_models()
            
            # Mock safety scoring logic
            safety_metrics = {
                "safe_following_distance": min(1.0, max(0.0, np.random.normal(0.78, 0.12))),
                "smooth_acceleration": min(1.0, max(0.0, np.random.normal(0.85, 0.10))),
                "smooth_braking": min(1.0, max(0.0, np.random.normal(0.82, 0.11))),
                "speed_limit_adherence": min(1.0, max(0.0, np.random.normal(0.76, 0.15))),
                "defensive_driving": min(1.0, max(0.0, np.random.normal(0.79, 0.13))),
                "attention_level": min(1.0, max(0.0, np.random.normal(0.88, 0.08)))
            }
            
            # Calculate overall safety score (0-100 scale)
            weights = {
                "safe_following_distance": 0.20,
                "smooth_acceleration": 0.18,
                "smooth_braking": 0.18,
                "speed_limit_adherence": 0.22,
                "defensive_driving": 0.12,
                "attention_level": 0.10
            }
            
            overall_score = sum(safety_metrics[metric] * weight for metric, weight in weights.items()) * 100
            
            # Generate improvement suggestions
            suggestions = []
            if safety_metrics["safe_following_distance"] < 0.7:
                suggestions.append("Maintain greater following distance from other vehicles")
            if safety_metrics["speed_limit_adherence"] < 0.8:
                suggestions.append("Reduce speeding incidents to improve safety score")
            if safety_metrics["smooth_braking"] < 0.75:
                suggestions.append("Practice gentler braking to avoid hard stops")
            if safety_metrics["smooth_acceleration"] < 0.8:
                suggestions.append("Use gradual acceleration for smoother driving")
            
            if not suggestions:
                suggestions.append("Great job! Keep up the safe driving habits")
            
            return {
                "user_id": user_id,
                "overall_score": round(overall_score, 1),
                "safety_metrics": {k: round(v, 3) for k, v in safety_metrics.items()},
                "improvement_suggestions": suggestions,
                "comparative_ranking": int(np.random.normal(75, 15)),  # Percentile ranking
                "timestamp": datetime.utcnow(),
                "model_version": "1.0"
            }
            
        except Exception as e:
            logger.error(f"Error calculating safety score for user {user_id}: {e}")
            return {
                "user_id": user_id,
                "error": "Unable to calculate safety score",
                "timestamp": datetime.utcnow()
            }
    
    async def process_driving_data(self, user_id: str, driving_data: Dict[str, Any]):
        """Process driving data and update ML models"""
        try:
            logger.info(f"Processing driving data for user {user_id}")
            
            # Extract features from driving data
            features = self._extract_features(driving_data)
            
            # Update user's risk and safety scores
            risk_score = await self.get_risk_score(user_id)
            safety_score = await self.get_safety_score(user_id)
            
            logger.info(f"Updated scores for user {user_id}: risk={risk_score['overall_score']}, safety={safety_score['overall_score']}")
            
            return {
                "status": "success",
                "risk_score": risk_score,
                "safety_score": safety_score,
                "features_extracted": len(features)
            }
            
        except Exception as e:
            logger.error(f"Error processing driving data: {e}")
            return {"status": "error", "message": str(e)}
    
    def _extract_features(self, driving_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract ML features from raw driving data"""
        try:
            features = {}
            
            # Extract basic trip features
            if "trip" in driving_data:
                trip = driving_data["trip"]
                features["distance"] = trip.get("distance", 0)
                features["duration"] = trip.get("duration", 0)
                features["avg_speed"] = trip.get("avg_speed", 0)
                features["max_speed"] = trip.get("max_speed", 0)
                
                # Calculate speed ratio
                if features["avg_speed"] > 0:
                    features["speed_ratio"] = features["max_speed"] / features["avg_speed"]
                else:
                    features["speed_ratio"] = 1.0
                
                # Count events by type
                events = trip.get("events", [])
                event_counts = {}
                for event in events:
                    event_type = event.get("event_type", "unknown")
                    event_counts[event_type] = event_counts.get(event_type, 0) + 1
                
                features["hard_brake_count"] = event_counts.get("hard_brake", 0)
                features["rapid_acceleration_count"] = event_counts.get("rapid_acceleration", 0)
                features["speeding_count"] = event_counts.get("speeding", 0)
                features["sharp_turn_count"] = event_counts.get("sharp_turn", 0)
                
                # Calculate event rates per km
                if features["distance"] > 0:
                    features["events_per_km"] = len(events) / features["distance"]
                    features["hard_brake_rate"] = features["hard_brake_count"] / features["distance"]
                else:
                    features["events_per_km"] = 0
                    features["hard_brake_rate"] = 0
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return {}