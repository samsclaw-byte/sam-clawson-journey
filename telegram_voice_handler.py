#!/usr/bin/env python3
"""
Telegram Voice Message Handler for OpenClaw
Processes voice messages and returns transcriptions
"""

import sys
import base64
from voice_transcribe import transcribe_telegram_voice

def process_voice_message(base64_audio, language="en-US"):
    """
    Process a base64-encoded voice message from Telegram
    
    Args:
        base64_audio: Base64-encoded audio content
        language: Language code (default: en-US)
    
    Returns:
        Transcribed text or error message
    """
    try:
        # Decode base64 audio
        audio_content = base64.b64decode(base64_audio)
        
        # Transcribe
        transcript = transcribe_telegram_voice(audio_content, language)
        
        if transcript:
            return f"🎤 Voice transcription:\n\n{transcript}"
        else:
            return "❌ Sorry, I couldn't transcribe that audio. Please try again."
            
    except Exception as e:
        return f"❌ Error processing voice message: {e}"

def main():
    """Main function for testing or command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python3 telegram_voice_handler.py <base64_audio> [language]")
        print("       echo 'base64_audio_content' | python3 telegram_voice_handler.py")
        return
    
    base64_audio = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "en-US"
    
    result = process_voice_message(base64_audio, language)
    print(result)

if __name__ == "__main__":
    main()