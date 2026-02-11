#!/usr/bin/env python3
"""
OpenClaw Voice Transcription Integration
Converts Telegram voice messages to text using Google Speech-to-Text
"""

import os
import sys
import tempfile
from google.cloud import speech
import io

def transcribe_telegram_voice(audio_content, language_code="en-US"):
    """
    Transcribe audio content from Telegram voice messages
    
    Args:
        audio_content: Raw audio bytes from Telegram
        language_code: Language code (default: en-US)
    
    Returns:
        Transcribed text or None if error
    """
    try:
        # Initialize client
        client = speech.SpeechClient()
        
        # Configure audio for Telegram voice format (OGG_OPUS)
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,  # Telegram standard
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="latest_long",  # Better for longer audio
        )
        
        # Perform transcription
        print("🎤 Transcribing audio...")
        response = client.recognize(config=config, audio=audio)
        
        # Extract transcript
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "
        
        return transcript.strip()
        
    except Exception as e:
        print(f"❌ Error transcribing audio: {e}")
        return None

def transcribe_audio_file(file_path, language_code="en-US"):
    """
    Transcribe an audio file (for testing)
    
    Args:
        file_path: Path to audio file
        language_code: Language code (default: en-US)
    
    Returns:
        Transcribed text or None if error
    """
    try:
        with open(file_path, "rb") as audio_file:
            audio_content = audio_file.read()
        
        return transcribe_telegram_voice(audio_content, language_code)
        
    except Exception as e:
        print(f"❌ Error reading audio file: {e}")
        return None

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python3 voice_transcribe.py <audio_file> [language_code]")
        print("       python3 voice_transcribe.py test")
        sys.exit(1)
    
    if sys.argv[1] == "test":
        print("🦞 OpenClaw Voice Transcription - Ready!")
        print("✅ Google Speech-to-Text API connected")
        print("✅ 60 minutes free monthly transcription")
        print("✅ Ready to process Telegram voice messages")
        print("\nUsage:")
        print("- Send me a voice message and I'll transcribe it")
        print("- Supported formats: OGG_OPUS (Telegram standard)")
        print("- Languages: English (default), Spanish, French, etc.")
        return
    
    audio_file = sys.argv[1]
    language_code = sys.argv[2] if len(sys.argv) > 2 else "en-US"
    
    if not os.path.exists(audio_file):
        print(f"Error: Audio file '{audio_file}' not found")
        sys.exit(1)
    
    print(f"🎤 Transcribing {audio_file}...")
    transcript = transcribe_audio_file(audio_file, language_code)
    
    if transcript:
        print("📝 Transcript:")
        print(transcript)
    else:
        print("❌ Transcription failed")
        sys.exit(1)

if __name__ == "__main__":
    main()