import { useState } from 'react';

export const useAuth = () => {
  // Mock authentication - in real app, connect to backend
  const [user] = useState({
    id: 'user123',
    email: 'demo@drivewise.ai',
    name: 'Demo User'
  });
  
  const [loading] = useState(false);

  return {
    user,
    loading,
    login: async (email: string, password: string) => {
      // Mock login
      return { success: true };
    },
    logout: () => {
      // Mock logout
    }
  };
};