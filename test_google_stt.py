#!/usr/bin/env python3
"""Test Google Cloud Speech-to-Text with proper configuration"""

from google.cloud import speech
import io

def test_google_stt():
    """Simple test of Google Cloud Speech-to-Text"""
    try:
        # Initialize client
        client = speech.SpeechClient()
        print("✅ Google Cloud client initialized successfully")
        
        # Test with a very short audio sample (1 second of silence)
        # This is a minimal valid MP3 file (can be processed as LINEAR16)
        test_audio = b'\xff\xfb\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        
        audio = speech.RecognitionAudio(content=test_audio)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Try MP3 encoding
            sample_rate_hertz=24000,  # Match our TTS output
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        
        print("Testing recognition...")
        response = client.recognize(config=config, audio=audio)
        print(f"✅ Recognition successful! Results: {len(response.results)}")
        
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_google_stt()