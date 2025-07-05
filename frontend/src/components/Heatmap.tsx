import React, { useState } from 'react';
import { useAppContext } from '../contexts/AppContext';
import { ChevronDown, ChevronUp } from 'lucide-react';

const emotions = ['joy', 'sadness', 'calm', 'excitement', 'anger'] as const;
const emotionColors = {
  joy: 'bg-yellow-500',
  sadness: 'bg-blue-500',
  calm: 'bg-green-500',
  excitement: 'bg-red-500',
  anger: 'bg-purple-500',
};

export function Heatmap() {
  const { state } = useAppContext();
  const [expandedTracks, setExpandedTracks] = useState<Set<string>>(new Set());
  const [hoveredCell, setHoveredCell] = useState<{trackId: string, emotion: string, score: number} | null>(null);

  if (!state.analysisResult) return null;

  const selectedTracks = state.topTracks.filter(track => 
    state.selectedIds.has(track.id) && state.analysisResult?.heatmap[track.id]
  );

  const toggleExpanded = (trackId: string) => {
    const newExpanded = new Set(expandedTracks);
    if (newExpanded.has(trackId)) {
      newExpanded.delete(trackId);
    } else {
      newExpanded.add(trackId);
    }
    setExpandedTracks(newExpanded);
  };

  const getDominantEmotion = (scores: Record<string, number>) => {
    return Object.entries(scores).reduce((a, b) => a[1] > b[1] ? a : b)[0];
  };

  const getIntensityClass = (score: number) => {
    if (score >= 0.8) return 'opacity-100';
    if (score >= 0.6) return 'opacity-80';
    if (score >= 0.4) return 'opacity-60';
    if (score >= 0.2) return 'opacity-40';
    return 'opacity-20';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Emotional Soundscape</h2>
      
      <div className="overflow-x-auto">
        <div className="min-w-full">
          {/* Header */}
          <div className="grid grid-cols-6 gap-2 mb-4">
            <div className="font-semibold text-gray-900">Track</div>
            {emotions.map(emotion => (
              <div key={emotion} className="font-semibold text-gray-900 text-center capitalize">
                {emotion}
              </div>
            ))}
          </div>

          {/* Heatmap rows */}
          {selectedTracks.map(track => {
            const scores = state.analysisResult!.heatmap[track.id];
            const dominantEmotion = getDominantEmotion(scores);
            const isExpanded = expandedTracks.has(track.id);

            return (
              <div key={track.id} className="mb-4 border rounded-lg p-4 bg-gray-50">
                <div className="grid grid-cols-6 gap-2 items-center">
                  <div className="font-medium text-gray-900">
                    <div className="text-sm">{track.title}</div>
                    <div className="text-xs text-gray-600">{track.artist}</div>
                  </div>
                  {emotions.map(emotion => (
                    <div
                      key={emotion}
                      className="relative"
                      onMouseEnter={() => setHoveredCell({trackId: track.id, emotion, score: scores[emotion]})}
                      onMouseLeave={() => setHoveredCell(null)}
                    >
                      <div className={`h-12 rounded ${emotionColors[emotion]} ${getIntensityClass(scores[emotion])} border-2 border-gray-200`}></div>
                      {hoveredCell?.trackId === track.id && hoveredCell?.emotion === emotion && (
                        <div className="absolute z-10 bg-black text-white text-xs rounded px-2 py-1 -top-8 left-1/2 transform -translate-x-1/2">
                          {(scores[emotion] * 100).toFixed(1)}%
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                
                {/* Rationale toggle */}
                <div className="mt-3">
                  <button
                    onClick={() => toggleExpanded(track.id)}
                    className="flex items-center space-x-2 text-sm text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    <span>Why this feels {dominantEmotion}</span>
                  </button>
                  
                  {isExpanded && (
                    <div className="mt-2 p-3 bg-white rounded border text-sm text-gray-700">
                      {state.analysisResult.why[track.id]}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}