from fastapi import APIRouter
from ..schemas import HealthResponse
import time

router = APIRouter()

# Track startup time for uptime calculation
startup_time = time.time()

@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = int(time.time() - startup_time)
    return HealthResponse(status="ok", uptime=uptime)

@router.get("/api/metrics")
async def get_metrics():
    """Get basic metrics"""
    from ..cache import audio_features_cache, analysis_cache
    
    return {
        "requests": 0,  # Could implement request counting
        "cache_hits": len(audio_features_cache) + len(analysis_cache),
        "uptime": int(time.time() - startup_time)
    } 