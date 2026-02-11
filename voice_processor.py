#!/usr/bin/env python3
"""
OpenClaw Voice Message Processor
Handles incoming Telegram voice messages with multiple transcription methods
"""

import os
import sys
import base64
import tempfile
import json
from pathlib import Path

def process_telegram_voice_message(audio_data, method="auto"):
    """
    Process a Telegram voice message using available transcription methods
    
    Args:
        audio_data: Base64-encoded audio content or file path
        method: "google", "telegram", "local", or "auto"
    
    Returns:
        Dict with transcription results and method used
    """
    result = {
        "success": False,
        "transcription": None,
        "method": None,
        "error": None,
        "confidence": None
    }
    
    try:
        # Determine input type
        if audio_data.startswith('/tmp/') or audio_data.startswith('./') or audio_data.startswith('/home/'):
            # File path
            audio_content = Path(audio_data).read_bytes()
        else:
            # Base64 encoded
            audio_content = base64.b64decode(audio_data)
        
        print(f"🎤 Processing {len(audio_content)} bytes of audio data...")
        
        # Try methods in order of preference
        methods_to_try = []
        if method == "auto":
            methods_to_try = ["telegram", "google", "local"]
        else:
            methods_to_try = [method]
        
        for try_method in methods_to_try:
            print(f"Trying {try_method} transcription...")
            
            if try_method == "telegram":
                # Use Telegram's built-in transcription (Premium feature)
                transcription = try_telegram_transcription(audio_content)
                if transcription:
                    result.update({
                        "success": True,
                        "transcription": transcription,
                        "method": "telegram",
                        "confidence": "high"
                    })
                    break
                    
            elif try_method == "google":
                # Use Google Cloud Speech-to-Text
                transcription = try_google_transcription(audio_content)
                if transcription:
                    result.update({
                        "success": True,
                        "transcription": transcription,
                        "method": "google",
                        "confidence": "high"
                    })
                    break
                    
            elif try_method == "local":
                # Use local Whisper (if available)
                transcription = try_local_whisper(audio_content)
                if transcription:
                    result.update({
                        "success": True,
                        "transcription": transcription,
                        "method": "local",
                        "confidence": "medium"
                    })
                    break
        
        if not result["success"]:
            result["error"] = "All transcription methods failed"
            
    except Exception as e:
        result["error"] = f"Processing error: {e}"
    
    return result

def try_telegram_transcription(audio_content):
    """Try Telegram Premium transcription"""
    try:
        # For now, this would be handled by the Telegram integration
        # Return None to indicate we should use the built-in feature
        return None
    except Exception as e:
        print(f"Telegram method failed: {e}")
        return None

def try_google_transcription(audio_content):
    """Try Google Cloud Speech-to-Text"""
    try:
        # Import here to avoid issues if not configured
        from google.cloud import speech
        
        client = speech.SpeechClient()
        
        # Configure for Telegram voice format
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            model="latest_long",
        )
        
        response = client.recognize(config=config, audio=audio)
        
        if response.results:
            transcript = " ".join([result.alternatives[0].transcript for result in response.results])
            return transcript.strip()
        
        return None
        
    except Exception as e:
        print(f"Google STT failed: {e}")
        return None

def try_local_whisper(audio_content):
    """Try local Whisper transcription"""
    try:
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_file:
            tmp_file.write(audio_content)
            tmp_path = tmp_file.name
        
        try:
            # Import Whisper
            import whisper
            
            # Load model (this will download if needed)
            model = whisper.load_model("base")
            
            # Transcribe
            result = model.transcribe(tmp_path)
            return result["text"].strip()
            
        finally:
            # Clean up
            os.unlink(tmp_path)
            
    except Exception as e:
        print(f"Local Whisper failed: {e}")
        return None

def main():
    """Main function for testing"""
    if len(sys.argv) < 2:
        print("Usage: python voice_processor.py <audio_file_or_base64> [method]")
        print("Methods: auto, telegram, google, local")
        return
    
    audio_input = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    print(f"🦞 Clawson Voice Processor - Testing with method: {method}")
    
    result = process_telegram_voice_message(audio_input, method)
    
    print(f"\n📊 Results:")
    print(f"Success: {result['success']}")
    print(f"Method: {result['method']}")
    print(f"Transcription: {result['transcription']}")
    print(f"Error: {result['error']}")
    
    if result['success']:
        print(f"\n📝 Transcription:")
        print(result['transcription'])

if __name__ == "__main__":
    main()