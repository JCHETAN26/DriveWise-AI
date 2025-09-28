import React, { useState, useEffect } from 'react';

export const InsurancePortal = () => {
  const [currentView, setCurrentView] = useState('overview');
  const [customerData, setCustomerData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock insurance company data
  useEffect(() => {
    const mockInsuranceData = {
      company: "SafeGuard Insurance Co.",
      totalCustomers: 2847,
      monthlyPremiums: 421850,
      claimsRatio: 0.68,
      customers: [
        {
          id: "user123",
          name: "Sarah Chen",
          vehicle: "2020 Honda Civic",
          location: "San Francisco, CA",
          riskScore: 0.15,
          safetyScore: 92,
          monthsTracked: 8,
          currentPremium: 67,
          standardPremium: 120,
          discount: 44,
          claims: 0,
          totalTrips: 324,
          riskTier: "excellent",
          lastUpdate: "2025-09-27"
        },
        {
          id: "user456", 
          name: "Mike Rodriguez",
          vehicle: "2018 Ford F-150",
          location: "Austin, TX",
          riskScore: 0.35,
          safetyScore: 74,
          monthsTracked: 6,
          currentPremium: 156,
          standardPremium: 120,
          surcharge: 30,
          claims: 1,
          totalTrips: 189,
          riskTier: "high_risk",
          lastUpdate: "2025-09-26"
        },
        {
          id: "user789",
          name: "Emma Johnson", 
          vehicle: "2022 Tesla Model 3",
          location: "Seattle, WA",
          riskScore: 0.22,
          safetyScore: 86,
          monthsTracked: 12,
          currentPremium: 95,
          standardPremium: 120,
          discount: 21,
          claims: 0,
          totalTrips: 456,
          riskTier: "good",
          lastUpdate: "2025-09-27"
        },
        {
          id: "user101",
          name: "David Kim",
          vehicle: "2019 BMW 330i", 
          location: "New York, NY",
          riskScore: 0.28,
          safetyScore: 81,
          monthsTracked: 10,
          currentPremium: 108,
          standardPremium: 120,
          discount: 10,
          claims: 0,
          totalTrips: 378,
          riskTier: "average",
          lastUpdate: "2025-09-27"
        },
        {
          id: "user202",
          name: "Lisa Thompson",
          vehicle: "2021 Subaru Outback",
          location: "Denver, CO", 
          riskScore: 0.25,
          safetyScore: 83,
          monthsTracked: 7,
          currentPremium: 102,
          standardPremium: 120,
          discount: 15,
          claims: 0,
          totalTrips: 267,
          riskTier: "good",
          lastUpdate: "2025-09-26"
        }
      ]
    };
    
    setCustomerData(mockInsuranceData);
    setLoading(false);
  }, []);

  const getRiskColor = (tier) => {
    const colors = {
      'excellent': 'text-green-600 bg-green-50',
      'good': 'text-blue-600 bg-blue-50', 
      'average': 'text-yellow-600 bg-yellow-50',
      'high_risk': 'text-red-600 bg-red-50'
    };
    return colors[tier] || 'text-gray-600 bg-gray-50';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading insurance dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Insurance Company Navigation */}
      <nav className="bg-indigo-700 text-white shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold">🏢 {customerData.company}</h1>
              <span className="text-indigo-200 text-sm">Insurance Management Portal</span>
            </div>
            <div className="space-x-4">
              <button 
                onClick={() => setCurrentView('overview')}
                className={`px-3 py-2 rounded transition-colors ${currentView === 'overview' ? 'bg-indigo-600' : 'hover:bg-indigo-600'}`}
              >
                Portfolio Overview
              </button>
              <button 
                onClick={() => setCurrentView('customers')}
                className={`px-3 py-2 rounded transition-colors ${currentView === 'customers' ? 'bg-indigo-600' : 'hover:bg-indigo-600'}`}
              >
                Customer Management
              </button>
              <button 
                onClick={() => setCurrentView('pricing')}
                className={`px-3 py-2 rounded transition-colors ${currentView === 'pricing' ? 'bg-indigo-600' : 'hover:bg-indigo-600'}`}
              >
                Pricing Engine
              </button>
              <button 
                onClick={() => setCurrentView('analytics')}
                className={`px-3 py-2 rounded transition-colors ${currentView === 'analytics' ? 'bg-indigo-600' : 'hover:bg-indigo-600'}`}
              >
                Risk Analytics
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8">
        {currentView === 'overview' && (
          <>
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Portfolio Performance Dashboard</h1>
              <p className="text-gray-600">Real-time insights into your DriveWise AI insurance portfolio</p>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Total Customers</h3>
                  <span className="text-blue-600">👥</span>
                </div>
                <div className="text-3xl font-bold text-blue-600">{customerData.totalCustomers.toLocaleString()}</div>
                <p className="text-sm text-green-600 mt-2">+12% vs traditional portfolio</p>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Monthly Premiums</h3>
                  <span className="text-green-600">💰</span>
                </div>
                <div className="text-3xl font-bold text-green-600">${customerData.monthlyPremiums.toLocaleString()}</div>
                <p className="text-sm text-green-600 mt-2">+8% revenue growth</p>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Claims Ratio</h3>
                  <span className="text-yellow-600">📊</span>
                </div>
                <div className="text-3xl font-bold text-yellow-600">{Math.round(customerData.claimsRatio * 100)}%</div>
                <p className="text-sm text-green-600 mt-2">-22% vs industry average</p>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Profit Margin</h3>
                  <span className="text-purple-600">📈</span>
                </div>
                <div className="text-3xl font-bold text-purple-600">24%</div>
                <p className="text-sm text-green-600 mt-2">+12% vs traditional</p>
              </div>
            </div>

            {/* Risk Distribution */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Risk Distribution</h2>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-green-600">Excellent Drivers</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-green-600 h-2 rounded-full" style={{width: '20%'}}></div>
                      </div>
                      <span className="text-sm font-medium">20%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-blue-600">Good Drivers</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{width: '40%'}}></div>
                      </div>
                      <span className="text-sm font-medium">40%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-yellow-600">Average Drivers</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-600 h-2 rounded-full" style={{width: '25%'}}></div>
                      </div>
                      <span className="text-sm font-medium">25%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-red-600">High Risk Drivers</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-red-600 h-2 rounded-full" style={{width: '15%'}}></div>
                      </div>
                      <span className="text-sm font-medium">15%</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Monthly Trends</h2>
                <div className="space-y-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-medium text-green-800">Premium Revenue</h4>
                    <p className="text-2xl font-bold text-green-600">$421,850</p>
                    <p className="text-sm text-green-600">+8.2% from last month</p>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium text-blue-800">New Customers</h4>
                    <p className="text-2xl font-bold text-blue-600">347</p>
                    <p className="text-sm text-blue-600">+15.3% from last month</p>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <h4 className="font-medium text-yellow-800">Claims Filed</h4>
                    <p className="text-2xl font-bold text-yellow-600">47</p>
                    <p className="text-sm text-green-600">-23.1% from last month</p>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {currentView === 'customers' && (
          <>
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Customer Management</h1>
              <p className="text-gray-600">Monitor and manage individual customer risk profiles</p>
            </div>

            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="px-6 py-4 bg-gray-50 border-b">
                <h2 className="text-lg font-semibold text-gray-900">Customer Portfolio</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk Tier</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Premium</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Discount/Surcharge</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Claims</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data Quality</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {customerData.customers && customerData.customers.map((customer) => (
                      <tr key={customer.id}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div>
                            <div className="text-sm font-medium text-gray-900">{customer.name}</div>
                            <div className="text-sm text-gray-500">{customer.vehicle}</div>
                            <div className="text-sm text-gray-500">{customer.location}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRiskColor(customer.riskTier)}`}>
                            {customer.riskTier.replace('_', ' ').toUpperCase()}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">${customer.currentPremium}/month</div>
                          <div className="text-sm text-gray-500">Was: ${customer.standardPremium}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {customer.discount ? (
                            <span className="text-green-600 font-medium">-{customer.discount}%</span>
                          ) : (
                            <span className="text-red-600 font-medium">+{customer.surcharge}%</span>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`font-medium ${customer.claims === 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {customer.claims}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">{customer.monthsTracked} months</div>
                          <div className="text-sm text-gray-500">{customer.totalTrips} trips</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-indigo-600 hover:text-indigo-900 mr-3">View Details</button>
                          <button className="text-gray-600 hover:text-gray-900">Adjust Rate</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {currentView === 'pricing' && (
          <>
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Pricing Engine</h1>
              <p className="text-gray-600">Configure risk-based pricing algorithms and discount structures</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Pricing Algorithm Settings</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Base Premium (Monthly)</label>
                    <input type="number" value="120" className="w-full p-3 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Maximum Discount (%)</label>
                    <input type="number" value="45" className="w-full p-3 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Maximum Surcharge (%)</label>
                    <input type="number" value="50" className="w-full p-3 border rounded-lg" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Minimum Data Period (months)</label>
                    <input type="number" value="6" className="w-full p-3 border rounded-lg" />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Risk Factor Weights</h2>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Speeding Events</span>
                    <div className="flex items-center space-x-2">
                      <input type="range" min="0" max="50" value="30" className="w-24" />
                      <span className="text-sm font-medium w-12">30%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Hard Braking</span>
                    <div className="flex items-center space-x-2">
                      <input type="range" min="0" max="50" value="25" className="w-24" />
                      <span className="text-sm font-medium w-12">25%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Phone Usage</span>
                    <div className="flex items-center space-x-2">
                      <input type="range" min="0" max="50" value="15" className="w-24" />
                      <span className="text-sm font-medium w-12">15%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Night Driving</span>
                    <div className="flex items-center space-x-2">
                      <input type="range" min="0" max="50" value="10" className="w-24" />
                      <span className="text-sm font-medium w-12">10%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Mileage</span>
                    <div className="flex items-center space-x-2">
                      <input type="range" min="0" max="50" value="10" className="w-24" />
                      <span className="text-sm font-medium w-12">10%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Weather Conditions</span>
                    <div className="flex items-center space-x-2">
                      <input type="range" min="0" max="50" value="10" className="w-24" />
                      <span className="text-sm font-medium w-12">10%</span>
                    </div>
                  </div>
                </div>
                <button className="w-full mt-6 bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700">
                  Update Pricing Model
                </button>
              </div>
            </div>
          </>
        )}

        {currentView === 'analytics' && (
          <>
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Risk Analytics Dashboard</h1>
              <p className="text-gray-600">Deep dive into risk patterns and predictive insights</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Predictive Risk Alerts</h3>
                <div className="space-y-3">
                  <div className="bg-red-50 border-l-4 border-red-400 p-3">
                    <p className="text-red-800 font-medium text-sm">High Risk Pattern Detected</p>
                    <p className="text-red-700 text-sm">Mike Rodriguez: +40% hard braking last week</p>
                  </div>
                  <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3">
                    <p className="text-yellow-800 font-medium text-sm">Improvement Opportunity</p>
                    <p className="text-yellow-700 text-sm">15 customers eligible for discount upgrades</p>
                  </div>
                  <div className="bg-green-50 border-l-4 border-green-400 p-3">
                    <p className="text-green-800 font-medium text-sm">Retention Success</p>
                    <p className="text-green-700 text-sm">Sarah Chen: 8 months claim-free driving</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Geographic Risk Heatmap</h3>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm">San Francisco, CA</span>
                      <span className="text-sm font-medium text-red-600">High</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-red-600 h-2 rounded-full" style={{width: '85%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm">Austin, TX</span>
                      <span className="text-sm font-medium text-yellow-600">Medium</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-yellow-600 h-2 rounded-full" style={{width: '60%'}}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm">Denver, CO</span>
                      <span className="text-sm font-medium text-green-600">Low</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-green-600 h-2 rounded-full" style={{width: '35%'}}></div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Model Performance</h3>
                <div className="space-y-4">
                  <div>
                    <div className="text-sm text-gray-600">Prediction Accuracy</div>
                    <div className="text-2xl font-bold text-green-600">94.2%</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">False Positive Rate</div>
                    <div className="text-2xl font-bold text-blue-600">3.1%</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Model Confidence</div>
                    <div className="text-2xl font-bold text-purple-600">91.7%</div>
                  </div>
                  <button className="w-full bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700 text-sm">
                    Retrain Model
                  </button>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
};