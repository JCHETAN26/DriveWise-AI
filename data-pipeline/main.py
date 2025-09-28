import os
import sys
import logging
import schedule
import time
from datetime import datetime
from typing import List, Tuple

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tomtom_connector import DataIngestionPipeline
from nhtsa_connector import VehicleDataPipeline
from bigquery_uploader import BigQueryUploader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class DataPipelineOrchestrator:
    """Main orchestrator for the DriveWise AI data pipeline"""
    
    def __init__(self):
        self.traffic_pipeline = DataIngestionPipeline()
        self.vehicle_pipeline = VehicleDataPipeline()
        self.bigquery_uploader = BigQueryUploader()
        
        # Define major cities for traffic data collection
        self.target_cities = [
            (37.7749, -122.4194, "San Francisco"),
            (34.0522, -118.2437, "Los Angeles"),
            (40.7128, -74.0060, "New York"),
            (41.8781, -87.6298, "Chicago"),
            (29.7604, -95.3698, "Houston"),
            (33.4484, -112.0740, "Phoenix"),
            (39.9526, -75.1652, "Philadelphia"),
            (32.7767, -96.7970, "Dallas"),
            (37.4419, -122.1430, "Palo Alto"),
            (47.6062, -122.3321, "Seattle")
        ]
    
    def collect_traffic_data(self):
        """Collect traffic data for all target cities"""
        try:
            logger.info("Starting traffic data collection...")
            all_traffic_data = []
            
            for lat, lon, city_name in self.target_cities:
                logger.info(f"Collecting traffic data for {city_name}")
                
                # Collect traffic data for the city
                traffic_data = self.traffic_pipeline.tomtom.get_traffic_flow(lat, lon)
                
                # Add city name to the data
                for data_point in traffic_data:
                    data_point.city = city_name
                
                all_traffic_data.extend(traffic_data)
                
                # Small delay between cities to respect rate limits
                time.sleep(2)
            
            # Upload to BigQuery
            if all_traffic_data:
                success = self.bigquery_uploader.upload_traffic_data(all_traffic_data)
                if success:
                    logger.info(f"Successfully uploaded {len(all_traffic_data)} traffic records")
                else:
                    logger.error("Failed to upload traffic data to BigQuery")
            else:
                logger.warning("No traffic data collected")
                
        except Exception as e:
            logger.error(f"Error in traffic data collection: {e}")
    
    def process_vehicle_data(self, vins: List[str] = None):
        """Process vehicle safety data"""
        try:
            logger.info("Starting vehicle data processing...")
            
            if not vins:
                # Get VINs from recent driving data (would query BigQuery in real implementation)
                vins = [
                    "1HGBH41JXMN109186",  # Sample Honda VIN
                    "WBANU53508CT05174",  # Sample BMW VIN
                    "JTDKN3DU0A0123456",  # Sample Toyota VIN
                ]
            
            vehicle_data = self.vehicle_pipeline.process_vehicle_batch(vins[:10])  # Limit batch size
            
            if vehicle_data:
                success = self.bigquery_uploader.upload_vehicle_data(vehicle_data)
                if success:
                    logger.info(f"Successfully processed {len(vehicle_data)} vehicles")
                else:
                    logger.error("Failed to upload vehicle data to BigQuery")
            else:
                logger.warning("No vehicle data processed")
                
        except Exception as e:
            logger.error(f"Error in vehicle data processing: {e}")
    
    def update_ml_models(self):
        """Trigger ML model updates"""
        try:
            logger.info("Triggering ML model updates...")
            
            # Update risk scores
            self.bigquery_uploader.execute_procedure("drivewise_ai.update_risk_scores")
            
            # Update safety scores  
            self.bigquery_uploader.execute_procedure("drivewise_ai.update_safety_scores")
            
            logger.info("ML model updates completed")
            
        except Exception as e:
            logger.error(f"Error in ML model updates: {e}")
    
    def run_full_pipeline(self):
        """Run the complete data pipeline"""
        start_time = datetime.now()
        logger.info("=== Starting Full Data Pipeline ===")
        
        try:
            # Collect traffic data
            self.collect_traffic_data()
            
            # Process vehicle data (less frequently)
            if datetime.now().hour % 6 == 0:  # Every 6 hours
                self.process_vehicle_data()
            
            # Update ML models (once per hour)
            if datetime.now().minute == 0:
                self.update_ml_models()
            
            duration = datetime.now() - start_time
            logger.info(f"=== Pipeline completed in {duration} ===")
            
        except Exception as e:
            logger.error(f"Error in full pipeline: {e}")

def setup_scheduler():
    """Setup the pipeline scheduler"""
    orchestrator = DataPipelineOrchestrator()
    
    # Schedule traffic data collection every 15 minutes
    schedule.every(15).minutes.do(orchestrator.collect_traffic_data)
    
    # Schedule vehicle data processing every 6 hours
    schedule.every(6).hours.do(orchestrator.process_vehicle_data)
    
    # Schedule ML model updates every hour
    schedule.every().hour.do(orchestrator.update_ml_models)
    
    # Schedule full pipeline run every 30 minutes
    schedule.every(30).minutes.do(orchestrator.run_full_pipeline)
    
    logger.info("Pipeline scheduler configured")
    return orchestrator

def main():
    """Main function"""
    logger.info("Starting DriveWise AI Data Pipeline")
    
    # Setup environment
    os.makedirs('/app/logs', exist_ok=True)
    
    try:
        orchestrator = setup_scheduler()
        
        # Run initial pipeline
        logger.info("Running initial pipeline...")
        orchestrator.run_full_pipeline()
        
        # Start scheduler
        logger.info("Starting pipeline scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("Pipeline stopped by user")
    except Exception as e:
        logger.error(f"Fatal error in pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()