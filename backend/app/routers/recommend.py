from fastapi import APIRouter, Request, HTTPException, Query
from ..schemas import RecommendationsResponse, EmotionEnum
from ..auth import get_session_token
from ..spotify_client import spotify_client

router = APIRouter()

@router.get("/api/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(emotion: EmotionEnum = Query(...), request: Request = None):
    """Get track recommendations based on emotion"""
    try:
        access_token = get_session_token(request)
        
        # For now, we'll use some default seed tracks
        # In a more sophisticated implementation, you could:
        # 1. Store the user's analyzed tracks in session
        # 2. Select tracks with highest scores for the target emotion
        # 3. Use those as seed tracks for recommendations
        
        # Default seed tracks for each emotion (popular tracks)
        default_seeds = {
            "joy": ["4iJyoBOLtHqaGxP12qzhQI", "09R8_2nJt739X8nJKy8ILK", "3n3Ppam7vgaVa1iaRUc9Lp"],
            "sadness": ["1lDWb6b6ieDQ2xT7ewTC3G", "5Z01UMMf7V1o0MzF86TqQL", "4h9wh7iOZ0GGn8QVp3RAVH"],
            "calm": ["5Z01UMMf7V1o0MzF86TqQL", "4h9wh7iOZ0GGn8QVp3RAVH", "1lDWb6b6ieDQ2xT7ewTC3G"],
            "excitement": ["3n3Ppam7vgaVa1iaRUc9Lp", "09R8_2nJt739X8nJKy8ILK", "4iJyoBOLtHqaGxP12qzhQI"],
            "anger": ["3n3Ppam7vgaVa1iaRUc9Lp", "09R8_2nJt739X8nJKy8ILK", "4iJyoBOLtHqaGxP12qzhQI"]
        }
        
        seed_tracks = default_seeds.get(emotion.value, default_seeds["joy"])
        
        recommendations = await spotify_client.get_recommendations(
            access_token, 
            seed_tracks, 
            emotion.value
        )
        
        return RecommendationsResponse(recommendations=recommendations)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations") 