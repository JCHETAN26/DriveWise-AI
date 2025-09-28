import React from 'react';
import { ScoreCard } from '../components/ScoreCard';
import { TrendChart } from '../components/TrendChart';
import { RecentTrips } from '../components/RecentTrips';
import { TrafficMap } from '../components/TrafficMap';
import { InsuranceQuote } from '../components/InsuranceQuote';

export const Dashboard: React.FC = () => {
  // Mock data for demo
  const mockData = {
    riskScore: {
      overall_score: 0.25,
      risk_factors: {
        speeding_score: 0.15,
        hard_braking_score: 0.35,
        acceleration_score: 0.20,
        distraction_score: 0.10
      }
    },
    safetyScore: {
      overall_score: 78.5,
      safety_metrics: {
        safe_following_distance: 0.82,
        smooth_acceleration: 0.91,
        speed_limit_adherence: 0.76
      }
    },
    recentTrips: [
      { id: 1, distance_km: 25.3, avg_speed_kmh: 45.2 },
      { id: 2, distance_km: 18.7, avg_speed_kmh: 52.1 }
    ],
    trends: [],
    trafficHotspots: [],
    insuranceQuote: {}
  };

  const riskScoreColor = mockData.riskScore.overall_score < 0.3 ? 'green' : 
                        mockData.riskScore.overall_score < 0.7 ? 'yellow' : 'red';
  
  const safetyScoreColor = mockData.safetyScore.overall_score > 80 ? 'green' : 
                          mockData.safetyScore.overall_score > 60 ? 'yellow' : 'red';

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">DriveWise AI Dashboard</h1>
        <p className="text-gray-600">Your personalized driving insights and insurance risk analysis</p>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ScoreCard
          title="Risk Score"
          score={Math.round((1 - mockData.riskScore.overall_score) * 100)}
          maxScore={100}
          color={riskScoreColor}
          icon={<span>🛡️</span>}
          description="Lower risk = Lower premiums"
          details={[
            { label: 'Speeding', value: Math.round((1 - mockData.riskScore.risk_factors.speeding_score) * 100) },
            { label: 'Braking', value: Math.round((1 - mockData.riskScore.risk_factors.hard_braking_score) * 100) },
            { label: 'Acceleration', value: Math.round((1 - mockData.riskScore.risk_factors.acceleration_score) * 100) }
          ]}
        />

        <ScoreCard
          title="Safety Score"
          score={Math.round(mockData.safetyScore.overall_score)}
          maxScore={100}
          color={safetyScoreColor}
          icon={<span>📈</span>}
          description="Your driving safety rating"
          details={[
            { label: 'Following Distance', value: Math.round(mockData.safetyScore.safety_metrics.safe_following_distance * 100) },
            { label: 'Smooth Acceleration', value: Math.round(mockData.safetyScore.safety_metrics.smooth_acceleration * 100) },
            { label: 'Speed Adherence', value: Math.round(mockData.safetyScore.safety_metrics.speed_limit_adherence * 100) }
          ]}
        />

        <ScoreCard
          title="Weekly Trips"
          score={mockData.recentTrips.length}
          maxScore={null}
          color="blue"
          icon={<span>📍</span>}
          description="Trips this week"
          details={[
            { label: 'Total Distance', value: `${mockData.recentTrips.reduce((sum, trip) => sum + trip.distance_km, 0).toFixed(1)} km` },
            { label: 'Avg Speed', value: `${(mockData.recentTrips.reduce((sum, trip) => sum + trip.avg_speed_kmh, 0) / mockData.recentTrips.length).toFixed(1)} km/h` }
          ]}
        />
      </div>

      {/* Charts and Maps */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Risk Trends</h2>
          <TrendChart data={mockData.trends} />
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Traffic Hotspots</h2>
          <TrafficMap hotspots={mockData.trafficHotspots} />
        </div>
      </div>

      {/* Recent Activity and Insurance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Trips</h2>
          <RecentTrips trips={mockData.recentTrips} />
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Insurance Quote</h2>
          <InsuranceQuote quote={mockData.insuranceQuote} />
        </div>
      </div>
    </div>
  );
};