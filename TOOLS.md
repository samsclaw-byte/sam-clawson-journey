# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Workflows (Saved in `/workflows/`)

Documented processes for complex tasks:

### Voice Transcription
- **Manual**: Run `/home/samsclaw/.openclaw/workspace/scripts/auto-transcribe.sh <file.ogg>`
- **Auto**: Cron job runs every 2 minutes
- **Tools**: Whisper (conda env), ffmpeg
- **See**: `workflows/voice-transcription.md`

### Habit Tracking (Natural Language)
- **Usage**: Just mention habits in chat
- **Examples**: "Drank 2 waters" | "30 min run" | "Took vitamins"
- **Parser**: `/home/samsclaw/.openclaw/workspace/scripts/habit_parser.py`
- **See**: `workflows/habit-tracking.md`

---

Add whatever helps you do your job. This is your cheat sheet.
