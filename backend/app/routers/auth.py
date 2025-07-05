from fastapi import APIRouter, Request, Response, Query
from ..auth import handle_spotify_login, handle_spotify_callback

router = APIRouter()

@router.get("/api/login")
async def login():
    """Initiate Spotify OAuth flow"""
    return await handle_spotify_login()

@router.get("/api/callback")
async def callback(code: str = Query(...), response: Response = None):
    """Handle Spotify OAuth callback"""
    return await handle_spotify_callback(code, response) 