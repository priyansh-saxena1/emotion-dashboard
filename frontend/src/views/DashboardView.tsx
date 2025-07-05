import React, { useEffect } from 'react';
import { useAppContext } from '../contexts/AppContext';
import { TrackGrid } from '../components/TrackGrid';
import { Heatmap } from '../components/Heatmap';
import { RecommendationList } from '../components/RecommendationList';
import { Music, AlertCircle, X } from 'lucide-react';

export function DashboardView() {
  const { state, dispatch } = useAppContext();

  useEffect(() => {
    // Fetch top tracks on component mount
    fetchTopTracks();
  }, []);

  const fetchTopTracks = async () => {
    console.log('🎵 [FRONTEND] Starting to fetch top tracks...');
    dispatch({ type: 'SET_LOADING', payload: { key: 'tracks', value: true } });
    
    try {
      const backendUrl = 'http://127.0.0.1:8000';
      console.log('🎵 [FRONTEND] Making request to backend:', `${backendUrl}/api/user/top-tracks`);
      console.log('🎵 [FRONTEND] Current cookies:', document.cookie);
      
      const response = await fetch(`${backendUrl}/api/user/top-tracks`, {
        credentials: 'include', // Important: include cookies
        headers: {
          'Accept': 'application/json',
        }
      });
      
      console.log('🎵 [FRONTEND] Response status:', response.status);
      console.log('🎵 [FRONTEND] Response headers:', Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('🎵 [FRONTEND] Error response:', errorText);
        throw new Error(`Failed to fetch top tracks: ${response.status} ${errorText}`);
      }
      
      const data = await response.json();
      console.log('🎵 [FRONTEND] Successfully fetched tracks:', data);
      dispatch({ type: 'SET_TOP_TRACKS', payload: data.tracks });
    } catch (error) {
      console.error('🎵 [FRONTEND] Error fetching top tracks:', error);
      dispatch({ type: 'SET_ERROR', payload: `Failed to load your top tracks: ${error.message}` });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: { key: 'tracks', value: false } });
    }
  };

  const handleAnalyze = async () => {
    const selectedTrackIds = Array.from(state.selectedIds);
    
    if (selectedTrackIds.length === 0) {
      dispatch({ type: 'SET_ERROR', payload: 'Please select at least one track to analyze.' });
      return;
    }

    dispatch({ type: 'SET_LOADING', payload: { key: 'analysis', value: true } });
    
    try {
      const backendUrl = 'http://127.0.0.1:8000';
      const response = await fetch(`${backendUrl}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ track_ids: selectedTrackIds }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to analyze tracks');
      }
      
      const data = await response.json();
      dispatch({ type: 'SET_ANALYSIS_RESULT', payload: data });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: 'Failed to analyze your tracks. Please try again.' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: { key: 'analysis', value: false } });
    }
  };

  const dismissError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <div className="inline-flex items-center justify-center w-10 h-10 bg-gradient-to-r from-green-400 to-blue-500 rounded-full">
              <Music size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Emotional Soundscape</h1>
              <p className="text-sm text-gray-600">Discover the emotions in your music</p>
            </div>
          </div>
        </div>
      </div>

      {/* Error Banner */}
      {state.error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mx-4 mt-4 rounded-r-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <AlertCircle size={20} className="text-red-400" />
              <p className="text-red-800">{state.error}</p>
            </div>
            <button
              onClick={dismissError}
              className="text-red-400 hover:text-red-600 transition-colors"
            >
              <X size={20} />
            </button>
          </div>
        </div>
      )}

      {/* Loading Overlay */}
      {state.loading.analysis && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent mx-auto mb-4"></div>
            <p className="text-gray-700">Analyzing your emotional soundscape...</p>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Top Tracks Section */}
        <div className="bg-white rounded-lg shadow-lg mb-6">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold text-gray-900">Your Top Tracks</h2>
            <p className="text-gray-600 mt-1">Select the tracks you'd like to analyze</p>
          </div>
          
          <TrackGrid />
          
          <div className="p-6 border-t">
            <button
              onClick={handleAnalyze}
              disabled={state.loading.analysis || state.selectedIds.size === 0}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
            >
              {state.loading.analysis ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                  <span>Analyzing...</span>
                </div>
              ) : (
                `Analyze My Emotional Soundscape (${state.selectedIds.size} tracks)`
              )}
            </button>
          </div>
        </div>

        {/* Heatmap Section */}
        <Heatmap />

        {/* Recommendations Section */}
        {state.analysisResult && <RecommendationList />}
      </div>
    </div>
  );
}