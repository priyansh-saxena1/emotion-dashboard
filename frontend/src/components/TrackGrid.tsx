import React from 'react';
import { useAppContext } from '../contexts/AppContext';
import { Check } from 'lucide-react';

export function TrackGrid() {
  const { state, dispatch } = useAppContext();

  const handleToggleSelection = (trackId: string) => {
    dispatch({ type: 'TOGGLE_TRACK_SELECTION', payload: trackId });
  };

  if (state.loading.tracks) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-4">
      {state.topTracks.map((track) => (
        <div
          key={track.id}
          className="relative group cursor-pointer transform transition-all duration-200 hover:scale-105"
          onClick={() => handleToggleSelection(track.id)}
        >
          <div className="relative aspect-square rounded-lg overflow-hidden shadow-md">
            <img
              src={track.cover_url}
              alt={`${track.title} by ${track.artist}`}
              className="w-full h-full object-cover transition-opacity duration-200 group-hover:opacity-80"
            />
            <div className={`absolute inset-0 bg-black bg-opacity-40 transition-opacity duration-200 ${
              state.selectedIds.has(track.id) ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'
            }`}>
              <div className="absolute top-2 right-2">
                <div className={`w-6 h-6 rounded-full border-2 border-white flex items-center justify-center transition-colors duration-200 ${
                  state.selectedIds.has(track.id) ? 'bg-green-500' : 'bg-transparent'
                }`}>
                  {state.selectedIds.has(track.id) && <Check size={16} className="text-white" />}
                </div>
              </div>
            </div>
          </div>
          <div className="mt-2 text-sm">
            <p className="font-medium text-gray-900 truncate">{track.title}</p>
            <p className="text-gray-600 truncate">{track.artist}</p>
          </div>
        </div>
      ))}
    </div>
  );
}