import React from 'react';

export const TrendChart: React.FC<{ data: any[] }> = ({ data }) => {
  return (
    <div className="h-64 flex items-center justify-center bg-gray-50 rounded">
      <p className="text-gray-500">📈 Trend Chart Component</p>
    </div>
  );
};