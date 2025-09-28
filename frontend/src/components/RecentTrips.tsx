import React from 'react';

export const RecentTrips: React.FC<{ trips: any[] }> = ({ trips }) => {
  return (
    <div className="space-y-4">
      {trips.length === 0 ? (
        <p className="text-gray-500 text-center py-8">No recent trips</p>
      ) : (
        trips.map((trip, index) => (
          <div key={index} className="p-4 bg-gray-50 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium">Trip {index + 1}</span>
              <span className="text-sm text-gray-500">Today</span>
            </div>
            <p className="text-sm text-gray-600">Distance: 25km • Duration: 45min</p>
          </div>
        ))
      )}
    </div>
  );
};