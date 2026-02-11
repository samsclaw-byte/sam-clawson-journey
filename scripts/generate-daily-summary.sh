#!/bin/bash
# Daily Summary Generator - DATA-POPULATED VERSION
# Pulls real data from workspace files and logs

DATE=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
YESTERDAY_DISPLAY=$(date -d "yesterday" +"%B %d, %Y")
REPO_DIR="/home/samsclaw/.openclaw/workspace/research"
SUMMARY_DIR="$REPO_DIR/daily-summaries"
WORKSPACE_DIR="/home/samsclaw/.openclaw/workspace"
HEALTH_LOG="$WORKSPACE_DIR/health/weight-food-log.md"
MEMORY_FILE="$WORKSPACE_DIR/memory/$YESTERDAY.md"

mkdir -p "$SUMMARY_DIR"
SUMMARY_FILE="$SUMMARY_DIR/$YESTERDAY-summary.md"

# ========== DATA COLLECTION FUNCTIONS ==========

# Extract habit data from health log
get_habit_data() {
    local habit="$1"
    if [ -f "$HEALTH_LOG" ]; then
        grep -A2 -i "^###.*$YESTERDAY" "$HEALTH_LOG" 2>/dev/null | grep -i "$habit" | head -1
    fi
}

# Get water intake from health log
get_water_intake() {
    if [ -f "$HEALTH_LOG" ]; then
        # Look for water entries on yesterday's date
        awk "/^###.*$YESTERDAY/,/^###/" "$HEALTH_LOG" 2>/dev/null | grep -i "water" | grep -oE "[0-9]+/[0-9]+" | tail -1
    fi
}

# Get exercise data from health log
get_exercise_data() {
    if [ -f "$HEALTH_LOG" ]; then
        local exercise_section=$(awk "/^###.*$YESTERDAY/,/^###/" "$HEALTH_LOG" 2>/dev/null | grep -A20 "Workout\|Exercise\|Run\|Swim")
        echo "$exercise_section"
    fi
}

# Get token usage estimate
get_token_usage() {
    if [ -x "$WORKSPACE_DIR/scripts/token_estimate.sh" ]; then
        "$WORKSPACE_DIR/scripts/token_estimate.sh" 2>/dev/null | head -30
    else
        echo "Token script not available"
    fi
}

# Get completed TAT tasks from memory file
get_completed_tasks() {
    if [ -f "$MEMORY_FILE" ]; then
        grep -E "^\s*- \[x\]|^\s*- ✅" "$MEMORY_FILE" 2>/dev/null | sed 's/^\s*- \[x\]\s*/- /;s/^\s*- ✅\s*/- /'
    fi
}

# Get pending TAT tasks from memory file
get_pending_tasks() {
    if [ -f "$MEMORY_FILE" ]; then
        grep -E "^\s*- \[ \]|^\s*- ⏳" "$MEMORY_FILE" 2>/dev/null | sed 's/^\s*- \[ \]\s*/- /;s/^\s*- ⏳\s*/- /'
    fi
}

# Get files created yesterday
get_files_created() {
    find "$WORKSPACE_DIR" -type f -newermt "$YESTERDAY 00:00" ! -newermt "$DATE 00:00" -printf "  - %p\n" 2>/dev/null | grep -v ".git" | head -20
}

# Get git commits from yesterday
get_git_commits() {
    cd "$REPO_DIR" 2>/dev/null && git log --since="$YESTERDAY 00:00" --until="$DATE 00:00" --oneline 2>/dev/null | sed 's/^/  - /'
}

# Get cron status
get_cron_status() {
    local job_count=$(crontab -l 2>/dev/null | grep -c "^[^#]" || echo "0")
    echo "$job_count jobs active"
}

# Get weight from health log
get_weight() {
    if [ -f "$HEALTH_LOG" ]; then
        grep -E "^\|.*$YESTERDAY.*\|.*kg" "$HEALTH_LOG" 2>/dev/null | tail -1 | awk -F'|' '{print $3}' | tr -d ' '
    fi
}

# ========== DATA POPULATION ==========

WATER_STATUS=$(get_water_intake)
[ -z "$WATER_STATUS" ] && WATER_STATUS="Check health log"

WEIGHT=$(get_weight)
[ -z "$WEIGHT" ] && WEIGHT="Not logged"

TOKEN_DATA=$(get_token_usage)
[ -z "$TOKEN_DATA" ] && TOKEN_DATA="Run token_estimate.sh for details"

COMPLETED_TASKS=$(get_completed_tasks)
[ -z "$COMPLETED_TASKS" ] && COMPLETED_TASKS="  - (Check memory/$YESTERDAY.md for details)"

PENDING_TASKS=$(get_pending_tasks)
[ -z "$PENDING_TASKS" ] && PENDING_TASKS="  - (Check TAT system in Notion)"

FILES_CREATED=$(get_files_created)
[ -z "$FILES_CREATED" ] && FILES_CREATED="  - (See git logs for file changes)"

GIT_COMMITS=$(get_git_commits)
[ -z "$GIT_COMMITS" ] && GIT_COMMITS="  - No commits yesterday"

CRON_STATUS=$(get_cron_status)

# ========== GENERATE SUMMARY ==========

cat > "$SUMMARY_FILE" << EOF
# Daily Summary - $YESTERDAY_DISPLAY

**Generated:** $DATE at 00:00  
**By:** Clawson 🦞

---

## 📊 Habits & Health

| Habit | Status | Notes |
|-------|--------|-------|
| 🚰 Water | $WATER_STATUS | From health log |
| 🍎 Fruit | Check health/weight-food-log.md | Target: 2 portions |
| 💊 Multivitamin | Check Notion habit tracker | Daily goal |
| 🏃 Exercise | Check health log for workout data | Target: 30+ min |
| 💊 Creatine | Check health log | 5g daily |

**Weight:** $WEIGHT

### Exercise Details
See \`health/weight-food-log.md\` for detailed workout breakdown with HR zones.

---

## ✅ Tasks Completed

### TAT System (Yesterday)
$COMPLETED_TASKS

### Pending Tasks
$PENDING_TASKS

---

## 💰 Token Usage & Costs ($YESTERDAY)

\`\`\`
$TOKEN_DATA
\`\`\`

**System Status:** $CRON_STATUS

---

## 📝 Activity Log

### Files Created/Modified
$FILES_CREATED

### GitHub Commits (Research Repo)
$GIT_COMMITS

### Voice Messages
- Check \`/home/samsclaw/.openclaw/media/inbound/\` for voice activity
- Transcription: Auto-processed every 5 minutes
- Logs: \`/tmp/cron-voice.log\`

---

## 🎯 Key Wins

(List major accomplishments from the day - populate from memory/$YESTERDAY.md)

### From Yesterday's Notes:
$(grep -A50 "^##.*Completed\|^###.*Completed" "$MEMORY_FILE" 2>/dev/null | head -30 || echo "  See memory/$YESTERDAY.md for details")

---

## 🍽️ Food Log ($YESTERDAY_DISPLAY)

See \`health/weight-food-log.md\` for detailed food log including:
- Meal breakdowns with estimated nutrition
- Calorie tracking
- Supplement timing

---

## 🔮 Tomorrow's Focus

$(grep -A10 "^##.*Next Actions\|^###.*Next" "$MEMORY_FILE" 2>/dev/null | head -15 || echo "  - Review pending TAT tasks")

---

*This summary is auto-generated from workspace data.*  
*Written by Clawson 🦞*  
*Part of the [Sam Clawson Research](https://samsclaw-byte.github.io/sam-clawson-research/) project*
EOF

# ========== GIT COMMIT & PUSH ==========

cd "$REPO_DIR"
git add daily-summaries/
git commit -m "Add daily summary for $YESTERDAY" 2>/dev/null || echo "Nothing new to commit"
git push origin master 2>&1

echo "✅ Daily summary created: $SUMMARY_FILE"
echo "🔗 View at: https://samsclaw-byte.github.io/sam-clawson-research/daily-summaries/$YESTERDAY-summary.md"
