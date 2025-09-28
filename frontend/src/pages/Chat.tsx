import React from 'react';

export const Chat: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">AI Driving Assistant</h1>
      <div className="bg-white rounded-lg shadow-md p-6 min-h-96">
        <div className="mb-4">
          <p className="bg-blue-50 p-4 rounded-lg">
            👋 Hi! I'm your DriveWise AI assistant. Ask me about your driving patterns, safety score, or insurance options!
          </p>
        </div>
        <div className="flex">
          <input 
            type="text" 
            placeholder="Ask me about your driving..." 
            className="flex-1 p-3 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button className="bg-blue-600 text-white px-6 py-3 rounded-r-lg hover:bg-blue-700">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};