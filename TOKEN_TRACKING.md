# Token Usage Tracker

## Manual Tracking Template

| Date/Time | Task Category | Model | Tokens In | Tokens Out | Cost Est. |
|-----------|---------------|-------|-----------|------------|-----------|
| 2026-02-05 18:00 | Voice Check | kimi-k2.5 | 500 | 50 | $0.005 |
| 2026-02-05 18:15 | Chat | kimi-k2.5 | 2000 | 300 | $0.02 |

## Categories
- `voice-transcription` - Auto voice checks
- `reminder-check` - Scheduled reminders (8pm, 3pm, etc.)
- `overnight-build` - Build tasks (11pm, 1am, 3am, 5am)
- `overnight-research` - Research tasks (12am, 2am, 4am)
- `main-chat` - Your direct messages with me
- `security-research` - Security checks
- `blog-update` - Blog maintenance

## Cost Calculation (Kimi K2.5)
~ $0.01 per 1K input tokens
~ $0.03 per 1K output tokens

## Files
- Log file: `logs/token-usage-YYYY-MM-DD.md`
- Aggregator: `scripts/track_tokens.py` (to be created)
