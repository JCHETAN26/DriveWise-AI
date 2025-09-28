import React from 'react';

export const TrafficMap: React.FC<{ hotspots: any[] }> = ({ hotspots }) => {
  return (
    <div className="h-64 flex items-center justify-center bg-gray-50 rounded">
      <p className="text-gray-500">🗺️ Traffic Map Component</p>
    </div>
  );
};