import httpx
from typing import List, Dict, Optional
from .schemas import Track, AudioFeatures
from .config import settings
import asyncio

class SpotifyClient:
    def __init__(self):
        self.base_url = "https://api.spotify.com/v1"
        self.auth_url = "https://accounts.spotify.com/api/token"
    
    async def exchange_code_for_tokens(self, code: str) -> Dict[str, str]:
        """Exchange authorization code for access and refresh tokens"""
        async with httpx.AsyncClient() as client:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
                "client_id": settings.SPOTIFY_CLIENT_ID,
                "client_secret": settings.SPOTIFY_CLIENT_SECRET,
            }
            
            response = await client.post(self.auth_url, data=data)
            response.raise_for_status()
            return response.json()
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """Refresh access token using refresh token"""
        async with httpx.AsyncClient() as client:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.SPOTIFY_CLIENT_ID,
                "client_secret": settings.SPOTIFY_CLIENT_SECRET,
            }
            
            response = await client.post(self.auth_url, data=data)
            response.raise_for_status()
            return response.json()
    
    async def get_top_tracks(self, access_token: str) -> List[Track]:
        """Fetch user's top tracks from Spotify"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/me/top/tracks?limit=50&time_range=short_term",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            tracks = []
            for item in data["items"]:
                track = Track(
                    id=item["id"],
                    title=item["name"],
                    artist=item["artists"][0]["name"],
                    cover_url=item["album"]["images"][0]["url"] if item["album"]["images"] else ""
                )
                tracks.append(track)
            
            return tracks
    
    async def get_audio_features(self, access_token: str, track_ids: List[str]) -> Dict[str, AudioFeatures]:
        """Fetch audio features for multiple tracks"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Spotify API allows max 100 tracks per request
        all_features = {}
        
        for i in range(0, len(track_ids), 100):
            batch_ids = track_ids[i:i+100]
            ids_param = ",".join(batch_ids)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/audio-features?ids={ids_param}",
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                for audio_feature in data["audio_features"]:
                    if audio_feature:  # Some tracks might not have audio features
                        features = AudioFeatures(
                            valence=audio_feature["valence"],
                            energy=audio_feature["energy"],
                            tempo=audio_feature["tempo"],
                            danceability=audio_feature["danceability"]
                        )
                        all_features[audio_feature["id"]] = features
        
        return all_features
    
    async def get_recommendations(self, access_token: str, seed_tracks: List[str], target_emotion: str) -> List[Track]:
        """Get track recommendations based on emotion"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Map emotions to Spotify parameters
        emotion_params = {
            "joy": {"target_valence": 0.8, "target_energy": 0.7, "target_danceability": 0.7},
            "sadness": {"target_valence": 0.2, "target_energy": 0.3, "target_danceability": 0.3},
            "calm": {"target_valence": 0.6, "target_energy": 0.2, "target_danceability": 0.4},
            "excitement": {"target_valence": 0.7, "target_energy": 0.9, "target_danceability": 0.8},
            "anger": {"target_valence": 0.3, "target_energy": 0.8, "target_danceability": 0.5}
        }
        
        params = {
            "seed_tracks": ",".join(seed_tracks[:5]),  # Max 5 seed tracks
            "limit": 5,
            **emotion_params.get(target_emotion, {})
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/recommendations",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            recommendations = []
            for track in data["tracks"]:
                rec_track = Track(
                    id=track["id"],
                    title=track["name"],
                    artist=track["artists"][0]["name"],
                    cover_url=track["album"]["images"][0]["url"] if track["album"]["images"] else ""
                )
                recommendations.append(rec_track)
            
            return recommendations

spotify_client = SpotifyClient() 