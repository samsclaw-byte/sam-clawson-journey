#!/bin/bash
# Auto-transcription for Telegram voice messages
# This script can be hooked into the voice message reception pipeline

VOICE_FILE="$1"
if [ -z "$$VOICE_FILE" ]; then
    echo "Usage: $0 <voice-file.ogg>"
    exit 1
fi

if [ ! -f "$VOICE_FILE" ]; then
    echo "Error: File not found: $VOICE_FILE"
    exit 1
fi

# Run whisper transcription
export PATH="/home/samsclaw/.miniforge/envs/whisper/bin:$PATH"
TMP_DIR=$(mktemp -d)
whisper "$VOICE_FILE" --model base --output_format txt --output_dir "$TMP_DIR" --fp16 False 2>/dev/null

# Extract and output transcript
BASENAME=$(basename "$VOICE_FILE" .ogg)
TRANSCRIPT_FILE="$TMP_DIR/${BASENAME}.txt"

if [ -f "$TRANSCRIPT_FILE" ]; then
    cat "$TRANSCRIPT_FILE"
    rm -rf "$TMP_DIR"
    exit 0
else
    echo "Error: Transcription failed"
    rm -rf "$TMP_DIR"
    exit 1
fi
