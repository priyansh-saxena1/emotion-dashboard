import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface Track {
  id: string;
  title: string;
  artist: string;
  cover_url: string;
}

interface EmotionScores {
  joy: number;
  sadness: number;
  calm: number;
  excitement: number;
  anger: number;
}

interface AnalysisResult {
  heatmap: Record<string, EmotionScores>;
  why: Record<string, string>;
}

interface AppState {
  user: { isLoggedIn: boolean };
  topTracks: Track[];
  selectedIds: Set<string>;
  analysisResult: AnalysisResult | null;
  recommendations: Track[];
  loading: {
    tracks: boolean;
    analysis: boolean;
    recommendations: boolean;
  };
  error: string | null;
}

type AppAction =
  | { type: 'SET_USER'; payload: { isLoggedIn: boolean } }
  | { type: 'SET_TOP_TRACKS'; payload: Track[] }
  | { type: 'TOGGLE_TRACK_SELECTION'; payload: string }
  | { type: 'SET_ANALYSIS_RESULT'; payload: AnalysisResult }
  | { type: 'SET_RECOMMENDATIONS'; payload: Track[] }
  | { type: 'SET_LOADING'; payload: { key: keyof AppState['loading']; value: boolean } }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_ERROR' };

const initialState: AppState = {
  user: { isLoggedIn: false },
  topTracks: [],
  selectedIds: new Set(),
  analysisResult: null,
  recommendations: [],
  loading: {
    tracks: false,
    analysis: false,
    recommendations: false,
  },
  error: null,
};

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_TOP_TRACKS':
      return { 
        ...state, 
        topTracks: action.payload,
        selectedIds: new Set(action.payload.map(track => track.id))
      };
    case 'TOGGLE_TRACK_SELECTION':
      const newSelectedIds = new Set(state.selectedIds);
      if (newSelectedIds.has(action.payload)) {
        newSelectedIds.delete(action.payload);
      } else {
        newSelectedIds.add(action.payload);
      }
      return { ...state, selectedIds: newSelectedIds };
    case 'SET_ANALYSIS_RESULT':
      return { ...state, analysisResult: action.payload };
    case 'SET_RECOMMENDATIONS':
      return { ...state, recommendations: action.payload };
    case 'SET_LOADING':
      return { 
        ...state, 
        loading: { ...state.loading, [action.payload.key]: action.payload.value }
      };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    default:
      return state;
  }
}

const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}