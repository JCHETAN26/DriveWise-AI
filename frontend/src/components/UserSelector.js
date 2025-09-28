import React, { useState, useEffect } from 'react';

export const UserSelector = ({ currentUserId, onUserChange }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('http://localhost:8005/api/v1/users');
        const data = await response.json();
        setUsers(data.users || []);
      } catch (error) {
        console.error('Error fetching users:', error);
        // Fallback to default users if API fails
        setUsers([
          { user_id: 'user123', name: 'Sarah Chen', profile_type: 'safe_driver', location: 'San Francisco, CA' },
          { user_id: 'user456', name: 'Mike Rodriguez', profile_type: 'average_driver', location: 'Austin, TX' },
          { user_id: 'user789', name: 'Emma Johnson', profile_type: 'tech_savvy_driver', location: 'Seattle, WA' },
          { user_id: 'user101', name: 'David Kim', profile_type: 'experienced_driver', location: 'New York, NY' },
          { user_id: 'user202', name: 'Lisa Thompson', profile_type: 'family_driver', location: 'Denver, CO' }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const getProfileBadgeColor = (profileType) => {
    const colors = {
      'safe_driver': 'bg-green-100 text-green-800',
      'average_driver': 'bg-yellow-100 text-yellow-800',
      'tech_savvy_driver': 'bg-blue-100 text-blue-800',
      'experienced_driver': 'bg-purple-100 text-purple-800',
      'family_driver': 'bg-pink-100 text-pink-800'
    };
    return colors[profileType] || 'bg-gray-100 text-gray-800';
  };

  const getProfileLabel = (profileType) => {
    const labels = {
      'safe_driver': 'Safe Driver',
      'average_driver': 'Average Driver',
      'tech_savvy_driver': 'Tech Savvy',
      'experienced_driver': 'Experienced',
      'family_driver': 'Family Driver'
    };
    return labels[profileType] || 'Driver';
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-3"></div>
          <div className="h-10 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-3">
        🎭 Demo User Profiles
      </h3>
      <div className="space-y-2">
        {users.map((user) => (
          <button
            key={user.user_id}
            onClick={() => onUserChange(user.user_id)}
            className={`w-full text-left p-3 rounded-lg border-2 transition-all duration-200 ${
              currentUserId === user.user_id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">{user.name}</div>
                <div className="text-sm text-gray-600">{user.location}</div>
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getProfileBadgeColor(user.profile_type)}`}>
                {getProfileLabel(user.profile_type)}
              </span>
            </div>
          </button>
        ))}
      </div>
      <div className="mt-3 text-xs text-gray-500">
        💡 Click different users to see how their profiles affect risk scores and insurance quotes
      </div>
    </div>
  );
};