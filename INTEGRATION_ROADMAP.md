# Integration Roadmap - WHOOP & Nutrition

## Priority 1: WHOOP Integration

### What's Ready:
- ✅ Skills installed (`whoop`, `whoop-integration`)
- ✅ Security infrastructure (`~/.config/whoop/` with 600/700 permissions)
- ✅ Setup script created
- ✅ Documentation complete

### What You Need (At Laptop):
1. **WHOOP Developer Account** (10 min)
   - https://developer.whoop.com/
   - Create app: "Sam-Clawson-Assistant"
   - Set redirect: `https://localhost:3000/callback`
   - Save: CLIENT_ID, CLIENT_SECRET

2. **Add Credentials** (5 min)
   ```bash
   nano ~/.config/whoop/credentials
   # Add your actual CLIENT_ID and CLIENT_SECRET
   ```

3. **OAuth Authorization** (5 min)
   ```bash
   cd ~/.openclaw/workspace/skills/whoop
   node bin/whoop-auth --redirect-uri https://localhost:3000/callback
   # Follow prompts, authorize on phone, paste code
   ```

4. **Test** (2 min)
   ```bash
   node bin/whoop-morning
   # Should output your recovery/sleep data
   ```

**Time Required:** ~20 minutes
**Benefit:** Daily morning reports with recovery, sleep, strain, HRV, calories burned

---

## Priority 2: Nutrition API (Edamam)

### What's Ready:
- ✅ Food logging started (text-based estimates)
- ✅ Health log file created

### What You Need:
1. **Edamam Account** (5 min)
   - https://developer.edamam.com/
   - Sign up for free tier (2,000 API calls/month)
   - Get: APP_ID and APP_KEY

2. **Store Credentials Securely** (2 min)
   ```bash
   mkdir -p ~/.config/nutrition
   chmod 700 ~/.config/nutrition
   echo "EDAMAM_APP_ID=your_id" > ~/.config/nutrition/credentials
   echo "EDAMAM_APP_KEY=your_key" >> ~/.config/nutrition/credentials
   chmod 600 ~/.config/nutrition/credentials
   ```

3. **Test Integration** (3 min)
   - Send me a food item
   - I'll query Edamam API
   - Get: calories, protein, carbs, fat, fiber, sugar

**Time Required:** ~10 minutes
**Benefit:** Accurate nutrition data instead of estimates

---

## Integration Flow (Once Both Ready)

### Morning (6am):
1. WHOOP fetches: recovery, sleep, strain, calories burned yesterday
2. Notion food log: calories consumed yesterday
3. Calculate: net calorie deficit/surplus
4. Report: "Yesterday you burned 3,200 cal and consumed 2,400 cal = 800 cal deficit"

### Real-time Food Logging:
1. You text: "Lunch: grilled chicken sandwich"
2. I query Edamam API
3. Get precise nutrition data
4. Log to Notion
5. Reply: "✅ 485 cal | 35g protein | 42g carbs | 12g fat"

### Weekly Reports:
- Average daily calories in/out
- Macro breakdown trends
- Weight change correlation
- WHOOP recovery patterns

---

## Recommendation

**Do WHOOP first** (bigger impact, more data sources)
**Then Edamam** (refines accuracy)

**Timeline:**
- **Today (if time):** WHOOP setup (20 min)
- **Tomorrow:** Edamam setup (10 min)
- **Sunday:** First integrated weekly report

---

## Current Status

**Without integrations:**
- Food estimates (±30% accuracy)
- Exercise logged manually
- Weight tracked
- No calorie burn data

**With both integrations:**
- Precise nutrition (Edamam database)
- Accurate calorie burn (WHOOP)
- Recovery insights (WHOOP)
- Net calorie tracking (automated)
- Weekly trend analysis

**Ready when you are!** 🦞💪
