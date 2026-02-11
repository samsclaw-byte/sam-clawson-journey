#!/usr/bin/env python3
"""Quick test of voice transcription systems"""

import os
from voice_transcribe import transcribe_audio_file

def test_transcription():
    """Test with a simple audio file if available"""
    # Look for any existing audio files
    test_files = [
        "/tmp/tts-dy2JTx/voice-1770097968952.mp3",
        "test.wav",
        "test.mp3",
        "sample.ogg"
    ]
    
    for audio_file in test_files:
        if os.path.exists(audio_file):
            print(f"Testing with {audio_file}...")
            result = transcribe_audio_file(audio_file)
            if result:
                print(f"✅ Success: {result}")
                return True
            else:
                print(f"❌ Failed to transcribe {audio_file}")
                return False
    
    print("No test audio files found. Creating a simple test...")
    return False

if __name__ == "__main__":
    test_transcription()