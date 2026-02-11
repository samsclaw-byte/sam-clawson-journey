#!/usr/bin/env python3
"""Debug Google Cloud authentication and test simple transcription"""

import os
import json
from pathlib import Path

def check_google_auth():
    """Check Google Cloud authentication status"""
    print("🔍 Checking Google Cloud authentication...")
    
    # Check for application default credentials
    adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
    if adc_path.exists():
        print(f"✅ Found ADC at: {adc_path}")
        with open(adc_path) as f:
            creds = json.load(f)
            print(f"   Type: {creds.get('type', 'unknown')}")
            print(f"   Client ID: {creds.get('client_id', 'none')[:20]}...")
    else:
        print("❌ No application default credentials found")
    
    # Check environment variables
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print(f"✅ GOOGLE_APPLICATION_CREDENTIALS: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
    else:
        print("ℹ️  GOOGLE_APPLICATION_CREDENTIALS not set (using ADC)")
    
    return adc_path.exists()

def test_simple_google_stt():
    """Test with a minimal audio sample"""
    try:
        from google.cloud import speech
        print("\n🎤 Testing Google Cloud Speech-to-Text...")
        
        # Create client
        client = speech.SpeechClient()
        print("✅ Client created successfully")
        
        # Test with 1 second of silence in LINEAR16 format (raw PCM)
        # This should be processed quickly
        sample_rate = 16000
        duration_seconds = 1
        samples = sample_rate * duration_seconds
        
        # Generate silence (zeros)
        import struct
        silence_data = struct.pack('<' + 'h' * samples, *[0] * samples)
        
        audio = speech.RecognitionAudio(content=silence_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code="en-US",
        )
        
        print("Sending request...")
        response = client.recognize(config=config, audio=audio)
        print(f"✅ Got response with {len(response.results)} results")
        
        for i, result in enumerate(response.results):
            print(f"   Result {i}: {result.alternatives[0].transcript}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    auth_ok = check_google_auth()
    if auth_ok:
        test_simple_google_stt()
    else:
        print("\n❌ Cannot test - authentication issues")