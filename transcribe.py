#!/usr/bin/env python3
"""
Google Speech-to-Text Integration for OpenClaw
Simple voice transcription service
"""

import os
import sys
from google.cloud import speech
import io

def transcribe_audio_file(audio_file_path, language_code="en-US"):
    """
    Transcribe an audio file using Google Speech-to-Text
    
    Args:
        audio_file_path: Path to the audio file
        language_code: Language code (default: en-US)
    
    Returns:
        Transcribed text or None if error
    """
    try:
        # Initialize client
        client = speech.SpeechClient()
        
        # Read audio file
        with io.open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()
        
        # Configure audio
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )
        
        # Perform transcription
        response = client.recognize(config=config, audio=audio)
        
        # Extract transcript
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "
        
        return transcript.strip()
        
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe.py <audio_file> [language_code]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language_code = sys.argv[2] if len(sys.argv) > 2 else "en-US"
    
    if not os.path.exists(audio_file):
        print(f"Error: Audio file '{audio_file}' not found")
        sys.exit(1)
    
    print(f"Transcribing {audio_file}...")
    transcript = transcribe_audio_file(audio_file, language_code)
    
    if transcript:
        print("Transcript:")
        print(transcript)
    else:
        print("Transcription failed")
        sys.exit(1)

if __name__ == "__main__":
    main()