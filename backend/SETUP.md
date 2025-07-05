# Quick Setup Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up Environment

```bash
cp env.example .env
# Edit .env with your actual credentials
```

## 3. Get API Keys

### Spotify API
1. Go to https://developer.spotify.com/dashboard
2. Create a new app
3. Add `http://127.0.0.1:8000/callback` to Redirect URIs
4. Copy Client ID and Client Secret

### OpenRouter API
1. Go to https://openrouter.ai/
2. Sign up (free tier available)
3. Get your API key

## 4. Run the Backend

```bash
python3 run.py
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 5. Test the API

Visit http://127.0.0.1:8000/docs to see the interactive API documentation.

## 6. Connect Frontend

Make sure your React frontend is running on http://127.0.0.1:3000 and it will automatically connect to the backend.

## Troubleshooting

- **Import errors**: Make sure you've installed all dependencies
- **401 errors**: Check your Spotify API credentials
- **502 errors**: Check your OpenRouter API key
- **CORS errors**: Make sure frontend is running on http://127.0.0.1:3000 