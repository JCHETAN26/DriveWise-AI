import React from 'react';

export const InsuranceQuote: React.FC<{ quote: any }> = ({ quote }) => {
  return (
    <div className="text-center">
      <h3 className="text-2xl font-bold text-green-600 mb-2">$85/month</h3>
      <p className="text-gray-600 mb-4">Estimated Premium</p>
      <div className="bg-green-50 p-4 rounded-lg">
        <p className="text-green-800 font-medium">15% Discount Applied</p>
        <p className="text-sm text-green-600">Based on your safe driving</p>
      </div>
    </div>
  );
};