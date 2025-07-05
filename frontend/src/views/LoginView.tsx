import React from 'react';
import { Music } from 'lucide-react';

export function LoginView() {
  const handleLogin = () => {
    console.log('🔐 [LOGIN] User clicked login button');
    console.log('🔐 [LOGIN] Redirecting to /api/login');
    window.location.href = '/api/login';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-pink-500 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full text-center">
        <div className="mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-400 to-blue-500 rounded-full mb-4">
            <Music size={32} className="text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Emotional Soundscape
          </h1>
          <p className="text-gray-600">
            Discover the emotions hidden in your music taste
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <div className="flex items-center space-x-3 text-sm text-gray-600">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span>Analyze your top tracks</span>
          </div>
          <div className="flex items-center space-x-3 text-sm text-gray-600">
            <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
            <span>Visualize emotional patterns</span>
          </div>
          <div className="flex items-center space-x-3 text-sm text-gray-600">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
            <span>Get personalized recommendations</span>
          </div>
        </div>

        <button
          onClick={handleLogin}
          className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white font-medium py-3 px-6 rounded-full hover:from-green-600 hover:to-green-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
        >
          Log in with Spotify
        </button>

        <p className="text-xs text-gray-500 mt-4">
          We'll never share your data or modify your playlists
        </p>
      </div>
    </div>
  );
}