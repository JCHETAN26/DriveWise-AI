import React from 'react';

export const Reports: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Driving Reports</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Weekly Summary</h2>
          <p className="text-gray-600">Your driving performance this week</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Monthly Trends</h2>
          <p className="text-gray-600">Long-term driving behavior analysis</p>
        </div>
      </div>
    </div>
  );
};