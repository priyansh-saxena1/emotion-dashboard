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
    print(f"🔍 [AUTH] Checking session for request from {request.client.host}")
    print(f"🔍 [AUTH] Request cookies: {request.cookies}")
    
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        print(f"❌ [AUTH] No session cookie found")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    print(f"🔍 [AUTH] Session cookie found: {session_cookie[:20]}...")
    
    session_data = get_session_data(session_cookie)
    if not session_data:
        print(f"❌ [AUTH] Failed to decode session data")
        raise HTTPException(status_code=401, detail="Invalid session")
    
    if "access_token" not in session_data:
        print(f"❌ [AUTH] No access token in session data")
        raise HTTPException(status_code=401, detail="Invalid session")
    
    print(f"✅ [AUTH] Valid session found, access token: {session_data['access_token'][:20]}...")
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
    print(f"🔄 [CALLBACK] Received Spotify callback with code: {code[:20]}...")
    try:
        # Exchange code for tokens
        print(f"🔄 [CALLBACK] Exchanging code for tokens...")
        token_data = await spotify_client.exchange_code_for_tokens(code)
        print(f"✅ [CALLBACK] Token exchange successful")
        
        # Create session data
        session_data = {
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": token_data.get("expires_in", 3600)
        }
        print(f"🔍 [CALLBACK] Session data created with access token: {session_data['access_token'][:20]}...")
        
        # Create secure session cookie
        session_cookie = create_session_cookie(session_data)
        print(f"🍪 [CALLBACK] Session cookie created: {session_cookie[:20]}...")
        
        # Set cookie and redirect to frontend
        frontend_url = settings.FRONTEND_URL
        print(f"🔄 [CALLBACK] Redirecting to frontend: {frontend_url}")
        
        response = RedirectResponse(url=frontend_url)
        response.set_cookie(
            key="session",
            value=session_cookie,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=3600
        )
        
        print(f"✅ [CALLBACK] Successfully set session cookie and redirecting")
        return response
        
    except Exception as e:
        print(f"❌ [CALLBACK] Error in Spotify callback: {e}")
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