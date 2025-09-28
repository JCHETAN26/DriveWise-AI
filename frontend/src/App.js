import React, { useState, useEffect } from 'react';
import { ChatDemo } from './components/ChatDemo';
import { UserSelector } from './components/UserSelector';
import { InsurancePortal } from './components/InsurancePortal';
import './App.css';

function App() {
  const [appMode, setAppMode] = useState('demo'); // 'demo', 'insurance'
  const [currentView, setCurrentView] = useState('dashboard');
  const [currentUserId, setCurrentUserId] = useState('user123');
  const [userData, setUserData] = useState(null);
  const [riskScore, setRiskScore] = useState(null);
  const [safetyScore, setSafetyScore] = useState(null);
  const [vehicleSafety, setVehicleSafety] = useState(null);
  const [isLiveMode, setIsLiveMode] = useState(false);
  const [liveDataCount, setLiveDataCount] = useState(0);

  // Define fetchUserData function that can be reused
  const fetchUserData = async () => {
    try {
      const [userResponse, riskResponse, safetyResponse, vehicleResponse] = await Promise.all([
        fetch(`http://localhost:8005/api/v1/user/${currentUserId}`),
        fetch(`http://localhost:8005/api/v1/enhanced-risk-score/${currentUserId}`),
        fetch(`http://localhost:8005/api/v1/safety-score/${currentUserId}`),
        fetch(`http://localhost:8005/api/v1/vehicle-safety/${currentUserId}`)
      ]);

      const [user, risk, safety, vehicle] = await Promise.all([
        userResponse.json(),
        riskResponse.json(),
        safetyResponse.json(),
        vehicleResponse.json()
      ]);

      setUserData(user);
      setRiskScore(risk);
      setSafetyScore(safety);
      setVehicleSafety(vehicle);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  // Fetch user data when user changes
  useEffect(() => {
    fetchUserData();
  }, [currentUserId]);

  // Real-time data streaming effect
  useEffect(() => {
    let interval;
    if (isLiveMode) {
      interval = setInterval(() => {
        // Fetch updated data every 6 seconds (10 requests per minute)
        fetchUserData();
        setLiveDataCount(prev => prev + 1);
      }, 6000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isLiveMode, currentUserId]);

  const toggleLiveMode = () => {
    setIsLiveMode(!isLiveMode);
    if (!isLiveMode) {
      setLiveDataCount(0);
      // Immediately fetch fresh data when starting live mode
      setTimeout(() => {
        fetchUserData();
      }, 500);
    }
  };

  // If in insurance portal mode, show the insurance dashboard
  if (appMode === 'insurance') {
    return (
      <div>
        {/* Back to Demo Button */}
        <div className="bg-indigo-600 text-white p-2 text-center">
          <button 
            onClick={() => setAppMode('demo')}
            className="bg-indigo-700 hover:bg-indigo-800 px-4 py-1 rounded text-sm"
          >
            ← Back to Demo View
          </button>
          <span className="ml-4 text-sm">🏢 Insurance Company Portal - Admin Dashboard</span>
        </div>
        <InsurancePortal />
      </div>
    );
  }

  if (appMode === 'insurance') {
    return (
      <div>
        {/* Navigation Header */}
        <div className="bg-indigo-600 text-white p-3 flex justify-between items-center">
          <button 
            onClick={() => setAppMode('demo')}
            className="bg-indigo-700 hover:bg-indigo-800 px-4 py-2 rounded text-sm font-medium"
          >
            ← Back to Demo
          </button>
          <div className="text-center">
            <h1 className="text-xl font-bold">Insurance Intelligence Portal</h1>
            <p className="text-sm opacity-90">DriveWise AI Integration Dashboard</p>
          </div>
          <div className="text-right text-sm">
            <div>Live Demo</div>
            <div className="text-xs opacity-75">Hackathon 2025</div>
          </div>
        </div>
        <InsurancePortal />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold">🚗 DriveWise AI</h1>
            <div className="space-x-4">
              <button 
                onClick={() => setCurrentView('dashboard')}
                className={`px-3 py-2 rounded ${currentView === 'dashboard' ? 'bg-blue-500' : 'hover:bg-blue-500'}`}
              >
                Dashboard
              </button>
              <button 
                onClick={() => setCurrentView('chat')}
                className={`px-3 py-2 rounded ${currentView === 'chat' ? 'bg-blue-500' : 'hover:bg-blue-500'}`}
              >
                AI Chat
              </button>
              <button 
                onClick={toggleLiveMode}
                className={`px-4 py-2 rounded font-medium ${
                  isLiveMode 
                    ? 'bg-green-600 hover:bg-green-700 text-white' 
                    : 'bg-orange-600 hover:bg-orange-700 text-white'
                }`}
              >
                {isLiveMode ? '🟢 Live Data ON' : '🔴 Start Live Data'}
              </button>
              <button 
                onClick={() => setAppMode('insurance')}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded font-medium"
              >
                🏢 Insurance Portal
              </button>
              <span className="px-3 py-2">Reports</span>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="container mx-auto px-4 py-8">
        {currentView === 'chat' ? (
          <ChatDemo currentUserId={currentUserId} userData={userData} />
        ) : (
          <>
            <UserSelector 
              currentUserId={currentUserId} 
              onUserChange={setCurrentUserId} 
            />
            
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                DriveWise AI Dashboard
                {userData && (
                  <span className="block text-xl font-normal text-gray-600 mt-1">
                    Welcome back, {userData.name}
                  </span>
                )}
              </h1>
              <p className="text-gray-600">Your personalized driving insights and insurance risk analysis</p>
              
              {/* Live Data Status Indicator */}
              {isLiveMode && (
                <div className="mt-4 inline-flex items-center space-x-2 bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span>🚀 Live Data Streaming</span>
                  <span className="bg-green-200 px-2 py-1 rounded text-xs">
                    Updates: {liveDataCount}
                  </span>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className={`border-2 p-6 rounded-lg ${
                riskScore?.enhanced_risk_score < 0.2 
                  ? 'bg-green-50 border-green-200 text-green-800' 
                  : riskScore?.enhanced_risk_score < 0.3 
                  ? 'bg-yellow-50 border-yellow-200 text-yellow-800'
                  : 'bg-red-50 border-red-200 text-red-800'
              }`}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Enhanced Risk Score</h3>
                <p className="text-sm text-gray-600 mb-2">Includes NHTSA safety data</p>
                  <span className={
                    riskScore?.enhanced_risk_score < 0.2 ? 'text-green-600' :
                    riskScore?.enhanced_risk_score < 0.3 ? 'text-yellow-600' : 'text-red-600'
                  }>🛡️</span>
                </div>
                <div className="mb-2">
                  <span className={`text-3xl font-bold ${
                    riskScore?.enhanced_risk_score < 0.2 ? 'text-green-600' :
                    riskScore?.enhanced_risk_score < 0.3 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {riskScore ? Math.round(riskScore.enhanced_risk_score * 100) : '...'}<span className="text-lg font-normal">/100</span>
                  </span>
                </div>
                <p className="text-sm mb-4">Lower risk = Lower premiums</p>
                {riskScore && riskScore.safety_factors && (
                  <div className="text-xs space-y-1">
                    <div>Vehicle Safety: {riskScore.safety_factors.vehicle_safety_rating}⭐</div>
                    <div>Risk Reduction: {riskScore.risk_improvement}</div>
                  </div>
                )}
              </div>

              <div className="bg-blue-50 border-2 border-blue-200 text-blue-800 p-6 rounded-lg">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Safety Score</h3>
                  <span className="text-blue-600">📈</span>
                </div>
                <div className="mb-2">
                  <span className="text-3xl font-bold">
                    {safetyScore ? Math.round(safetyScore.overall_score) : '...'}<span className="text-lg font-normal">/100</span>
                  </span>
                </div>
                <p className="text-sm mb-4">Your driving safety rating</p>
                {safetyScore && (
                  <div className="text-xs space-y-1">
                    <div>Smooth Acceleration: {Math.round(safetyScore.safety_metrics.smooth_acceleration * 100)}%</div>
                    <div>Following Distance: {Math.round(safetyScore.safety_metrics.safe_following_distance * 100)}%</div>
                  </div>
                )}
              </div>

              <div className="bg-yellow-50 border-2 border-yellow-200 text-yellow-800 p-6 rounded-lg">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Profile Info</h3>
                  <span className="text-yellow-600">�</span>
                </div>
                <div className="mb-2">
                  <span className="text-lg font-bold">
                    {userData?.vehicle || 'Vehicle'}
                  </span>
                </div>
                <p className="text-sm mb-2">{userData?.location || 'Location'}</p>
                {userData && (
                  <div className="text-xs space-y-1">
                    <div>Age: {userData.age}</div>
                    <div>Experience: {userData.driving_experience} years</div>
                  </div>
                )}
              </div>
            </div>

            {/* NHTSA Vehicle Safety Section */}
            {vehicleSafety && (
              <div className="mb-8">
                <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-blue-800">🚗 Vehicle Safety Rating</h3>
                    <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                      NHTSA Certified
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-600 mb-1">
                        {vehicleSafety.nhtsa_data.overall_rating}⭐
                      </div>
                      <div className="text-sm text-blue-700">Overall Rating</div>
                    </div>
                    
                    <div className="text-center">
                      <div className={`text-2xl font-bold mb-1 ${
                        vehicleSafety.risk_impact.premium_adjustment < 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {vehicleSafety.risk_impact.premium_adjustment > 0 ? '+' : ''}{(vehicleSafety.risk_impact.premium_adjustment * 100).toFixed(0)}%
                      </div>
                      <div className="text-sm text-gray-600">Premium Impact</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600 mb-1">
                        {riskScore?.risk_improvement || 'N/A'}
                      </div>
                      <div className="text-sm text-purple-700">Risk Improvement</div>
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-lg p-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Detailed Safety Scores:</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>Rollover: {vehicleSafety.nhtsa_data.rollover_rating}⭐</div>
                      <div>Frontal Crash: {vehicleSafety.nhtsa_data.frontal_crash_rating}⭐</div>
                      <div>Side Crash: {vehicleSafety.nhtsa_data.side_crash_rating}⭐</div>
                      <div className="text-blue-600 font-medium">Data Source: {vehicleSafety.data_source}</div>
                    </div>
                  </div>
                  
                  <div className="mt-4 p-3 bg-green-100 rounded-lg">
                    <p className="text-green-800 text-sm font-medium">
                      💡 Your {vehicleSafety.nhtsa_data.overall_rating}-star safety rating reduces your insurance risk by {((riskScore?.base_risk_score - riskScore?.enhanced_risk_score) / riskScore?.base_risk_score * 100).toFixed(1)}%!
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Insurance Quote</h2>
                <div className="text-center">
                  {riskScore ? (() => {
                    const basePrice = 120;
                    const discountPercent = Math.round((0.3 - riskScore.enhanced_risk_score) * 83.33); // Higher discount for lower risk
                    const finalPrice = Math.round(basePrice * (1 - discountPercent / 100));
                    const savings = basePrice - finalPrice;
                    
                    return (
                      <>
                        <h3 className="text-2xl font-bold text-green-600 mb-2">${finalPrice}/month</h3>
                        <p className="text-gray-600 mb-4">Estimated Premium</p>
                        <div className="bg-green-50 p-4 rounded-lg">
                          <p className="text-green-800 font-medium">{discountPercent}% Discount Applied</p>
                          <p className="text-sm text-green-600">Based on your driving profile</p>
                          <p className="text-sm text-green-600">Annual Savings: ${savings * 12}</p>
                        </div>
                      </>
                    );
                  })() : (
                    <>
                      <h3 className="text-2xl font-bold text-gray-400 mb-2">Loading...</h3>
                      <p className="text-gray-600 mb-4">Calculating your premium</p>
                    </>
                  )}
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">AI Insights</h2>
                <div className="space-y-3">
                  {safetyScore?.improvement_suggestions?.map((suggestion, index) => (
                    <div key={index} className="bg-blue-50 p-3 rounded-lg">
                      <p className="text-blue-800 font-medium text-sm">💡 {suggestion}</p>
                    </div>
                  ))}
                  
                  {riskScore && (
                    <div className={`p-3 rounded-lg ${
                      riskScore.enhanced_risk_score < 0.2 
                        ? 'bg-green-50' 
                        : riskScore.enhanced_risk_score < 0.3 
                        ? 'bg-yellow-50' 
                        : 'bg-red-50'
                    }`}>
                      <p className={`font-medium text-sm ${
                        riskScore.enhanced_risk_score < 0.2 
                          ? 'text-green-800' 
                          : riskScore.enhanced_risk_score < 0.3 
                          ? 'text-yellow-800' 
                          : 'text-red-800'
                      }`}>
                        {riskScore.enhanced_risk_score < 0.2 
                          ? '🎉 Excellent driving + safe vehicle! Maximum discounts applied.' 
                          : riskScore.enhanced_risk_score < 0.3 
                          ? '⚠️ Good profile with NHTSA safety benefits included.' 
                          : '🚨 Consider both safer driving and vehicle safety features.'}
                      </p>
                    </div>
                  )}
                  
                  <button 
                    onClick={() => setCurrentView('chat')}
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Chat with AI Assistant →
                  </button>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;