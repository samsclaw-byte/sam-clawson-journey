# Voice Message Workflow

## Current Status (2026-02-05)
✅ Local Whisper installed and working
✅ Can transcribe manually via: `/home/samsclaw/.miniforge/envs/whisper/bin/whisper`
❌ Not yet automatic — requires manual trigger

## Manual Process (Working Now)
```bash
# When user sends voice message:
export PATH="/home/samsclaw/.miniforge/envs/whisper/bin:$PATH"
whisper <audio-file.ogg> --model base --output_format txt
```

## Tools Required
- **Whisper**: `/home/samsclaw/.miniforge/envs/whisper/bin/whisper`
- **Model**: base (74MB, downloaded)
- **Conda env**: `/home/samsclaw/.miniforge/envs/whisper/`

## Auto-Integration Needed
To make this automatic:
1. Hook into Telegram voice message reception
2. Auto-run transcription on .ogg files
3. Inject transcript into session context
4. Enable normal response flow

## File Locations
- Voice messages: `/home/samsclaw/.openclaw/media/inbound/`
- Transcription script: `/home/samsclaw/.openclaw/workspace/skills/voice-transcribe/transcribe_voice.py`
- Whisper binary: `/home/samsclaw/.miniforge/envs/whisper/bin/whisper`

## Usage Commands
```bash
# Direct whisper usage
/home/samsclaw/.miniforge/envs/whisper/bin/whisper <file.ogg> --model base

# Via conda env
conda run -n whisper whisper <file.ogg> --model base
```
