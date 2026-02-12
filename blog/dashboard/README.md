# 🏃‍♀️ Health Dashboard

Interactive WHOOP + Nutrition analytics dashboard using Streamlit.

## 📁 Files

| File | Purpose |
|------|---------|
| `sync_whoop.py` | Sync WHOOP data to CSV |
| `health_dashboard.py` | Streamlit dashboard app |
| `run_dashboard.sh` | One-command setup & launch |
| `whoop_data.csv` | Exported WHOOP data (auto-generated) |

## 🚀 Quick Start

### Option 1: One Command (Recommended)

```bash
cd ~/.openclaw/workspace/dashboard
./run_dashboard.sh
```

This will:
1. Install dependencies (streamlit, pandas, plotly)
2. Sync latest WHOOP data
3. Start dashboard at http://localhost:8501

### Option 2: Manual Steps

```bash
# 1. Install dependencies
pip install streamlit pandas plotly

# 2. Sync WHOOP data
cd ~/.openclaw/workspace/dashboard
python3 sync_whoop.py

# 3. Run dashboard
streamlit run health_dashboard.py
```

## 📊 Dashboard Features

### Visualizations
- **Recovery Trend** - Line chart with good/poor thresholds
- **Sleep Performance** - Color-coded bar chart
- **Sleep Stages** - Stacked area chart (Deep/REM/Light/Awake)
- **Strain vs Recovery** - Scatter plot with trendline
- **HRV Trend** - Heart rate variability over time
- **Resting HR** - Resting heart rate trends

### Filters
- Date range selector
- Interactive charts (hover for details)
- Export to CSV

### Data Sources
- WHOOP API (recovery, sleep, strain, HRV, RHR)
- Nutrition data (placeholder - add when Edamam ready)

## 🔄 Updating Data

### Manual Update
```bash
cd ~/.openclaw/workspace/dashboard
python3 sync_whoop.py
```

### Auto-Update (Optional)
Add to crontab to sync daily:
```bash
0 6 * * * cd ~/.openclaw/workspace/dashboard && python3 sync_whoop.py
```

## 📈 Future Enhancements

When Edamam nutrition API is ready:
1. Add `sync_nutrition.py` script
2. Merge nutrition data in dashboard
3. Add visualizations:
   - Calories In vs Out
   - Macro breakdown (protein/carbs/fat)
   - Nutrition correlation with recovery

## 🔧 Troubleshooting

**"Module not found" error:**
```bash
pip install streamlit pandas plotly
```

**"No data found" error:**
```bash
python3 sync_whoop.py
```

**Dashboard won't open:**
- Check if port 8501 is available
- Try: `streamlit run health_dashboard.py --server.port 8502`

## 📱 Accessing Dashboard

Once running, open browser:
```
http://localhost:8501
```

Or share on network (if needed):
```bash
streamlit run health_dashboard.py --server.address 0.0.0.0
```

---

**Built with:** Streamlit + Plotly + Pandas 🦞
