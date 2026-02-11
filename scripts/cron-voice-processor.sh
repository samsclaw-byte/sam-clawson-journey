#!/bin/bash
# Auto Voice Transcription Cron Job
# Runs every 2 minutes to process new voice messages

MEDIA_DIR="/home/samsclaw/.openclaw/media/inbound"
PROCESSED_LOG="/home/samsclaw/.openclaw/media/inbound/.processed_voices"
WHISPER="/home/samsclaw/.miniforge/envs/whisper/bin/whisper"

# Create processed log if doesn't exist
touch "$PROCESSED_LOG"

# Find new .ogg files
for ogg_file in "$MEDIA_DIR"/file_*.ogg; do
    [ -f "$ogg_file" ] || continue
    
    # Check if already processed
    basename=$(basename "$ogg_file")
    if grep -q "^$basename$" "$PROCESSED_LOG" 2>/dev/null; then
        continue
    fi
    
    # Transcribe
    TMP_DIR=$(mktemp -d)
    export PATH="/home/samsclaw/.miniforge/envs/whisper/bin:$PATH"
    
    if $WHISPER "$ogg_file" --model base --output_format txt --output_dir "$TMP_DIR" --fp16 False 2>/dev/null; then
        TRANSCRIPT_FILE="$TMP_DIR/${basename%.ogg}.txt"
        if [ -f "$TRANSCRIPT_FILE" ]; then
            TRANSCRIPT=$(cat "$TRANSCRIPT_FILE")
            echo "🎤 **Voice Message Transcribed:**

$TRANSCRIPT

---
*Reply to respond* 🦞"
        fi
    fi
    
    # Cleanup
    rm -rf "$TMP_DIR"
    
    # Mark as processed
    echo "$basename" >> "$PROCESSED_LOG"
done
