"""
Real-time TomTom traffic integration for DriveWise AI
"""
import os
import requests
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeTomTomConnector:
    """Live TomTom traffic data integration"""
    
    def __init__(self):
        self.api_key = os.getenv("TOMTOM_API_KEY")
        self.base_url = "https://api.tomtom.com/traffic"
        
        if not self.api_key:
            raise ValueError("TOMTOM_API_KEY not found in environment")
    
    async def get_live_traffic_flow(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get real-time traffic flow data for a location"""
        try:
            url = f"{self.base_url}/services/4/flowSegmentData/absolute/10/json"
            
            params = {
                "key": self.api_key,
                "point": f"{lat},{lon}",
                "unit": "KMPH"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "flowSegmentData" in data:
                segment = data["flowSegmentData"]
                
                return {
                    "location": {"lat": lat, "lon": lon},
                    "current_speed": segment.get("currentSpeed", 0),
                    "free_flow_speed": segment.get("freeFlowSpeed", 50),
                    "congestion_level": self._calculate_congestion(
                        segment.get("currentSpeed", 0),
                        segment.get("freeFlowSpeed", 50)
                    ),
                    "road_closure": segment.get("roadClosure", False),
                    "confidence": segment.get("confidence", 0.8),
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "tomtom_live"
                }
            else:
                return self._get_fallback_data(lat, lon)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"TomTom API error: {e}")
            return self._get_fallback_data(lat, lon)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return self._get_fallback_data(lat, lon)
    
    async def get_live_incidents(self, lat: float, lon: float, radius: float = 10.0) -> List[Dict[str, Any]]:
        """Get real-time traffic incidents"""
        try:
            url = f"{self.base_url}/services/5/incidentDetails/s3/{lat},{lon},{radius}/10/-1/json"
            
            params = {
                "key": self.api_key,
                "language": "en-US"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            incidents = []
            
            if "incidents" in data:
                for incident in data["incidents"]:
                    incidents.append({
                        "id": incident.get("id"),
                        "type": incident.get("iconCategory", 0),
                        "description": incident.get("description", "Traffic incident"),
                        "severity": incident.get("magnitude", 1),
                        "location": {
                            "lat": incident.get("geometry", {}).get("coordinates", [lon, lat])[1],
                            "lon": incident.get("geometry", {}).get("coordinates", [lon, lat])[0]
                        },
                        "delay_seconds": incident.get("delay", 0),
                        "timestamp": datetime.utcnow().isoformat()
                    })
            
            return incidents
            
        except Exception as e:
            logger.error(f"Error fetching incidents: {e}")
            return []
    
    def _calculate_congestion(self, current_speed: float, free_flow_speed: float) -> float:
        """Calculate congestion level (0-1)"""
        if free_flow_speed <= 0:
            return 0.0
        
        speed_ratio = current_speed / free_flow_speed
        
        if speed_ratio >= 0.85:
            return 0.0  # Free flow
        elif speed_ratio >= 0.65:
            return 0.3  # Light congestion
        elif speed_ratio >= 0.45:
            return 0.6  # Moderate congestion
        else:
            return 1.0  # Heavy congestion
    
    def _get_fallback_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fallback data when API fails"""
        return {
            "location": {"lat": lat, "lon": lon},
            "current_speed": 45.0,
            "free_flow_speed": 50.0,
            "congestion_level": 0.1,
            "road_closure": False,
            "confidence": 0.5,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "fallback_data"
        }

# City locations for testing
MAJOR_CITIES = {
    "san_francisco": (37.7749, -122.4194),
    "austin": (30.2672, -97.7431),
    "seattle": (47.6062, -122.3321),
    "new_york": (40.7128, -74.0060),
    "denver": (39.7392, -104.9903)
}

async def test_real_traffic_data():
    """Test real-time traffic data fetching"""
    connector = RealTimeTomTomConnector()
    
    print("🚗 Testing Real-Time TomTom Traffic Data Integration")
    print("=" * 60)
    
    for city_name, (lat, lon) in MAJOR_CITIES.items():
        print(f"\n📍 {city_name.replace('_', ' ').title()}: ({lat}, {lon})")
        
        try:
            # Get traffic flow
            traffic_data = await connector.get_live_traffic_flow(lat, lon)
            
            print(f"   Current Speed: {traffic_data['current_speed']:.1f} km/h")
            print(f"   Free Flow Speed: {traffic_data['free_flow_speed']:.1f} km/h")
            print(f"   Congestion Level: {traffic_data['congestion_level']:.2f}")
            print(f"   Source: {traffic_data['source']}")
            
            # Get incidents
            incidents = await connector.get_live_incidents(lat, lon, 15.0)
            print(f"   Active Incidents: {len(incidents)}")
            
            if incidents:
                for incident in incidents[:2]:  # Show first 2
                    print(f"     - {incident['description']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Small delay to be nice to the API
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(test_real_traffic_data())