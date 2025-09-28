from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, ChatSession
from vertexai.language_models import TextGenerationModel
import vertexai
from typing import Dict, List, Any, Optional
import json
import logging
import os

logger = logging.getLogger(__name__)

class VertexAIService:
    def __init__(self):
        """Initialize Vertex AI service"""
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        
        # Initialize Vertex AI
        vertexai.init(project=self.project_id, location=self.location)
        
        # Initialize models
        self.chat_model = GenerativeModel("gemini-pro")
        self.text_model = TextGenerationModel.from_pretrained("text-bison@001")
        
        # Chat session for maintaining context
        self.chat_sessions: Dict[str, ChatSession] = {}
    
    async def chat(self, message: str, user_context: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> str:
        """Chat with the DriveWise AI agent"""
        try:
            # Build context-aware prompt
            system_prompt = self._build_system_prompt(user_context)
            full_message = f"{system_prompt}\n\nUser: {message}"
            
            # Get or create chat session
            user_id = user_context.get("user_id")
            if user_id not in self.chat_sessions:
                self.chat_sessions[user_id] = self.chat_model.start_chat()
            
            chat_session = self.chat_sessions[user_id]
            
            # Send message and get response
            response = chat_session.send_message(full_message)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."
    
    def _build_system_prompt(self, user_context: Dict[str, Any]) -> str:
        """Build system prompt with user context"""
        
        risk_score = user_context.get("risk_score", {})
        safety_score = user_context.get("safety_score", {})
        recent_trips = user_context.get("recent_trips", [])
        
        prompt = f"""
You are DriveWise AI, an intelligent driving assistant that helps users understand their driving behavior and insurance risk. You have access to the following user data:

CURRENT RISK SCORE: {risk_score.get('overall_score', 'N/A')}
- Speeding: {risk_score.get('speeding_score', 'N/A')}
- Hard Braking: {risk_score.get('hard_braking_score', 'N/A')}
- Acceleration: {risk_score.get('acceleration_score', 'N/A')}
- Distraction: {risk_score.get('distraction_score', 'N/A')}

CURRENT SAFETY SCORE: {safety_score.get('overall_score', 'N/A')}/100
- Following Distance: {safety_score.get('safe_following_distance', 'N/A')}
- Smooth Acceleration: {safety_score.get('smooth_acceleration', 'N/A')}
- Speed Limit Adherence: {safety_score.get('speed_limit_adherence', 'N/A')}

RECENT DRIVING ACTIVITY: {len(recent_trips)} trips in the last 7 days

Guidelines:
- Be conversational and helpful
- Provide specific, actionable insights based on the data
- Explain complex driving metrics in simple terms
- Offer personalized suggestions for improvement
- Reference specific data points when relevant
- Be encouraging while being honest about areas for improvement
- If asked about insurance implications, explain how behavior affects premiums

Example responses:
- "Based on your recent driving, your safety score is 85/100, which is great! Your smooth braking is excellent at 0.92, but there's room to improve your following distance."
- "I noticed you had 3 hard braking events this week. These typically happen in heavy traffic - try leaving more space between cars."
- "Your speeding score of 0.15 means you exceed speed limits about 15% of the time. Reducing this could lower your insurance premium by 10-15%."
"""
        
        return prompt
    
    async def analyze_driving_pattern(self, driving_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze driving patterns using AI"""
        try:
            # Prepare data summary for analysis
            data_summary = self._prepare_data_summary(driving_data)
            
            prompt = f"""
Analyze the following driving data and provide insights:

{json.dumps(data_summary, indent=2)}

Provide analysis in JSON format with:
1. "key_insights": List of main observations
2. "risk_factors": Identified risk areas
3. "improvements": Specific suggestions
4. "trends": Notable patterns over time
5. "score_explanation": Why the current scores are what they are
"""
            
            response = self.text_model.predict(
                prompt=prompt,
                temperature=0.3,
                max_output_tokens=1024
            )
            
            # Try to parse as JSON, fallback to text
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return {"analysis": response.text}
                
        except Exception as e:
            logger.error(f"Error analyzing driving pattern: {e}")
            return {"error": "Unable to analyze driving pattern"}
    
    def _prepare_data_summary(self, driving_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare driving data summary for AI analysis"""
        if not driving_data:
            return {"message": "No driving data available"}
        
        # Calculate summary statistics
        total_trips = len(driving_data)
        total_distance = sum(trip.get("distance_km", 0) for trip in driving_data)
        avg_speed = sum(trip.get("avg_speed_kmh", 0) for trip in driving_data) / total_trips if total_trips > 0 else 0
        
        # Count events
        event_counts = {}
        for trip in driving_data:
            events = trip.get("events", [])
            for event in events:
                event_type = event.get("event_type", "unknown")
                event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Time patterns
        trip_times = []
        for trip in driving_data:
            timestamp = trip.get("timestamp")
            if timestamp:
                trip_times.append(timestamp)
        
        return {
            "summary": {
                "total_trips": total_trips,
                "total_distance_km": round(total_distance, 2),
                "average_speed_kmh": round(avg_speed, 2),
                "event_counts": event_counts,
                "time_period": f"Last {len(driving_data)} trips"
            },
            "recent_patterns": {
                "most_common_events": sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "average_trip_distance": round(total_distance / total_trips, 2) if total_trips > 0 else 0
            }
        }
    
    async def generate_improvement_suggestions(self, risk_factors: Dict[str, float], safety_metrics: Dict[str, float]) -> List[str]:
        """Generate personalized improvement suggestions"""
        try:
            prompt = f"""
Based on these driving metrics, provide 3-5 specific, actionable improvement suggestions:

Risk Factors (0-1, where 1 is highest risk):
- Speeding: {risk_factors.get('speeding_score', 0)}
- Hard Braking: {risk_factors.get('hard_braking_score', 0)}
- Acceleration: {risk_factors.get('acceleration_score', 0)}
- Distraction: {risk_factors.get('distraction_score', 0)}

Safety Metrics (0-1, where 1 is best):
- Following Distance: {safety_metrics.get('safe_following_distance', 0)}
- Smooth Acceleration: {safety_metrics.get('smooth_acceleration', 0)}
- Speed Limit Adherence: {safety_metrics.get('speed_limit_adherence', 0)}

Provide suggestions as a JSON array of strings, each being a specific, actionable tip.
Focus on the areas that need the most improvement.
"""
            
            response = self.text_model.predict(
                prompt=prompt,
                temperature=0.4,
                max_output_tokens=512
            )
            
            try:
                suggestions = json.loads(response.text)
                return suggestions if isinstance(suggestions, list) else [response.text]
            except json.JSONDecodeError:
                # Fallback: split by lines and clean up
                lines = response.text.strip().split('\n')
                return [line.strip('- ').strip() for line in lines if line.strip()]
                
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return ["Focus on maintaining safe following distances", "Monitor your speed regularly", "Practice smooth acceleration and braking"]
    
    async def health_check(self) -> bool:
        """Check if Vertex AI service is healthy"""
        try:
            # Simple test prediction
            response = self.text_model.predict(
                prompt="Test prompt",
                max_output_tokens=10
            )
            return bool(response.text)
        except Exception as e:
            logger.error(f"Vertex AI health check failed: {e}")
            return False