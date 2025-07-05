from fastapi import APIRouter, Request, HTTPException
from ..schemas import TopTracksResponse
from ..auth import get_session_token
from ..spotify_client import spotify_client

router = APIRouter()

@router.get("/api/user/top-tracks", response_model=TopTracksResponse)
async def get_top_tracks(request: Request):
    """Get user's top tracks from Spotify"""
    print(f"🎵 [TOP-TRACKS] Request received from {request.client.host}")
    print(f"🎵 [TOP-TRACKS] Request headers: {dict(request.headers)}")
    print(f"🎵 [TOP-TRACKS] Request cookies: {request.cookies}")
    
    try:
        print(f"🔍 [TOP-TRACKS] Getting session token...")
        access_token = get_session_token(request)
        print(f"✅ [TOP-TRACKS] Got access token, fetching tracks...")
        
        tracks = await spotify_client.get_top_tracks(access_token)
        print(f"✅ [TOP-TRACKS] Successfully fetched {len(tracks)} tracks")
        
        return TopTracksResponse(tracks=tracks)
    except HTTPException as e:
        print(f"❌ [TOP-TRACKS] HTTP Exception: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        print(f"❌ [TOP-TRACKS] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch top tracks") 