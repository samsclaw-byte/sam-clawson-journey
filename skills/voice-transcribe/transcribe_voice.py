#!/usr/bin/env python3
"""Quick voice transcription using OpenAI API"""

import os
import sys
from pathlib import Path

# Load API key from .env
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        content = f.read().strip()
        if content.startswith("OPENAI_API_KEY="):
            os.environ["OPENAI_API_KEY"] = content.split("=", 1)[1]
        elif content.startswith("sk-"):
            os.environ["OPENAI_API_KEY"] = content

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env", file=sys.stderr)
    sys.exit(1)

def transcribe_file(audio_path):
    """Transcribe audio file using OpenAI API"""
    try:
        import requests
    except ImportError:
        print("Error: requests library not available", file=sys.stderr)
        sys.exit(1)
    
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    with open(audio_path, "rb") as audio_file:
        files = {
            "file": (os.path.basename(audio_path), audio_file, "audio/ogg"),
            "model": (None, "gpt-4o-mini-transcribe")
        }
        response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        print(f"Error: {response.status_code} - {response.text}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_voice.py <audio-file>", file=sys.stderr)
        sys.exit(1)
    
    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"Error: File not found: {audio_file}", file=sys.stderr)
        sys.exit(1)
    
    transcript = transcribe_file(audio_file)
    print(transcript)
