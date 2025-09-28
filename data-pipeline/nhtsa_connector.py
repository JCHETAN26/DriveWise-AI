import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VehicleData:
    make: str
    model: str
    year: int
    vin: str
    safety_rating: Optional[float]
    recall_count: int
    crash_test_rating: Optional[Dict[str, Any]]
    timestamp: datetime
    source: str = "nhtsa"

class NHTSAConnector:
    """NHTSA Vehicle Safety API Connector"""
    
    def __init__(self):
        self.base_url = "https://vpic.nhtsa.dot.gov/api/vehicles"
        self.recall_url = "https://api.nhtsa.gov/recalls/recallsByVehicle"
        self.safety_url = "https://api.nhtsa.gov/SafetyRatings"
        
    def get_vehicle_info(self, vin: str) -> Optional[VehicleData]:
        """Get vehicle information by VIN"""
        try:
            # Decode VIN
            url = f"{self.base_url}/DecodeVin/{vin}"
            params = {"format": "json"}
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if "Results" in data and len(data["Results"]) > 0:
                results = {item["Variable"]: item["Value"] for item in data["Results"]}
                
                # Get additional safety data
                safety_rating = self.get_safety_rating(
                    results.get("Make", ""),
                    results.get("Model", ""),
                    results.get("Model Year", "")
                )
                
                # Get recall information
                recall_count = self.get_recall_count(vin)
                
                vehicle_data = VehicleData(
                    make=results.get("Make", "Unknown"),
                    model=results.get("Model", "Unknown"),
                    year=int(results.get("Model Year", "0")) if results.get("Model Year", "").isdigit() else 0,
                    vin=vin,
                    safety_rating=safety_rating.get("overall_rating") if safety_rating else None,
                    recall_count=recall_count,
                    crash_test_rating=safety_rating,
                    timestamp=datetime.utcnow()
                )
                
                return vehicle_data
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching NHTSA vehicle data for VIN {vin}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching vehicle data: {e}")
            return None
    
    def get_safety_rating(self, make: str, model: str, year: str) -> Optional[Dict[str, Any]]:
        """Get safety rating for a vehicle"""
        try:
            url = f"{self.safety_url}/modelyear/{year}/make/{make}/model/{model}"
            params = {"format": "json"}
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if "Results" in data and len(data["Results"]) > 0:
                result = data["Results"][0]
                
                return {
                    "overall_rating": float(result.get("OverallRating", 0)) if result.get("OverallRating") else None,
                    "rollover_rating": float(result.get("RolloverRating", 0)) if result.get("RolloverRating") else None,
                    "front_crash_rating": float(result.get("OverallFrontCrashRating", 0)) if result.get("OverallFrontCrashRating") else None,
                    "side_crash_rating": float(result.get("OverallSideCrashRating", 0)) if result.get("OverallSideCrashRating") else None,
                    "vehicle_id": result.get("VehicleId"),
                    "vehicle_description": result.get("VehicleDescription")
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching safety rating for {year} {make} {model}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching safety rating: {e}")
            return None
    
    def get_recall_count(self, vin: str) -> int:
        """Get number of recalls for a vehicle"""
        try:
            url = f"{self.recall_url}"
            params = {
                "vin": vin,
                "format": "json"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if "results" in data:
                return len(data["results"])
            
            return 0
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching recalls for VIN {vin}: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error fetching recalls: {e}")
            return 0
    
    def get_recalls_by_make_model_year(self, make: str, model: str, year: int) -> List[Dict[str, Any]]:
        """Get recalls for a specific make/model/year"""
        try:
            url = f"{self.recall_url}"
            params = {
                "make": make,
                "model": model,
                "modelYear": year,
                "format": "json"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            recalls = []
            
            if "results" in data:
                for recall in data["results"]:
                    recalls.append({
                        "recall_number": recall.get("NHTSACampaignNumber"),
                        "recall_date": recall.get("ReportReceivedDate"),
                        "component": recall.get("Component"),
                        "summary": recall.get("Summary"),
                        "consequence": recall.get("Consequence"),
                        "remedy": recall.get("Remedy"),
                        "manufacturer": recall.get("Manufacturer")
                    })
            
            return recalls
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching recalls for {year} {make} {model}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching recalls: {e}")
            return []
    
    def search_vehicles(self, make: str = None, model: str = None, year: int = None) -> List[Dict[str, Any]]:
        """Search for vehicles by make, model, or year"""
        try:
            vehicles = []
            
            if make and not model:
                # Get models for a make
                url = f"{self.base_url}/GetModelsForMake/{make}"
                params = {"format": "json"}
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if "Results" in data:
                    for result in data["Results"]:
                        vehicles.append({
                            "make": result.get("Make_Name"),
                            "model": result.get("Model_Name"),
                            "make_id": result.get("Make_ID"),
                            "model_id": result.get("Model_ID")
                        })
            
            elif make and model and year:
                # Get specific vehicle data
                safety_rating = self.get_safety_rating(make, model, str(year))
                recalls = self.get_recalls_by_make_model_year(make, model, year)
                
                vehicles.append({
                    "make": make,
                    "model": model,
                    "year": year,
                    "safety_rating": safety_rating,
                    "recalls": recalls
                })
            
            return vehicles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching vehicles: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error searching vehicles: {e}")
            return []

class VehicleDataPipeline:
    """Pipeline for processing vehicle safety data"""
    
    def __init__(self):
        self.nhtsa = NHTSAConnector()
    
    def process_vehicle_batch(self, vins: List[str]) -> List[VehicleData]:
        """Process a batch of VINs"""
        vehicle_data = []
        
        logger.info(f"Processing batch of {len(vins)} VINs")
        
        for i, vin in enumerate(vins):
            try:
                data = self.nhtsa.get_vehicle_info(vin)
                if data:
                    vehicle_data.append(data)
                
                # Log progress
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(vins)} VINs")
                    
            except Exception as e:
                logger.error(f"Error processing VIN {vin}: {e}")
                continue
        
        logger.info(f"Successfully processed {len(vehicle_data)} vehicles")
        return vehicle_data
    
    def enrich_driving_data_with_vehicle_info(self, driving_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich driving data with vehicle safety information"""
        enriched_records = []
        
        for record in driving_records:
            try:
                vin = record.get("vehicle", {}).get("vin")
                if vin:
                    vehicle_data = self.nhtsa.get_vehicle_info(vin)
                    if vehicle_data:
                        record["vehicle"]["safety_rating"] = vehicle_data.safety_rating
                        record["vehicle"]["recall_count"] = vehicle_data.recall_count
                        record["vehicle"]["crash_test_rating"] = vehicle_data.crash_test_rating
                
                enriched_records.append(record)
                
            except Exception as e:
                logger.error(f"Error enriching record: {e}")
                enriched_records.append(record)  # Keep original record
        
        return enriched_records

def main():
    """Main function for testing the NHTSA connector"""
    try:
        connector = NHTSAConnector()
        pipeline = VehicleDataPipeline()
        
        # Test VIN lookup
        test_vin = "1HGBH41JXMN109186"  # Example Honda VIN
        logger.info(f"Testing VIN lookup for: {test_vin}")
        
        vehicle_data = connector.get_vehicle_info(test_vin)
        if vehicle_data:
            logger.info(f"Vehicle: {vehicle_data.year} {vehicle_data.make} {vehicle_data.model}")
            logger.info(f"Safety Rating: {vehicle_data.safety_rating}")
            logger.info(f"Recalls: {vehicle_data.recall_count}")
        
        # Test make/model search
        logger.info("Testing vehicle search...")
        vehicles = connector.search_vehicles(make="Honda", model="Civic", year=2020)
        logger.info(f"Found {len(vehicles)} matching vehicles")
        
        # Test recall lookup
        logger.info("Testing recall lookup...")
        recalls = connector.get_recalls_by_make_model_year("Honda", "Civic", 2020)
        logger.info(f"Found {len(recalls)} recalls")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()