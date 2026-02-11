# Edamam Nutrition API Integration

**Status:** Setup scripts ready — awaiting API credentials

## Quick Start

### Step 1: Get Free API Key (5 minutes)
1. Go to: https://developer.edamam.com/
2. Click "Sign Up" (free developer account)
3. Navigate to "Nutrition Analysis API"
4. Create a new application
5. Copy your **App ID** and **API Key**

**Free tier includes:**
- 2,000 API calls/month
- Full nutrition database
- No credit card required

### Step 2: Run Setup Script
```bash
cd /home/samsclaw/.openclaw/workspace/scripts
./setup-edamam.sh
```

Enter your App ID and API Key when prompted.

**Security:** Credentials stored in `~/.config/edamam/` with 600 permissions (owner read/write only)

### Step 3: Test Integration
```bash
./edamam-nutrition.sh "1 cup rice"
```

**Expected output:**
```
🔍 Analyzing: 1 cup rice
📊 Results:
  Calories: 200 kcal
  Protein: 4g
  Carbs: 45g
  Fat: 0.5g
```

---

## How It Works

### Current Workflow (Manual)
1. You tell me: "Ate pasta bolognese"
2. I estimate: ~1,100 cal, ~35g protein
3. I update Notion with estimates

### New Workflow (Edamam API)
1. You tell me: "Ate pasta bolognese"
2. I query Edamam API with exact description
3. Get precise nutrition data from database
4. Update Notion with accurate values

### Benefits
✅ **Accuracy** — Real nutrition data, not estimates  
✅ **Consistency** — Same portion sizes every time  
✅ **Speed** — Instant lookup  
✅ **Flexibility** — Handles complex meals, ingredients, brands  

---

## Usage Examples

### Simple Foods
```bash
./edamam-nutrition.sh "1 banana"
./edamam-nutrition.sh "2 eggs scrambled"
./edamam-nutrition.sh "grilled chicken breast 150g"
```

### Complex Meals
```bash
./edamam-nutrition.sh "pasta bolognese with beef and tomato sauce"
./edamam-nutrition.sh "ham and cheese sandwich on multigrain bread"
```

### With Portions
```bash
./edamam-nutrition.sh "1 cup cooked rice"
./edamam-nutrition.sh "200g salmon fillet"
```

---

## Integration with Notion

Once setup is complete:

**Option A: Real-time (Manual)**
- You send food photo/description
- I query Edamam API
- Get accurate nutrition
- Update Notion Food Log

**Option B: Daily Batch (Automated)**
- 11pm cron job reviews day's food log
- Queries Edamam for each meal
- Updates all entries with precise data
- Calculates daily totals

**Recommended:** Start with Option A (real-time), migrate to Option B after calibration.

---

## Next Steps

1. **Get API credentials** (link above)
2. **Run setup script**: `./setup-edamam.sh`
3. **Test with breakfast tomorrow**
4. **Compare**: My estimate vs. Edamam data
5. **Calibrate**: Adjust portion sizes based on accuracy

---

## API Limits

- **Free tier:** 2,000 calls/month
- **Your usage:** ~5-10 meals/day = ~150-300 calls/month
- **Headroom:** 85% unused capacity

If you exceed free tier: $0.001/call (very affordable)

---

**Ready when you are!** Get those API credentials and we'll have precise nutrition tracking today 🎉
