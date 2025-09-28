from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from typing import Dict, List, Any, Optional
import pandas as pd
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class BigQueryService:
    def __init__(self):
        """Initialize BigQuery client"""
        self.client = bigquery.Client()
        self.dataset_id = os.getenv("BIGQUERY_DATASET_ID", "drivewise_ai")
        self.project_id = os.getenv("GCP_PROJECT_ID")
        
        # Table names
        self.tables = {
            "driving_data": "driving_data",
            "risk_scores": "risk_scores",
            "safety_scores": "safety_scores",
            "traffic_data": "traffic_data",
            "vehicle_data": "vehicle_data",
            "user_profiles": "user_profiles"
        }
        
        # Initialize dataset and tables
        self._initialize_dataset()
    
    def _initialize_dataset(self):
        """Create dataset and tables if they don't exist"""
        try:
            # Create dataset
            dataset_ref = self.client.dataset(self.dataset_id)
            try:
                self.client.get_dataset(dataset_ref)
                logger.info(f"Dataset {self.dataset_id} already exists")
            except NotFound:
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = "US"
                dataset = self.client.create_dataset(dataset)
                logger.info(f"Created dataset {self.dataset_id}")
            
            # Create tables
            self._create_tables()
            
        except Exception as e:
            logger.error(f"Error initializing BigQuery dataset: {e}")
            raise
    
    def _create_tables(self):
        """Create all required tables"""
        
        # Driving data table schema
        driving_data_schema = [
            bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("trip_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("vehicle_make", "STRING"),
            bigquery.SchemaField("vehicle_model", "STRING"),
            bigquery.SchemaField("vehicle_year", "INTEGER"),
            bigquery.SchemaField("start_lat", "FLOAT"),
            bigquery.SchemaField("start_lon", "FLOAT"),
            bigquery.SchemaField("end_lat", "FLOAT"),
            bigquery.SchemaField("end_lon", "FLOAT"),
            bigquery.SchemaField("distance_km", "FLOAT"),
            bigquery.SchemaField("duration_seconds", "FLOAT"),
            bigquery.SchemaField("avg_speed_kmh", "FLOAT"),
            bigquery.SchemaField("max_speed_kmh", "FLOAT"),
            bigquery.SchemaField("events", "JSON"),
            bigquery.SchemaField("weather_conditions", "STRING"),
            bigquery.SchemaField("traffic_conditions", "STRING"),
        ]
        
        # Risk scores table schema
        risk_scores_schema = [
            bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("overall_score", "FLOAT"),
            bigquery.SchemaField("speeding_score", "FLOAT"),
            bigquery.SchemaField("hard_braking_score", "FLOAT"),
            bigquery.SchemaField("acceleration_score", "FLOAT"),
            bigquery.SchemaField("distraction_score", "FLOAT"),
            bigquery.SchemaField("time_of_day_score", "FLOAT"),
            bigquery.SchemaField("weather_score", "FLOAT"),
            bigquery.SchemaField("traffic_score", "FLOAT"),
            bigquery.SchemaField("confidence", "FLOAT"),
            bigquery.SchemaField("version", "STRING"),
        ]
        
        # Safety scores table schema
        safety_scores_schema = [
            bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("overall_score", "FLOAT"),
            bigquery.SchemaField("safe_following_distance", "FLOAT"),
            bigquery.SchemaField("smooth_acceleration", "FLOAT"),
            bigquery.SchemaField("smooth_braking", "FLOAT"),
            bigquery.SchemaField("speed_limit_adherence", "FLOAT"),
            bigquery.SchemaField("defensive_driving", "FLOAT"),
            bigquery.SchemaField("attention_level", "FLOAT"),
            bigquery.SchemaField("comparative_ranking", "INTEGER"),
            bigquery.SchemaField("improvement_suggestions", "JSON"),
            bigquery.SchemaField("version", "STRING"),
        ]
        
        # Traffic data table schema
        traffic_data_schema = [
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("location_lat", "FLOAT"),
            bigquery.SchemaField("location_lon", "FLOAT"),
            bigquery.SchemaField("congestion_level", "FLOAT"),
            bigquery.SchemaField("average_speed", "FLOAT"),
            bigquery.SchemaField("incident_count", "INTEGER"),
            bigquery.SchemaField("road_type", "STRING"),
            bigquery.SchemaField("weather", "STRING"),
            bigquery.SchemaField("source", "STRING"),
        ]
        
        schemas = {
            "driving_data": driving_data_schema,
            "risk_scores": risk_scores_schema,
            "safety_scores": safety_scores_schema,
            "traffic_data": traffic_data_schema,
        }
        
        for table_name, schema in schemas.items():
            self._create_table_if_not_exists(table_name, schema)
    
    def _create_table_if_not_exists(self, table_name: str, schema: List[bigquery.SchemaField]):
        """Create table if it doesn't exist"""
        table_ref = self.client.dataset(self.dataset_id).table(table_name)
        
        try:
            self.client.get_table(table_ref)
            logger.info(f"Table {table_name} already exists")
        except NotFound:
            table = bigquery.Table(table_ref, schema=schema)
            table = self.client.create_table(table)
            logger.info(f"Created table {table_name}")
    
    async def insert_driving_data(self, data: Dict[str, Any]) -> bool:
        """Insert driving data into BigQuery"""
        try:
            table_ref = self.client.dataset(self.dataset_id).table("driving_data")
            
            # Transform data for BigQuery
            row = {
                "user_id": data["user_id"],
                "trip_id": data["trip"]["trip_id"],
                "timestamp": data["timestamp"],
                "vehicle_make": data["vehicle"]["make"],
                "vehicle_model": data["vehicle"]["model"],
                "vehicle_year": data["vehicle"]["year"],
                "start_lat": data["trip"]["start_location"]["latitude"],
                "start_lon": data["trip"]["start_location"]["longitude"],
                "end_lat": data["trip"]["end_location"]["latitude"],
                "end_lon": data["trip"]["end_location"]["longitude"],
                "distance_km": data["trip"]["distance"],
                "duration_seconds": data["trip"]["duration"],
                "avg_speed_kmh": data["trip"]["avg_speed"],
                "max_speed_kmh": data["trip"]["max_speed"],
                "events": data["trip"]["events"],
                "weather_conditions": data["trip"].get("weather_conditions"),
                "traffic_conditions": data["trip"].get("traffic_conditions"),
            }
            
            errors = self.client.insert_rows_json(table_ref, [row])
            
            if errors:
                logger.error(f"Error inserting driving data: {errors}")
                return False
            
            logger.info(f"Successfully inserted driving data for user {data['user_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting driving data: {e}")
            return False
    
    async def get_user_driving_history(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get driving history for a user"""
        query = f"""
        SELECT *
        FROM `{self.project_id}.{self.dataset_id}.driving_data`
        WHERE user_id = @user_id
        AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
        ORDER BY timestamp DESC
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("days", "INT64", days),
            ]
        )
        
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [dict(row) for row in results]
    
    async def get_risk_trends(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get risk score trends for a user"""
        query = f"""
        SELECT 
            DATE(timestamp) as date,
            AVG(overall_score) as avg_risk_score,
            AVG(speeding_score) as avg_speeding_score,
            AVG(hard_braking_score) as avg_braking_score
        FROM `{self.project_id}.{self.dataset_id}.risk_scores`
        WHERE user_id = @user_id
        AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("days", "INT64", days),
            ]
        )
        
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [dict(row) for row in results]
    
    async def get_traffic_hotspots(self, lat: float, lon: float, radius: float) -> List[Dict[str, Any]]:
        """Get traffic hotspots in a geographic area"""
        query = f"""
        SELECT 
            location_lat,
            location_lon,
            AVG(congestion_level) as avg_congestion,
            COUNT(*) as incident_count
        FROM `{self.project_id}.{self.dataset_id}.traffic_data`
        WHERE ST_DWITHIN(
            ST_GEOGPOINT(location_lon, location_lat),
            ST_GEOGPOINT(@lon, @lat),
            @radius * 1000  -- Convert km to meters
        )
        AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
        GROUP BY location_lat, location_lon
        HAVING avg_congestion > 0.7
        ORDER BY avg_congestion DESC
        LIMIT 50
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("lat", "FLOAT64", lat),
                bigquery.ScalarQueryParameter("lon", "FLOAT64", lon),
                bigquery.ScalarQueryParameter("radius", "FLOAT64", radius),
            ]
        )
        
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [dict(row) for row in results]
    
    async def health_check(self) -> bool:
        """Check if BigQuery service is healthy"""
        try:
            # Simple query to test connection
            query = "SELECT 1 as test"
            query_job = self.client.query(query)
            results = query_job.result()
            
            return True
        except Exception as e:
            logger.error(f"BigQuery health check failed: {e}")
            return False