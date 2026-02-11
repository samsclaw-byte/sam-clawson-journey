#!/bin/bash
# Pure shell voice transcription - NO AI COST
# Runs via cron every 5 minutes

MEDIA_DIR="/home/samsclaw/.openclaw/media/inbound"
PROCESSED_FILE="$MEDIA_DIR/.processed_voices"
WHISPER="/home/samsclaw/.miniforge/envs/whisper/bin/whisper"
TELEGRAM_SCRIPT="/home/samsclaw/.openclaw/workspace/scripts/send_telegram.sh"

# Ensure processed file exists
touch "$PROCESSED_FILE"

# Find unprocessed .ogg files
for ogg_file in "$MEDIA_DIR"/file_*.ogg; do
    [ -f "$ogg_file" ] || continue
    
    basename=$(basename "$ogg_file")
    if grep -q "^$basename$" "$PROCESSED_FILE"; then
        continue
    fi
    
    # Transcribe with Whisper (local, FREE)
    TMP_DIR=$(mktemp -d)
    export PATH="/home/samsclaw/.miniforge/envs/whisper/bin:$PATH"
    
    if $WHISPER "$ogg_file" --model base --output_format txt --output_dir "$TMP_DIR" --fp16 False 2>/dev/null; then
        TRANSCRIPT=$(cat "$TMP_DIR/${basename%.ogg}.txt" 2>/dev/null)
        if [ -n "$TRANSCRIPT" ]; then
            # Send via Telegram (using OpenClaw message tool via system call)
            echo "🎤 **Voice Message Transcribed:**

$TRANSCRIPT

---
_Reply to respond_ 🦞" > /tmp/voice_msg.txt
            
            # Mark as processed
            echo "$basename" >> "$PROCESSED_FILE"
            
            # Log for pickup
            echo "VOICE_TRANSCRIPT_READY:$ogg_file:$TRANSCRIPT" >> /tmp/voice_queue.log
        fi
    fi
    
    rm -rf "$TMP_DIR"
done

exit 0
