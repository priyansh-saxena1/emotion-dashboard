#!/usr/bin/env python3
"""
Debug script to test authentication flow
"""
import os
from dotenv import load_dotenv

load_dotenv()

def debug_config():
    print("🔍 [DEBUG] Checking configuration...")
    
    # Check environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    frontend_url = os.getenv("FRONTEND_URL")
    secret_key = os.getenv("SECRET_KEY")
    
    print(f"✅ Spotify Client ID: {'SET' if client_id and client_id != 'your_spotify_client_id_here' else 'NOT SET'}")
    print(f"✅ Spotify Client Secret: {'SET' if client_secret and client_secret != 'your_spotify_client_secret_here' else 'NOT SET'}")
    print(f"✅ Redirect URI: {redirect_uri}")
    print(f"✅ Frontend URL: {frontend_url}")
    print(f"✅ Secret Key: {'SET' if secret_key and secret_key != 'your-secret-key-change-in-production' else 'NOT SET'}")
    
    print("\n📋 [DEBUG] Configuration Summary:")
    if not all([client_id, client_secret]) or client_id == 'your_spotify_client_id_here':
        print("❌ Spotify credentials not properly configured")
        print("   - Go to https://developer.spotify.com/dashboard")
        print("   - Create an app and get Client ID/Secret")
        print("   - Update your .env file")
    else:
        print("✅ Spotify credentials configured")
    
    if redirect_uri != "http://127.0.0.1:8000/callback":
        print("❌ Redirect URI mismatch")
        print(f"   - Expected: http://127.0.0.1:8000/callback")
        print(f"   - Found: {redirect_uri}")
    else:
        print("✅ Redirect URI configured correctly")
    
    if frontend_url != "http://127.0.0.1:5173":
        print("❌ Frontend URL mismatch")
        print(f"   - Expected: http://127.0.0.1:5173")
        print(f"   - Found: {frontend_url}")
    else:
        print("✅ Frontend URL configured correctly")

if __name__ == "__main__":
    debug_config() 