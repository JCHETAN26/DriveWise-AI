import React from 'react';

interface NavbarProps {}

export const Navbar: React.FC<NavbarProps> = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold">🚗 DriveWise AI</h1>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <a href="/dashboard" className="hover:text-blue-200 px-3 py-2 rounded">Dashboard</a>
            <a href="/chat" className="hover:text-blue-200 px-3 py-2 rounded">AI Chat</a>
            <a href="/reports" className="hover:text-blue-200 px-3 py-2 rounded">Reports</a>
            <a href="/profile" className="hover:text-blue-200 px-3 py-2 rounded">Profile</a>
          </div>
        </div>
      </div>
    </nav>
  );
};