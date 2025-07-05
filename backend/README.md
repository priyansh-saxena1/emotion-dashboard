# Emotional Soundscape Backend

A FastAPI backend for analyzing emotions in music using Spotify API and OpenRouter's LLM services.

## Features

- **Spotify Integration**: OAuth 2.0 authentication and track analysis
- **AI-Powered Emotion Analysis**: Uses OpenRouter's GPT models to classify emotions
- **Caching**: LRU cache for audio features and analysis results
- **Session Management**: Secure server-side sessions with cookies
- **Recommendations**: Get personalized track recommendations based on emotions

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and fill in your credentials:

```bash
cp env.example .env
```

Edit `.env` with your actual credentials:

- **Spotify API**: Get from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- **OpenRouter API**: Get from [OpenRouter](https://openrouter.ai/) (free tier available)

### 3. Spotify App Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add `http://127.0.0.1:8000/callback` to Redirect URIs
4. Copy Client ID and Client Secret to `.env`

### 4. OpenRouter Setup

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your API key (free tier available)
3. Add to `.env`

## Running the Backend

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `GET /api/login` - Initiate Spotify OAuth
- `GET /api/callback` - Handle OAuth callback

### User Data
- `GET /api/user/top-tracks` - Get user's top tracks

### Analysis
- `POST /api/analyze` - Analyze emotions for selected tracks

### Recommendations
- `GET /api/recommendations?emotion=<emotion>` - Get recommendations

### Health
- `GET /api/health` - Health check
- `GET /api/metrics` - Basic metrics

## API Documentation

Once running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Frontend Integration

The backend is designed to work with the React frontend. Make sure:

1. Frontend is running on `http://127.0.0.1:3000`
2. CORS is properly configured (already set up)
3. All API calls use the correct endpoints

## Error Handling

The API returns consistent error responses:

```json
{
  "detail": "Error message here"
}
```

Common status codes:
- `401` - Authentication required
- `400` - Bad request
- `502` - LLM service error
- `500` - Internal server error

## Caching

The backend uses in-memory LRU caches:
- **Audio Features**: 10 minutes TTL
- **Analysis Results**: 1 hour TTL

## Security Notes

- Session cookies are HTTP-only and secure
- OAuth tokens are stored server-side only
- CORS is configured for local development
- Change `SECRET_KEY` in production 