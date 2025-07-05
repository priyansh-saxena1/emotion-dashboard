from fastapi import APIRouter, Request, HTTPException
from ..schemas import TopTracksResponse
from ..auth import get_session_token
from ..spotify_client import spotify_client

router = APIRouter()

@router.get("/api/user/top-tracks", response_model=TopTracksResponse)
async def get_top_tracks(request: Request):
    """Get user's top tracks from Spotify"""
    try:
        access_token = get_session_token(request)
        tracks = await spotify_client.get_top_tracks(access_token)
        return TopTracksResponse(tracks=tracks)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch top tracks") 