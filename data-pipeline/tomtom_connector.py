import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
from dataclasses import dataclass
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrafficData:
    location_lat: float
    location_lon: float
    congestion_level: float
    average_speed: float
    incident_count: int
    road_type: str
    timestamp: datetime
    source: str = "tomtom"

class TomTomConnector:
    """TomTom Traffic API Connector"""
    
    def __init__(self):
        self.api_key = os.getenv("TOMTOM_API_KEY")
        self.base_url = "https://api.tomtom.com/traffic"
        self.rate_limit_delay = 1  # seconds between requests
        
        if not self.api_key:
            raise ValueError("TOMTOM_API_KEY environment variable is required")
    
    def get_traffic_flow(self, lat: float, lon: float, radius: float = 5.0) -> List[TrafficData]:
        """Get traffic flow data for a geographic area"""
        try:
            # TomTom Traffic Flow API endpoint
            url = f"{self.base_url}/services/4/flowSegmentData/absolute/10/json"
            
            params = {
                "key": self.api_key,
                "point": f"{lat},{lon}",
                "unit": "KMPH"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            traffic_data = []
            
            # Parse TomTom response
            if "flowSegmentData" in data:
                segment = data["flowSegmentData"]
                
                traffic_item = TrafficData(
                    location_lat=lat,
                    location_lon=lon,
                    congestion_level=self._calculate_congestion_level(
                        segment.get("currentSpeed", 0),
                        segment.get("freeFlowSpeed", 1)
                    ),
                    average_speed=segment.get("currentSpeed", 0),
                    incident_count=0,  # TomTom flow API doesn't provide incidents
                    road_type=segment.get("roadClosure", "unknown"),
                    timestamp=datetime.utcnow()
                )
                
                traffic_data.append(traffic_item)
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            return traffic_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching TomTom traffic data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in TomTom connector: {e}")
            return []
    
    def get_traffic_incidents(self, lat: float, lon: float, radius: float = 10.0) -> List[Dict[str, Any]]:
        """Get traffic incidents in a geographic area"""
        try:
            url = f"{self.base_url}/services/5/incidentDetails/s3/{lat},{lon},{radius}/10/-1/json"
            
            params = {
                "key": self.api_key,
                "language": "en-US",
                "categoryFilter": "0,1,2,3,4,5,6,7,8,9,10,11"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            incidents = []
            
            if "incidents" in data:
                for incident in data["incidents"]:
                    incidents.append({
                        "id": incident.get("id"),
                        "type": incident.get("iconCategory"),
                        "description": incident.get("description"),
                        "severity": incident.get("magnitude", 0),
                        "location": {
                            "lat": incident.get("geometry", {}).get("coordinates", [0, 0])[1],
                            "lon": incident.get("geometry", {}).get("coordinates", [0, 0])[0]
                        },
                        "road": incident.get("roadNumbers", ["Unknown"])[0] if incident.get("roadNumbers") else "Unknown",
                        "timestamp": datetime.utcnow()
                    })
            
            time.sleep(self.rate_limit_delay)
            return incidents
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching TomTom incidents: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching incidents: {e}")
            return []
    
    def _calculate_congestion_level(self, current_speed: float, free_flow_speed: float) -> float:
        """Calculate congestion level (0-1) based on speed ratio"""
        if free_flow_speed <= 0:
            return 0.0
        
        speed_ratio = current_speed / free_flow_speed
        
        if speed_ratio >= 0.8:
            return 0.0  # Free flow
        elif speed_ratio >= 0.6:
            return 0.3  # Light congestion
        elif speed_ratio >= 0.4:
            return 0.6  # Moderate congestion
        else:
            return 1.0  # Heavy congestion
    
    def get_route_traffic(self, start_lat: float, start_lon: float, 
                         end_lat: float, end_lon: float) -> Dict[str, Any]:
        """Get traffic information for a specific route"""
        try:
            url = f"{self.base_url}/routing/1/calculateRoute/{start_lat},{start_lon}:{end_lat},{end_lon}/json"
            
            params = {
                "key": self.api_key,
                "traffic": "true",
                "travelMode": "car"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if "routes" in data and len(data["routes"]) > 0:
                route = data["routes"][0]
                summary = route.get("summary", {})
                
                return {
                    "distance_meters": summary.get("lengthInMeters", 0),
                    "travel_time_seconds": summary.get("travelTimeInSeconds", 0),
                    "traffic_delay_seconds": summary.get("trafficDelayInSeconds", 0),
                    "congestion_level": self._calculate_congestion_level(
                        summary.get("lengthInMeters", 0) / max(summary.get("travelTimeInSeconds", 1), 1) * 3.6,  # Convert to km/h
                        50  # Assume 50 km/h free flow speed
                    ),
                    "route_points": route.get("legs", [{}])[0].get("points", [])
                }
            
            time.sleep(self.rate_limit_delay)
            return {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching route traffic: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error fetching route traffic: {e}")
            return {}

class DataIngestionPipeline:
    """Main data ingestion pipeline for traffic data"""
    
    def __init__(self):
        self.tomtom = TomTomConnector()
        self.batch_size = 100
        self.processing_delay = 5  # seconds between batches
    
    def ingest_traffic_data_for_region(self, center_lat: float, center_lon: float, 
                                     radius: float = 25.0) -> List[TrafficData]:
        """Ingest traffic data for a geographic region"""
        all_traffic_data = []
        
        # Generate grid points around the center
        grid_points = self._generate_grid_points(center_lat, center_lon, radius, grid_size=5)
        
        logger.info(f"Ingesting traffic data for {len(grid_points)} locations")
        
        for i, (lat, lon) in enumerate(grid_points):
            try:
                traffic_data = self.tomtom.get_traffic_flow(lat, lon)
                all_traffic_data.extend(traffic_data)
                
                # Log progress
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(grid_points)} locations")
                
                # Batch processing delay
                if (i + 1) % self.batch_size == 0:
                    time.sleep(self.processing_delay)
                    
            except Exception as e:
                logger.error(f"Error processing location {lat}, {lon}: {e}")
                continue
        
        logger.info(f"Completed traffic data ingestion: {len(all_traffic_data)} records")
        return all_traffic_data
    
    def _generate_grid_points(self, center_lat: float, center_lon: float, 
                            radius: float, grid_size: int = 5) -> List[tuple]:
        """Generate grid points for data collection"""
        points = []
        
        # Convert radius from km to degrees (approximate)
        lat_step = radius / 111.0 / grid_size  # 1 degree lat ≈ 111 km
        lon_step = radius / (111.0 * abs(center_lat)) / grid_size  # Adjust for longitude
        
        for i in range(-grid_size, grid_size + 1):
            for j in range(-grid_size, grid_size + 1):
                lat = center_lat + i * lat_step
                lon = center_lon + j * lon_step
                points.append((lat, lon))
        
        return points
    
    def run_continuous_ingestion(self, locations: List[tuple], interval_minutes: int = 15):
        """Run continuous data ingestion for specified locations"""
        logger.info(f"Starting continuous ingestion for {len(locations)} locations")
        logger.info(f"Update interval: {interval_minutes} minutes")
        
        while True:
            try:
                start_time = datetime.utcnow()
                all_data = []
                
                for lat, lon in locations:
                    traffic_data = self.tomtom.get_traffic_flow(lat, lon)
                    all_data.extend(traffic_data)
                
                # Here you would typically save to BigQuery
                logger.info(f"Collected {len(all_data)} traffic records")
                
                # Calculate sleep time
                elapsed = (datetime.utcnow() - start_time).total_seconds()
                sleep_time = max(0, interval_minutes * 60 - elapsed)
                
                if sleep_time > 0:
                    logger.info(f"Sleeping for {sleep_time:.1f} seconds until next collection")
                    time.sleep(sleep_time)
                
            except KeyboardInterrupt:
                logger.info("Continuous ingestion stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in continuous ingestion: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main function for testing the data ingestion pipeline"""
    try:
        # Initialize pipeline
        pipeline = DataIngestionPipeline()
        
        # Test locations (San Francisco Bay Area)
        test_locations = [
            (37.7749, -122.4194),  # San Francisco
            (37.4419, -122.1430),  # Palo Alto
            (37.8044, -122.2711),  # Berkeley
        ]
        
        # Run single ingestion test
        logger.info("Running single ingestion test...")
        for lat, lon in test_locations:
            traffic_data = pipeline.tomtom.get_traffic_flow(lat, lon)
            incidents = pipeline.tomtom.get_traffic_incidents(lat, lon)
            
            logger.info(f"Location ({lat}, {lon}): {len(traffic_data)} traffic records, {len(incidents)} incidents")
        
        # Uncomment to run continuous ingestion
        # pipeline.run_continuous_ingestion(test_locations, interval_minutes=15)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()