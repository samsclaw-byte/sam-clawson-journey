#!/bin/bash
# Async voice transcription processor
# Queues files and processes them in background

QUEUE_DIR="/home/samsclaw/.openclaw/media/queue"
PROCESSED_DIR="/home/samsclaw/.openclaw/media/processed"
LOG_FILE="/tmp/voice-transcription.log"

mkdir -p "$QUEUE_DIR" "$PROCESSED_DIR"

# Function to transcribe a single file
transcribe_file() {
    local input_file="$1"
    local basename=$(basename "$input_file" .ogg)
    local output_file="$PROCESSED_DIR/${basename}.txt"
    
    echo "[$(date)] Starting transcription: $basename" >> "$LOG_FILE"
    
    # Use conda whisper environment
    source ~/.miniforge/etc/profile.d/conda.sh
    conda activate whisper
    
    # Transcribe with tiny model for speed
    timeout 300 python3 /home/samsclaw/.openclaw/workspace/skills/local-whisper/scripts/transcribe.py \
        "$input_file" --model tiny --language en > "$output_file" 2>> "$LOG_FILE"
    
    if [ $? -eq 0 ] && [ -s "$output_file" ]; then
        echo "[$(date)] ✓ Transcription complete: $basename" >> "$LOG_FILE"
        # Move original to processed
        mv "$input_file" "$PROCESSED_DIR/"
        return 0
    else
        echo "[$(date)] ✗ Transcription failed: $basename" >> "$LOG_FILE"
        return 1
    fi
}

# Process all queued files
process_queue() {
    for file in "$QUEUE_DIR"/*.ogg; do
        [ -e "$file" ] || continue
        transcribe_file "$file"
    done
}

# Main execution
if [ "$1" == "process" ]; then
    process_queue
elif [ "$1" == "queue" ] && [ -n "$2" ]; then
    # Add file to queue
    cp "$2" "$QUEUE_DIR/"
    echo "[$(date)] Queued: $(basename $2)" >> "$LOG_FILE"
else
    echo "Usage: $0 process|queue <file>"
    exit 1
fi
