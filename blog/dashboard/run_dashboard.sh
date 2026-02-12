#!/bin/bash
# Setup script for Health Dashboard

echo "🏃‍♀️ Setting up Health Dashboard..."
echo "================================"

# Install required packages
echo "📦 Installing dependencies..."
pip install streamlit pandas plotly -q

# Sync WHOOP data
echo "🔄 Syncing WHOOP data..."
cd ~/.openclaw/workspace/dashboard
python3 sync_whoop.py

# Start dashboard
echo ""
echo "🚀 Starting dashboard..."
echo "Opening browser at http://localhost:8501"
echo ""
streamlit run health_dashboard.py
