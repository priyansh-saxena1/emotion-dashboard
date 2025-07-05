import React, { useState } from 'react';
import { useAppContext } from '../contexts/AppContext';
import { Music } from 'lucide-react';

const emotions = ['joy', 'sadness', 'calm', 'excitement', 'anger'];

export function RecommendationList() {
  const { state, dispatch } = useAppContext();
  const [selectedEmotion, setSelectedEmotion] = useState<string>('joy');

  const handleGetRecommendations = async () => {
    dispatch({ type: 'SET_LOADING', payload: { key: 'recommendations', value: true } });
    
    try {
      const response = await fetch(`/api/recommendations?emotion=${selectedEmotion}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }
      
      const data = await response.json();
      dispatch({ type: 'SET_RECOMMENDATIONS', payload: data.recommendations });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: 'Failed to fetch recommendations. Please try again.' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: { key: 'recommendations', value: false } });
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Discover More Music</h2>
      
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <select
          value={selectedEmotion}
          onChange={(e) => setSelectedEmotion(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {emotions.map(emotion => (
            <option key={emotion} value={emotion} className="capitalize">
              {emotion}
            </option>
          ))}
        </select>
        
        <button
          onClick={handleGetRecommendations}
          disabled={state.loading.recommendations}
          className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
          {state.loading.recommendations ? (
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
              <span>Loading...</span>
            </div>
          ) : (
            'Suggest Me More'
          )}
        </button>
      </div>

      {state.recommendations.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {state.recommendations.map((track) => (
            <div key={track.id} className="group">
              <div className="aspect-square rounded-lg overflow-hidden shadow-md mb-2 transform transition-transform duration-200 group-hover:scale-105">
                <img
                  src={track.cover_url}
                  alt={`${track.title} by ${track.artist}`}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="text-sm">
                <p className="font-medium text-gray-900 truncate">{track.title}</p>
                <p className="text-gray-600 truncate">{track.artist}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {state.recommendations.length === 0 && !state.loading.recommendations && (
        <div className="text-center py-12 text-gray-500">
          <Music size={48} className="mx-auto mb-4 opacity-50" />
          <p>Select an emotion and click "Suggest Me More" to discover new music!</p>
        </div>
      )}
    </div>
  );
}