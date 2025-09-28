import React from 'react';

export const Profile: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">User Profile</h1>
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center space-x-4 mb-6">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-xl font-bold">
            DU
          </div>
          <div>
            <h2 className="text-xl font-semibold">Demo User</h2>
            <p className="text-gray-600">demo@drivewise.ai</p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold mb-2">Vehicle Information</h3>
            <p className="text-gray-600">2020 Honda Civic</p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Driving Experience</h3>
            <p className="text-gray-600">8 years</p>
          </div>
        </div>
      </div>
    </div>
  );
};