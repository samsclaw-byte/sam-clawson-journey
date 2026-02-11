#!/usr/bin/env python3
"""
Simple Voice Transcription Test
Tests the Google Cloud Speech-to-Text setup
"""

import os
from google.cloud import speech
import io

def test_speech_setup():
    """Test if speech client can be initialized"""
    try:
        client = speech.SpeechClient()
        print("✅ Google Speech client initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing speech client: {e}")
        return False

def create_test_audio():
    """Create a simple test audio file (1 second of silence)"""
    # For now, we'll just test the client setup
    # Actual audio transcription will come after billing setup
    print("🎤 Ready for voice transcription once billing is enabled!")

if __name__ == "__main__":
    print("Testing Google Speech-to-Text setup...")
    
    # Test 1: Client initialization
    if test_speech_setup():
        print("✅ Setup complete - ready for billing activation!")
        print("\nNext steps:")
        print("1. Set up billing account")
        print("2. Enable Speech-to-Text API")
        print("3. Start transcribing voice messages!")
    else:
        print("❌ Setup needs attention")