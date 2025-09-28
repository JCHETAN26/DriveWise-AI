#!/usr/bin/env python3

"""
NHTSA API Connector for DriveWise AI
Fetches vehicle safety ratings from National Highway Traffic Safety Administration
"""

import requests
import json
from typing import Dict, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NHTSAConnector:
    """
    Connector for NHTSA Vehicle Safety API
    """
    
    def __init__(self):
        self.base_url = "https://api.nhtsa.gov/SafetyRatings"
        
    def get_vehicle_safety_rating(self, year: int, make: str, model: str) -> Dict[str, Any]:
        """
        Get safety rating for a specific vehicle
        
        Args:
            year: Vehicle year (e.g., 2020)
            make: Vehicle make (e.g., "HONDA") 
            model: Vehicle model (e.g., "CIVIC")
            
        Returns:
            Dictionary with safety ratings and risk adjustments
        """
        try:
            # Step 1: Get vehicle ID
            search_url = f"{self.base_url}/modelyear/{year}/make/{make.upper()}/model/{model.upper()}"
            
            logger.info(f"Searching for vehicle: {year} {make} {model}")
            response = requests.get(search_url, timeout=10)
            response.raise_for_status()
            
            search_data = response.json()
            
            if not search_data.get('Results'):
                logger.warning(f"No results found for {year} {make} {model}")
                return self._get_default_rating(year, make, model)
            
            # Get first vehicle ID (usually most relevant)
            vehicle_id = search_data['Results'][0]['VehicleId']
            
            # Step 2: Get detailed safety ratings
            rating_url = f"{self.base_url}/VehicleId/{vehicle_id}"
            rating_response = requests.get(rating_url, timeout=10)
            rating_response.raise_for_status()
            
            rating_data = rating_response.json()
            
            if not rating_data.get('Results'):
                logger.warning(f"No rating data found for vehicle ID {vehicle_id}")
                return self._get_default_rating(year, make, model)
            
            vehicle_data = rating_data['Results'][0]
            
            # Parse safety ratings
            overall_rating = self._parse_rating(vehicle_data.get('OverallRating'))
            rollover_rating = self._parse_rating(vehicle_data.get('RolloverRating'))
            frontal_rating = self._parse_rating(vehicle_data.get('FrontalCrashRating'))
            side_rating = self._parse_rating(vehicle_data.get('SideCrashRating'))
            
            # Calculate premium adjustment based on safety
            premium_adjustment = self._calculate_premium_adjustment(overall_rating)
            
            result = {
                "year": year,
                "make": make.title(),
                "model": model.title(),
                "nhtsa_data": {
                    "overall_rating": overall_rating,
                    "rollover_rating": rollover_rating,  
                    "frontal_crash_rating": frontal_rating,
                    "side_crash_rating": side_rating,
                    "vehicle_description": vehicle_data.get('VehicleDescription', f"{year} {make} {model}"),
                    "nhtsa_id": vehicle_id
                },
                "risk_impact": {
                    "premium_adjustment": premium_adjustment,
                    "safety_score_boost": max(0, (overall_rating - 3) * 10),  # 0-20 point boost
                    "risk_reduction": max(0, (overall_rating - 3) * 0.05)  # Up to 10% risk reduction
                },
                "api_status": "success",
                "data_source": "NHTSA Vehicle Safety Database"
            }
            
            logger.info(f"Successfully retrieved safety data: {overall_rating} stars for {year} {make} {model}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"NHTSA API request failed: {e}")
            return self._get_error_fallback(year, make, model, str(e))
        except Exception as e:
            logger.error(f"Unexpected error in NHTSA lookup: {e}")
            return self._get_error_fallback(year, make, model, str(e))
    
    def _parse_rating(self, rating_str: Optional[str]) -> int:
        """Convert rating string to integer, default to 4 if not available"""
        if not rating_str:
            return 4  # Default to 4 stars if no data
        try:
            return int(rating_str)
        except (ValueError, TypeError):
            return 4
    
    def _calculate_premium_adjustment(self, overall_rating: int) -> float:
        """
        Calculate premium adjustment based on safety rating
        5 stars = -15% premium, 1 star = +10% premium
        """
        adjustment_map = {
            5: -0.15,  # 15% discount
            4: -0.08,  # 8% discount  
            3: 0.0,    # No adjustment
            2: 0.05,   # 5% increase
            1: 0.10    # 10% increase
        }
        return adjustment_map.get(overall_rating, 0.0)
    
    def _get_default_rating(self, year: int, make: str, model: str) -> Dict[str, Any]:
        """Return default safety rating when API data unavailable"""
        return {
            "year": year,
            "make": make.title(),
            "model": model.title(),
            "nhtsa_data": {
                "overall_rating": 4,
                "rollover_rating": 4,
                "frontal_crash_rating": 4,
                "side_crash_rating": 4,
                "vehicle_description": f"{year} {make.title()} {model.title()}",
                "nhtsa_id": None
            },
            "risk_impact": {
                "premium_adjustment": -0.08,
                "safety_score_boost": 10,
                "risk_reduction": 0.05
            },
            "api_status": "default",
            "data_source": "NHTSA Default Estimates"
        }
    
    def _get_error_fallback(self, year: int, make: str, model: str, error: str) -> Dict[str, Any]:
        """Return fallback data when API fails"""
        return {
            "year": year,
            "make": make.title(),
            "model": model.title(), 
            "nhtsa_data": {
                "overall_rating": 3,
                "rollover_rating": 3,
                "frontal_crash_rating": 3,
                "side_crash_rating": 3,
                "vehicle_description": f"{year} {make.title()} {model.title()}",
                "nhtsa_id": None
            },
            "risk_impact": {
                "premium_adjustment": 0.0,
                "safety_score_boost": 0,
                "risk_reduction": 0.0
            },
            "api_status": "error",
            "error": error,
            "data_source": "NHTSA API Error Fallback"
        }

# Test the connector
if __name__ == "__main__":
    nhtsa = NHTSAConnector()
    
    # Test with our demo vehicles
    test_vehicles = [
        (2020, "Honda", "Civic"),
        (2018, "Ford", "F-150"), 
        (2022, "Tesla", "Model 3"),
        (2019, "BMW", "330i"),
        (2021, "Subaru", "Outback")
    ]
    
    print("🚗 NHTSA Safety Rating Test Results:")
    print("=" * 50)
    
    for year, make, model in test_vehicles:
        result = nhtsa.get_vehicle_safety_rating(year, make, model)
        rating = result['nhtsa_data']['overall_rating']
        adjustment = result['risk_impact']['premium_adjustment']
        
        print(f"{year} {make} {model}:")
        print(f"  ⭐ Safety Rating: {rating}/5 stars")
        print(f"  💰 Premium Impact: {adjustment:+.1%}")
        print(f"  📊 Status: {result['api_status']}")
        print()