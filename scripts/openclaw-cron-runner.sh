#!/bin/bash
# OpenClaw Cron Jobs - External Linux Cron Version
# These run via system crontab, NOT OpenClaw's internal scheduler
# This bypasses the OpenClaw scheduler bug (issue #10353)

# Configuration
export OPENCLAW_GATEWAY_URL="ws://127.0.0.1:18789"
export HOME="/home/samsclaw"
export PATH="$HOME/.npm-global/bin:$PATH"

# Function to send message via OpenClaw
send_message() {
    local text="$1"
    # This would need OpenClaw CLI or API call
    # Placeholder for actual implementation
    echo "[$$(date)] Would send: $text" >> /tmp/openclaw-cron.log
}

# 6am - Morning Briefing
case "${1:-}" in
    morning)
        echo "Running morning briefing..."
        # Fetch data
        token_info=$(/home/samsclaw/.openclaw/workspace/scripts/token_estimate.sh 2>/dev/null | head -20)
        
        # Send via Telegram (using curl or similar)
        # This requires Telegram bot token setup
        ;;
        
    midday)
        echo "Running midday check..."
        ;;
        
    afternoon)
        echo "Running afternoon check..."
        ;;
        
    evening)
        echo "Running evening check..."
        ;;
        
    voice)
        echo "Processing voice messages..."
        /home/samsclaw/.openclaw/workspace/scripts/cron-voice-processor.sh
        ;;
        
    *)
        echo "Usage: $0 {morning|midday|afternoon|evening|voice}"
        exit 1
        ;;
esac
