# Migration Plan: WSL → Native Windows with RTX 4070 GPU

**Target Machine:** Sam's Laptop (Windows 11, RTX 4070, 16GB+ RAM)  
**Current Setup:** WSL2 Ubuntu on Intel i5-1235U (no GPU)  
**Migration Window:** Planned for [TBD - Weekend recommended]  
**Estimated Downtime:** 4-6 hours

---

## 🎯 Migration Goals

1. **GPU Acceleration:** Enable CUDA for Whisper (10-20x transcription speed)
2. **Better Performance:** Native Windows + GPU for local ML tasks
3. **Maintain Functionality:** All current systems (cron, Notion, Telegram) working
4. **Seamless Transition:** Minimal disruption to daily workflow

---

## 📋 Pre-Migration Checklist

### Before Moving:
- [ ] Export all critical data from WSL:
  - Git repos (workspace, blog, research)
  - Configuration files (openclaw.json, crontab, .env files)
  - Notion API key, Telegram bot token
  - WHOOP credentials (secure)
- [ ] Document current OpenClaw version and installed skills
- [ ] Test OpenClaw on target machine (basic install)
- [ ] Schedule downtime (weekend morning recommended)

### Target Machine Prep:
- [ ] Windows 11 updated
- [ ] NVIDIA drivers installed (latest)
- [ ] CUDA Toolkit installed (12.x)
- [ ] Python 3.12 installed (via Windows Store or python.org)
- [ ] Git for Windows installed
- [ ] VS Code (optional, for editing)

---

## 🔧 Migration Steps

### Phase 1: Backup & Export (30 min)

```bash
# On WSL - Create migration archive
cd ~
tar -czf openclaw-migration-$(date +%Y%m%d).tar.gz \
  .openclaw/ \
  .npm-global/ \
  .miniforge/ \
  .config/notion/ \
  .config/whoop/ \
  .gitconfig \
  .ssh/ 2>/dev/null

# Export crontab
crontab -l > ~/crontab-backup.txt

# Export environment variables
env | grep -E "OPENCLAW|NOTION|TELEGRAM|PATH" > ~/env-backup.txt
```

### Phase 2: Target Machine Setup (1 hour)

**1. Install Prerequisites:**
```powershell
# As Administrator on Windows
# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install tools
choco install git python nodejs-lts ffmpeg cuda -y
```

**2. Install OpenClaw:**
```powershell
# Install OpenClaw globally
npm install -g openclaw

# Verify
openclaw --version
```

**3. Configure GPU for Whisper:**
```powershell
# Create Python environment
python -m venv C:\Users\Sam\.whisper-env
C:\Users\Sam\.whisper-env\Scripts\activate

# Install Whisper with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install openai-whisper

# Verify CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Phase 3: Restore Configuration (1 hour)

**1. Restore OpenClaw Config:**
```powershell
# Copy from WSL backup
# Extract .openclaw folder to C:\Users\Sam\.openclaw\

# Update paths in openclaw.json (WSL paths → Windows paths)
# /home/samsclaw/ → C:/Users/Sam/
```

**2. Restore Crontab:**
```powershell
# Windows uses Task Scheduler instead of crontab
# Create scheduled tasks or use OpenClaw's built-in scheduler
# Option: Use WSL cron or switch to Task Scheduler
```

**3. Restore Skills & Scripts:**
```powershell
# Copy workspace folder
# Re-install any custom skills
openclaw skills install notion
openclaw skills install local-whisper
```

### Phase 4: Testing & Validation (2 hours)

- [ ] OpenClaw gateway starts successfully
- [ ] Telegram bot responds
- [ ] Notion integration works
- [ ] Cron jobs running (or Task Scheduler equivalents)
- [ ] Voice transcription with GPU:
  ```powershell
  whisper test-audio.ogg --model base --device cuda
  ```
- [ ] WHOOP integration works

### Phase 5: Optimize GPU Performance (1 hour)

**Whisper Configuration:**
```json
// .openclaw/config/whisper.json
{
  "model": "base",
  "device": "cuda",
  "fp16": true,
  "language": "en"
}
```

**Expected Performance:**
- 3-minute voice note: ~10-20 seconds (vs 3-5 minutes on CPU)
- Can use larger models (small, medium) for better accuracy
- Real-time transcription possible for short clips

---

## 🔄 Alternative: Hybrid Approach

**Keep WSL for OpenClaw, use Windows GPU for transcription:**

```powershell
# On Windows - Expose GPU Whisper as HTTP service
# WSL can call Windows GPU via localhost

# Windows side (PowerShell):
# Run whisper as service that accepts files via API
```

**Pros:**
- No migration needed
- Get GPU transcription speed
- Keep working Linux environment

**Cons:**
- More complex setup
- Cross-OS communication overhead

---

## 🚨 Rollback Plan

If migration fails:
1. Keep WSL environment running (don't delete!)
2. Can switch back in 30 minutes
3. Re-export any new data from Windows back to WSL
4. Update Telegram bot webhook if needed

---

## 📊 Performance Comparison

| Task | WSL (CPU) | Windows (GPU) | Speedup |
|------|-----------|---------------|---------|
| Whisper Tiny (3 min audio) | 3-5 min | 10-20 sec | 10-20x |
| Whisper Base (3 min audio) | 5-8 min | 15-30 sec | 15-20x |
| Whisper Small (3 min audio) | N/A (too slow) | 30-60 sec | N/A |
| Token usage tracking | Same | Same | - |
| Cron jobs | Linux cron | Task Scheduler | - |

---

## ⏰ Recommended Timeline

**Weekend Migration (Saturday morning):**
- 09:00 - Backup & export
- 09:30 - Windows setup & OpenClaw install
- 10:30 - Restore config
- 11:30 - Testing
- 12:30 - Lunch break
- 13:30 - GPU optimization
- 14:30 - Final validation
- 15:00 - Done! 🎉

**Backup Plan:**
If issues arise, abort by 12:00, revert to WSL, try again next weekend.

---

## ✅ DECISION MADE: OPTION A - FULL MIGRATION

**Selected:** February 7, 2026  
**Rationale:** 10-20x transcription speed, clean modern setup, aligns with co-development vision

---

## 🚦 Pre-Migration Status

| Step | Status |
|------|--------|
| Decision made | ✅ Complete |
| Backup plan created | ✅ Complete |
| Migration guide written | ✅ Complete |
| Schedule migration date | ⏳ Pending |
| Execute migration | ⏳ Pending |

---

## 📋 Alternative Options (Not Selected)

**Option B: Hybrid** (Safer)
- Keep WSL for OpenClaw
- Use Windows GPU only for Whisper
- No migration risk
- Slightly more complex
- *Not selected — want full GPU integration*

**Option C: Status Quo**
- Stay on WSL (no GPU)
- Wait for better WSL GPU support (maybe never)
- Continue slow transcription
- *Not selected — transcription speed critical for workflow*

---

**Next Steps:**
1. Decide which option (A, B, or C)
2. Schedule migration date
3. Create full backup
4. Execute plan

*Prepared by Clawson 🦞*  
*Date: February 7, 2026*
