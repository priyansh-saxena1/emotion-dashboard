// Backend configuration
export const BACKEND_URL = 'http://localhost:8000';

// API endpoints
export const API_ENDPOINTS = {
  LOGIN: `${BACKEND_URL}/api/login`,
  TOP_TRACKS: `${BACKEND_URL}/api/user/top-tracks`,
  ANALYZE: `${BACKEND_URL}/api/analyze`,
  RECOMMENDATIONS: `${BACKEND_URL}/api/recommendations`,
  HEALTH: `${BACKEND_URL}/api/health`,
} as const; 