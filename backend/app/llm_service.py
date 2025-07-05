import httpx
import json
from typing import List, Dict
from .schemas import Track, AudioFeatures, EmotionScores
from .config import settings

class LLMService:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = "gpt-3.5-turbo"
    
    async def classify_emotions(self, tracks_data: List[Dict]) -> Dict[str, EmotionScores]:
        """Classify emotions for multiple tracks using LLM"""
        if not tracks_data:
            return {}
        
        # Build prompt for emotion classification
        prompt = self._build_classification_prompt(tracks_data)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert music analyst. Analyze the emotional content of tracks based on their audio features and provide emotion scores."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.3,
                        "max_tokens": 2000
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Parse the response
                content = data["choices"][0]["message"]["content"]
                return self._parse_emotion_scores(content, [track["id"] for track in tracks_data])
                
        except Exception as e:
            print(f"Error in emotion classification: {e}")
            # Return default scores if LLM fails
            return self._get_default_scores([track["id"] for track in tracks_data])
    
    async def explain_emotions(self, tracks_data: List[Dict], heatmap: Dict[str, EmotionScores]) -> Dict[str, str]:
        """Generate explanations for dominant emotions"""
        explanations = {}
        
        for track_data in tracks_data:
            track_id = track_data["id"]
            if track_id in heatmap:
                dominant_emotion = self._get_dominant_emotion(heatmap[track_id])
                explanation = await self._explain_single_track(track_data, dominant_emotion)
                explanations[track_id] = explanation
        
        return explanations
    
    def _build_classification_prompt(self, tracks_data: List[Dict]) -> str:
        """Build prompt for emotion classification"""
        prompt = "Analyze the emotional content of these tracks based on their audio features. Return ONLY a valid JSON object with the following structure:\n\n"
        prompt += "{\n"
        for track in tracks_data:
            prompt += f'  "{track["id"]}": {{\n'
            prompt += f'    "joy": <score 0-1>,\n'
            prompt += f'    "sadness": <score 0-1>,\n'
            prompt += f'    "calm": <score 0-1>,\n'
            prompt += f'    "excitement": <score 0-1>,\n'
            prompt += f'    "anger": <score 0-1>\n'
            prompt += f'  }},\n'
        prompt = prompt.rstrip(',\n') + "\n}\n\n"
        
        prompt += "Track details:\n"
        for track in tracks_data:
            features = track["features"]
            prompt += f"- Track: {track['title']} by {track['artist']}\n"
            prompt += f"  Valence: {features.valence:.2f} (happiness)\n"
            prompt += f"  Energy: {features.energy:.2f} (intensity)\n"
            prompt += f"  Tempo: {features.tempo:.0f} BPM\n"
            prompt += f"  Danceability: {features.danceability:.2f}\n\n"
        
        return prompt
    
    def _parse_emotion_scores(self, content: str, track_ids: List[str]) -> Dict[str, EmotionScores]:
        """Parse emotion scores from LLM response"""
        try:
            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                return self._get_default_scores(track_ids)
            
            json_str = content[start_idx:end_idx]
            data = json.loads(json_str)
            
            results = {}
            for track_id in track_ids:
                if track_id in data:
                    scores = data[track_id]
                    results[track_id] = EmotionScores(
                        joy=float(scores.get("joy", 0.5)),
                        sadness=float(scores.get("sadness", 0.5)),
                        calm=float(scores.get("calm", 0.5)),
                        excitement=float(scores.get("excitement", 0.5)),
                        anger=float(scores.get("anger", 0.5))
                    )
                else:
                    results[track_id] = self._get_default_emotion_scores()
            
            return results
            
        except Exception as e:
            print(f"Error parsing emotion scores: {e}")
            return self._get_default_scores(track_ids)
    
    async def _explain_single_track(self, track_data: Dict, dominant_emotion: str) -> str:
        """Generate explanation for a single track's dominant emotion"""
        features = track_data["features"]
        
        prompt = f"""Explain in 1-2 sentences why the track "{track_data['title']}" by {track_data['artist']} feels {dominant_emotion}, based on these audio features:
- Valence: {features.valence:.2f} (happiness)
- Energy: {features.energy:.2f} (intensity)  
- Tempo: {features.tempo:.0f} BPM
- Danceability: {features.danceability:.2f}

Provide a brief, natural explanation:"""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 100
                    },
                    timeout=15.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
                
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return f"This track has a {dominant_emotion} feeling based on its musical characteristics."
    
    def _get_dominant_emotion(self, scores: EmotionScores) -> str:
        """Get the dominant emotion from scores"""
        emotion_values = {
            "joy": scores.joy,
            "sadness": scores.sadness,
            "calm": scores.calm,
            "excitement": scores.excitement,
            "anger": scores.anger
        }
        return max(emotion_values, key=emotion_values.get)
    
    def _get_default_emotion_scores(self) -> EmotionScores:
        """Get default emotion scores"""
        return EmotionScores(
            joy=0.5,
            sadness=0.5,
            calm=0.5,
            excitement=0.5,
            anger=0.5
        )
    
    def _get_default_scores(self, track_ids: List[str]) -> Dict[str, EmotionScores]:
        """Get default scores for multiple tracks"""
        return {track_id: self._get_default_emotion_scores() for track_id in track_ids}

llm_service = LLMService() 