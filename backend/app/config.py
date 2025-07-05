import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Spotify API Configuration
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8000/callback")
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    # Session Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Cache Configuration
    AUDIO_FEATURES_CACHE_TTL = 600  # 10 minutes
    ANALYSIS_CACHE_TTL = 3600  # 1 hour
    
    # Frontend URL for redirects
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:3000")

settings = Settings() 