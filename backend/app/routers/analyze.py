from fastapi import APIRouter, Request, HTTPException
from ..schemas import AnalyzeRequest, AnalyzeResponse
from ..auth import get_session_token
from ..spotify_client import spotify_client
from ..llm_service import llm_service
from ..cache import audio_features_cache, analysis_cache, get_audio_features_cache_key, get_analysis_cache_key, get_from_cache, set_in_cache
import hashlib
import json

router = APIRouter()

@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_tracks(payload: AnalyzeRequest, request: Request):
    """Analyze emotions for selected tracks"""
    try:
        access_token = get_session_token(request)
        
        # Check cache for analysis results
        features_hash = hashlib.md5(json.dumps(sorted(payload.track_ids)).encode()).hexdigest()
        cache_key = get_analysis_cache_key(payload.track_ids, features_hash)
        cached_result = get_from_cache(analysis_cache, cache_key)
        if cached_result:
            return AnalyzeResponse(**cached_result)
        
        # Get audio features (with caching)
        features_cache_key = get_audio_features_cache_key(payload.track_ids)
        cached_features = get_from_cache(audio_features_cache, features_cache_key)
        
        if cached_features:
            audio_features = cached_features
        else:
            audio_features = await spotify_client.get_audio_features(access_token, payload.track_ids)
            set_in_cache(audio_features_cache, features_cache_key, audio_features)
        
        # Prepare data for LLM analysis
        tracks_data = []
        for track_id in payload.track_ids:
            if track_id in audio_features:
                # For now, use generic track info since we don't have track names
                # In a full implementation, you could store track info in session or fetch it
                track_data = {
                    "id": track_id,
                    "title": f"Track {track_id[:8]}...",  # Use first 8 chars of ID
                    "artist": "Various Artists",
                    "features": audio_features[track_id]
                }
                tracks_data.append(track_data)
        
        if not tracks_data:
            raise HTTPException(status_code=400, detail="No valid tracks found for analysis")
        
        # Classify emotions
        heatmap = await llm_service.classify_emotions(tracks_data)
        
        # Generate explanations
        why = await llm_service.explain_emotions(tracks_data, heatmap)
        
        # Cache the results
        result = {
            "heatmap": {k: v.dict() for k, v in heatmap.items()},
            "why": why
        }
        set_in_cache(analysis_cache, cache_key, result)
        
        return AnalyzeResponse(heatmap=heatmap, why=why)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error analyzing tracks: {e}")
        raise HTTPException(status_code=502, detail="Failed to analyze tracks. Please try again.") 