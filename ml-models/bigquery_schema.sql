-- DriveWise AI BigQuery Schema Setup
-- This file contains all the SQL schemas and ML models for the DriveWise AI platform

-- Create the main dataset
CREATE SCHEMA IF NOT EXISTS `drivewise_ai`
OPTIONS (
  description = "DriveWise AI - Driving insights and insurance risk platform",
  location = "US"
);

-- ============================================================================
-- RAW DATA TABLES
-- ============================================================================

-- Driving data table
CREATE OR REPLACE TABLE `drivewise_ai.driving_data` (
  user_id STRING NOT NULL,
  trip_id STRING NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  vehicle_make STRING,
  vehicle_model STRING,
  vehicle_year INT64,
  vehicle_vin STRING,
  start_lat FLOAT64,
  start_lon FLOAT64,
  end_lat FLOAT64,
  end_lon FLOAT64,
  distance_km FLOAT64,
  duration_seconds FLOAT64,
  avg_speed_kmh FLOAT64,
  max_speed_kmh FLOAT64,
  events JSON,
  weather_conditions STRING,
  traffic_conditions STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id;

-- Traffic data table
CREATE OR REPLACE TABLE `drivewise_ai.traffic_data` (
  timestamp TIMESTAMP NOT NULL,
  location_lat FLOAT64,
  location_lon FLOAT64,
  congestion_level FLOAT64,
  average_speed FLOAT64,
  incident_count INT64,
  road_type STRING,
  weather STRING,
  source STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp)
CLUSTER BY location_lat, location_lon;

-- Vehicle safety data table
CREATE OR REPLACE TABLE `drivewise_ai.vehicle_data` (
  vin STRING NOT NULL,
  make STRING,
  model STRING,
  year INT64,
  safety_rating FLOAT64,
  recall_count INT64,
  crash_test_rating JSON,
  timestamp TIMESTAMP,
  source STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY vin;

-- User profiles table
CREATE OR REPLACE TABLE `drivewise_ai.user_profiles` (
  user_id STRING NOT NULL,
  age INT64,
  driving_experience_years INT64,
  license_type STRING,
  annual_mileage FLOAT64,
  primary_vehicle_vin STRING,
  location_lat FLOAT64,
  location_lon FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY user_id;

-- ============================================================================
-- PROCESSED DATA TABLES
-- ============================================================================

-- Risk scores table
CREATE OR REPLACE TABLE `drivewise_ai.risk_scores` (
  user_id STRING NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  overall_score FLOAT64,
  speeding_score FLOAT64,
  hard_braking_score FLOAT64,
  acceleration_score FLOAT64,
  distraction_score FLOAT64,
  time_of_day_score FLOAT64,
  weather_score FLOAT64,
  traffic_score FLOAT64,
  confidence FLOAT64,
  model_version STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id;

-- Safety scores table
CREATE OR REPLACE TABLE `drivewise_ai.safety_scores` (
  user_id STRING NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  overall_score FLOAT64,
  safe_following_distance FLOAT64,
  smooth_acceleration FLOAT64,
  smooth_braking FLOAT64,
  speed_limit_adherence FLOAT64,
  defensive_driving FLOAT64,
  attention_level FLOAT64,
  comparative_ranking INT64,
  improvement_suggestions JSON,
  model_version STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id;

-- ============================================================================
-- FEATURE ENGINEERING VIEWS
-- ============================================================================

-- Daily driving metrics view
CREATE OR REPLACE VIEW `drivewise_ai.daily_driving_metrics` AS
SELECT 
  user_id,
  DATE(timestamp) as driving_date,
  COUNT(DISTINCT trip_id) as trip_count,
  SUM(distance_km) as total_distance,
  AVG(avg_speed_kmh) as avg_speed,
  MAX(max_speed_kmh) as max_speed,
  SUM(duration_seconds) / 3600 as total_driving_hours,
  
  -- Event analysis
  SUM(JSON_EXTRACT_SCALAR(event, '$.event_type') = 'hard_brake' FOR event IN UNNEST(JSON_EXTRACT_ARRAY(events))) as hard_brake_count,
  SUM(JSON_EXTRACT_SCALAR(event, '$.event_type') = 'rapid_acceleration' FOR event IN UNNEST(JSON_EXTRACT_ARRAY(events))) as rapid_acceleration_count,
  SUM(JSON_EXTRACT_SCALAR(event, '$.event_type') = 'speeding' FOR event IN UNNEST(JSON_EXTRACT_ARRAY(events))) as speeding_count,
  SUM(JSON_EXTRACT_SCALAR(event, '$.event_type') = 'sharp_turn' FOR event IN UNNEST(JSON_EXTRACT_ARRAY(events))) as sharp_turn_count,
  
  -- Time of day analysis
  AVG(CASE WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 6 AND 9 THEN 1 ELSE 0 END) as morning_rush_ratio,
  AVG(CASE WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 17 AND 19 THEN 1 ELSE 0 END) as evening_rush_ratio,
  AVG(CASE WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 22 AND 5 THEN 1 ELSE 0 END) as night_driving_ratio

FROM `drivewise_ai.driving_data`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY user_id, DATE(timestamp);

-- Weekly risk trends view
CREATE OR REPLACE VIEW `drivewise_ai.weekly_risk_trends` AS
SELECT 
  user_id,
  DATE_TRUNC(DATE(timestamp), WEEK) as week_start,
  AVG(overall_score) as avg_risk_score,
  AVG(speeding_score) as avg_speeding_score,
  AVG(hard_braking_score) as avg_braking_score,
  AVG(acceleration_score) as avg_acceleration_score,
  COUNT(*) as score_count
FROM `drivewise_ai.risk_scores`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 12 WEEK)
GROUP BY user_id, DATE_TRUNC(DATE(timestamp), WEEK);

-- Traffic hotspots view
CREATE OR REPLACE VIEW `drivewise_ai.traffic_hotspots` AS
SELECT 
  ROUND(location_lat, 3) as lat_rounded,
  ROUND(location_lon, 3) as lon_rounded,
  AVG(congestion_level) as avg_congestion,
  AVG(average_speed) as avg_speed,
  SUM(incident_count) as total_incidents,
  COUNT(*) as measurement_count
FROM `drivewise_ai.traffic_data`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND congestion_level > 0.5
GROUP BY lat_rounded, lon_rounded
HAVING measurement_count >= 10
ORDER BY avg_congestion DESC;

-- ============================================================================
-- MACHINE LEARNING MODELS
-- ============================================================================

-- Risk scoring model
CREATE OR REPLACE MODEL `drivewise_ai.risk_scoring_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['risk_label'],
  auto_class_weights=TRUE
) AS
SELECT 
  -- Features
  trip_count,
  total_distance,
  avg_speed,
  max_speed,
  total_driving_hours,
  hard_brake_count / GREATEST(trip_count, 1) as hard_brake_rate,
  rapid_acceleration_count / GREATEST(trip_count, 1) as acceleration_rate,
  speeding_count / GREATEST(trip_count, 1) as speeding_rate,
  sharp_turn_count / GREATEST(trip_count, 1) as sharp_turn_rate,
  morning_rush_ratio,
  evening_rush_ratio,
  night_driving_ratio,
  
  -- Vehicle features (will be joined)
  COALESCE(v.safety_rating, 3.0) as vehicle_safety_rating,
  COALESCE(v.recall_count, 0) as vehicle_recall_count,
  
  -- Target variable (high risk = 1, low risk = 0)
  CASE 
    WHEN (hard_brake_count / GREATEST(trip_count, 1)) > 0.1
         OR (speeding_count / GREATEST(trip_count, 1)) > 0.2
         OR max_speed > 120
    THEN 1 
    ELSE 0 
  END as risk_label

FROM `drivewise_ai.daily_driving_metrics` dm
LEFT JOIN (SELECT DISTINCT vin, safety_rating, recall_count FROM `drivewise_ai.vehicle_data`) v
  ON v.vin IN (SELECT vehicle_vin FROM `drivewise_ai.driving_data` dd WHERE dd.user_id = dm.user_id LIMIT 1)
WHERE dm.driving_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY);

-- Safety scoring model (regression)
CREATE OR REPLACE MODEL `drivewise_ai.safety_scoring_model`
OPTIONS(
  model_type='LINEAR_REG',
  input_label_cols=['safety_score']
) AS
SELECT 
  -- Features
  trip_count,
  total_distance,
  avg_speed,
  total_driving_hours,
  1.0 - (hard_brake_count / GREATEST(total_distance, 1)) as smooth_braking_score,
  1.0 - (rapid_acceleration_count / GREATEST(total_distance, 1)) as smooth_acceleration_score,
  1.0 - (speeding_count / GREATEST(total_distance, 1)) as speed_adherence_score,
  CASE WHEN avg_speed BETWEEN 40 AND 80 THEN 1.0 ELSE 0.5 END as safe_speed_score,
  1.0 - night_driving_ratio as safe_timing_score,
  
  -- Target variable (composite safety score 0-100)
  LEAST(100, GREATEST(0, 
    100 - (hard_brake_count / GREATEST(trip_count, 1) * 50) - 
          (speeding_count / GREATEST(trip_count, 1) * 30) - 
          (rapid_acceleration_count / GREATEST(trip_count, 1) * 20)
  )) as safety_score

FROM `drivewise_ai.daily_driving_metrics`
WHERE driving_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
  AND trip_count > 0;

-- ============================================================================
-- PREDICTION FUNCTIONS
-- ============================================================================

-- Function to predict risk score for a user
CREATE OR REPLACE FUNCTION `drivewise_ai.predict_risk_score`(
  user_id STRING,
  days_lookback INT64
) AS (
  SELECT predicted_risk_label_probs[OFFSET(1)].prob as risk_probability
  FROM ML.PREDICT(
    MODEL `drivewise_ai.risk_scoring_model`,
    (
      SELECT 
        trip_count,
        total_distance,
        avg_speed,
        max_speed,
        total_driving_hours,
        hard_brake_count / GREATEST(trip_count, 1) as hard_brake_rate,
        rapid_acceleration_count / GREATEST(trip_count, 1) as acceleration_rate,
        speeding_count / GREATEST(trip_count, 1) as speeding_rate,
        sharp_turn_count / GREATEST(trip_count, 1) as sharp_turn_rate,
        morning_rush_ratio,
        evening_rush_ratio,
        night_driving_ratio,
        3.0 as vehicle_safety_rating,
        0 as vehicle_recall_count
      FROM `drivewise_ai.daily_driving_metrics`
      WHERE user_id = user_id
        AND driving_date >= DATE_SUB(CURRENT_DATE(), INTERVAL days_lookback DAY)
      ORDER BY driving_date DESC
      LIMIT 1
    )
  )
);

-- Function to predict safety score for a user
CREATE OR REPLACE FUNCTION `drivewise_ai.predict_safety_score`(
  user_id STRING,
  days_lookback INT64
) AS (
  SELECT predicted_safety_score
  FROM ML.PREDICT(
    MODEL `drivewise_ai.safety_scoring_model`,
    (
      SELECT 
        trip_count,
        total_distance,
        avg_speed,
        total_driving_hours,
        1.0 - (hard_brake_count / GREATEST(total_distance, 1)) as smooth_braking_score,
        1.0 - (rapid_acceleration_count / GREATEST(total_distance, 1)) as smooth_acceleration_score,
        1.0 - (speeding_count / GREATEST(total_distance, 1)) as speed_adherence_score,
        CASE WHEN avg_speed BETWEEN 40 AND 80 THEN 1.0 ELSE 0.5 END as safe_speed_score,
        1.0 - night_driving_ratio as safe_timing_score
      FROM `drivewise_ai.daily_driving_metrics`
      WHERE user_id = user_id
        AND driving_date >= DATE_SUB(CURRENT_DATE(), INTERVAL days_lookback DAY)
      ORDER BY driving_date DESC
      LIMIT 1
    )
  )
);

-- ============================================================================
-- BATCH SCORING PROCEDURES
-- ============================================================================

-- Procedure to update risk scores for all users
CREATE OR REPLACE PROCEDURE `drivewise_ai.update_risk_scores`()
BEGIN
  -- Calculate and insert new risk scores
  INSERT INTO `drivewise_ai.risk_scores` (
    user_id, timestamp, overall_score, speeding_score, hard_braking_score,
    acceleration_score, distraction_score, time_of_day_score, 
    weather_score, traffic_score, confidence, model_version
  )
  SELECT 
    dm.user_id,
    CURRENT_TIMESTAMP() as timestamp,
    `drivewise_ai.predict_risk_score`(dm.user_id, 7) as overall_score,
    LEAST(1.0, speeding_count / GREATEST(trip_count, 1) * 5) as speeding_score,
    LEAST(1.0, hard_brake_count / GREATEST(trip_count, 1) * 10) as hard_braking_score,
    LEAST(1.0, rapid_acceleration_count / GREATEST(trip_count, 1) * 10) as acceleration_score,
    0.1 as distraction_score, -- Placeholder
    CASE 
      WHEN night_driving_ratio > 0.3 THEN 0.8
      WHEN (morning_rush_ratio + evening_rush_ratio) > 0.4 THEN 0.6
      ELSE 0.2 
    END as time_of_day_score,
    0.3 as weather_score, -- Placeholder
    0.4 as traffic_score, -- Placeholder
    0.85 as confidence,
    'v1.0' as model_version
  FROM (
    SELECT user_id, 
           SUM(trip_count) as trip_count,
           SUM(speeding_count) as speeding_count,
           SUM(hard_brake_count) as hard_brake_count,
           SUM(rapid_acceleration_count) as rapid_acceleration_count,
           AVG(night_driving_ratio) as night_driving_ratio,
           AVG(morning_rush_ratio) as morning_rush_ratio,
           AVG(evening_rush_ratio) as evening_rush_ratio
    FROM `drivewise_ai.daily_driving_metrics`
    WHERE driving_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY user_id
    HAVING trip_count > 0
  ) dm;
END;

-- Procedure to update safety scores for all users
CREATE OR REPLACE PROCEDURE `drivewise_ai.update_safety_scores`()
BEGIN
  INSERT INTO `drivewise_ai.safety_scores` (
    user_id, timestamp, overall_score, safe_following_distance,
    smooth_acceleration, smooth_braking, speed_limit_adherence,
    defensive_driving, attention_level, comparative_ranking,
    improvement_suggestions, model_version
  )
  SELECT 
    dm.user_id,
    CURRENT_TIMESTAMP() as timestamp,
    `drivewise_ai.predict_safety_score`(dm.user_id, 7) as overall_score,
    0.8 as safe_following_distance, -- Placeholder
    1.0 - (rapid_acceleration_count / GREATEST(trip_count, 1) * 5) as smooth_acceleration,
    1.0 - (hard_brake_count / GREATEST(trip_count, 1) * 5) as smooth_braking,
    1.0 - (speeding_count / GREATEST(trip_count, 1) * 3) as speed_limit_adherence,
    0.75 as defensive_driving, -- Placeholder
    1.0 - night_driving_ratio as attention_level,
    PERCENT_RANK() OVER (ORDER BY `drivewise_ai.predict_safety_score`(dm.user_id, 7)) * 100 as comparative_ranking,
    JSON_ARRAY(
      IF(speeding_count > trip_count * 0.1, 'Reduce speeding incidents', NULL),
      IF(hard_brake_count > trip_count * 0.1, 'Practice smoother braking', NULL),
      IF(night_driving_ratio > 0.3, 'Avoid night driving when possible', NULL)
    ) as improvement_suggestions,
    'v1.0' as model_version
  FROM (
    SELECT user_id, 
           SUM(trip_count) as trip_count,
           SUM(speeding_count) as speeding_count,
           SUM(hard_brake_count) as hard_brake_count,
           SUM(rapid_acceleration_count) as rapid_acceleration_count,
           AVG(night_driving_ratio) as night_driving_ratio
    FROM `drivewise_ai.daily_driving_metrics`
    WHERE driving_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY user_id
    HAVING trip_count > 0
  ) dm;
END;