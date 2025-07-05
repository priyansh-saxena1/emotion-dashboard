from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeSerializer
from typing import Optional
import urllib.parse
from .config import settings
from .spotify_client import spotify_client

# Session serializer
serializer = URLSafeSerializer(settings.SECRET_KEY)

def create_session_cookie(user_data: dict) -> str:
    """Create a secure session cookie"""
    return serializer.dumps(user_data)

def get_session_data(cookie_value: str) -> Optional[dict]:
    """Get session data from cookie"""
    try:
        return serializer.loads(cookie_value)
    except:
        return None

def get_session_token(request: Request) -> str:
    """Get access token from session"""
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session_data = get_session_data(session_cookie)
    if not session_data or "access_token" not in session_data:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    return session_data["access_token"]

async def handle_spotify_login():
    """Handle Spotify login redirect"""
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": "user-top-read user-read-private",
        "show_dialog": "true"
    }
    
    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url=auth_url)

async def handle_spotify_callback(code: str, response: Response):
    """Handle Spotify OAuth callback"""
    try:
        # Exchange code for tokens
        token_data = await spotify_client.exchange_code_for_tokens(code)
        
        # Create session data
        session_data = {
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": token_data.get("expires_in", 3600)
        }
        
        # Create secure session cookie
        session_cookie = create_session_cookie(session_data)
        
        # Set cookie and redirect to frontend
        response = RedirectResponse(url=settings.FRONTEND_URL)
        response.set_cookie(
            key="session",
            value=session_cookie,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=3600
        )
        
        return response
        
    except Exception as e:
        print(f"Error in Spotify callback: {e}")
        # Redirect to frontend with error
        error_url = f"{settings.FRONTEND_URL}?error=auth_failed"
        return RedirectResponse(url=error_url)

async def refresh_session_token(request: Request) -> str:
    """Refresh access token if needed"""
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session_data = get_session_data(session_cookie)
    if not session_data:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Check if token needs refresh
    if "refresh_token" in session_data:
        try:
            token_data = await spotify_client.refresh_access_token(session_data["refresh_token"])
            
            # Update session data
            session_data["access_token"] = token_data["access_token"]
            if "refresh_token" in token_data:
                session_data["refresh_token"] = token_data["refresh_token"]
            
            # Update cookie
            new_session_cookie = create_session_cookie(session_data)
            request.cookies["session"] = new_session_cookie
            
            return token_data["access_token"]
            
        except Exception as e:
            print(f"Error refreshing token: {e}")
            raise HTTPException(status_code=401, detail="Token refresh failed")
    
    return session_data["access_token"] 