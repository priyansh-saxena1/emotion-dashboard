from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class Track(BaseModel):
    id: str
    title: str
    artist: str
    cover_url: str

class AudioFeatures(BaseModel):
    valence: float
    energy: float
    tempo: float
    danceability: float

class EmotionScores(BaseModel):
    joy: float
    sadness: float
    calm: float
    excitement: float
    anger: float

class AnalyzeRequest(BaseModel):
    track_ids: List[str]

class AnalyzeResponse(BaseModel):
    heatmap: Dict[str, EmotionScores]
    why: Dict[str, str]

class TopTracksResponse(BaseModel):
    tracks: List[Track]

class RecommendationsResponse(BaseModel):
    recommendations: List[Track]

class HealthResponse(BaseModel):
    status: str
    uptime: int

class EmotionEnum(str, Enum):
    joy = "joy"
    sadness = "sadness"
    calm = "calm"
    excitement = "excitement"
    anger = "anger" 