#!/usr/bin/env python3
"""
Quick Voice Transcription Test
Uses Whisper to transcribe audio files
"""

import subprocess
import sys
import os

def transcribe_audio(audio_path):
    """Transcribe audio using Whisper"""
    whisper_path = "/home/samsclaw/.miniforge/envs/whisper/bin/whisper"
    
    if not os.path.exists(audio_path):
        return f"Error: File not found: {audio_path}"
    
    try:
        # Run whisper with base model (faster)
        result = subprocess.run(
            [whisper_path, audio_path, "--model", "base", "--output_format", "txt", "--output_dir", "/tmp"],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        if result.returncode == 0:
            # Read the output file
            base_name = os.path.basename(audio_path).replace('.ogg', '.txt')
            output_file = f"/tmp/{base_name}"
            
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    return f.read().strip()
            else:
                return "Transcription completed but output file not found"
        else:
            return f"Error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Transcription timed out (taking too long)"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_voice.py <audio-file.ogg>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    print(f"Transcribing: {audio_file}")
    print("-" * 40)
    
    transcript = transcribe_audio(audio_file)
    print(transcript)
