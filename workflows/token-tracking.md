# Token Usage Tracking - Implementation Plan

## Objective
Include token usage breakdown in daily morning briefing

## Current Limitation
OpenClaw doesn't expose per-job token usage via API. The `cron` tool doesn't return token counts.

## Solution: Hybrid Approach

### Phase 1: Estimation (Immediate)
Use script-based estimation based on known cron schedules:
- `/home/samsclaw/.openclaw/workspace/scripts/token_estimate.sh`
- Calculates based on: job count × frequency × model cost
- Updated when cron jobs change

### Phase 2: Logging (Future)
When OpenClaw adds token logging:
- `/home/samsclaw/.openclaw/workspace/scripts/token_tracker.py`
- Real per-job tracking
- Historical analysis

## Morning Briefing Integration

The 6am briefing will now include:
```
📊 **Token Usage (Est. Last 24h):**
• Voice transcription (K1): ~28,800 tokens
• Reminders (K1): ~1,500 tokens  
• Overnight tasks (K2.5): ~16,000 tokens
• Main chat: ~5,000 tokens
• Total: ~51,000 tokens (~$4.50)
```

## Categories Tracked

| Category | Model | Runs/Day | Est. Tokens/Run |
|----------|-------|----------|-----------------|
| Voice transcription | K1 | 288 | 100 |
| Reminders (3×) | K1 | 3 | 500 |
| Overnight build | K2.5 | 4 | 2,000 |
| Overnight research | K2.5 | 4 | 2,000 |
| Blog check | K1 | 1 | 800 |
| Security check | K1 | 1 | 800 |
| Morning briefing | K2.5 | 1 | 3,000 |
| Main chat | K2.5 | Variable | - |

## Files

- Estimator: `scripts/token_estimate.sh`
- Tracker (future): `scripts/token_tracker.py`
- Documentation: `workflows/token-tracking.md`

---

*Last updated: 2026-02-05*
