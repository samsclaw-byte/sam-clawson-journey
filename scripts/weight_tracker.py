#!/usr/bin/env python3
"""
Weight Tracker - Daily weight logging with trend analysis
"""

import json
import os
from datetime import datetime, date

STATE_FILE = "/home/samsclaw/.openclaw/workspace/data/weight_tracker.json"

def load_data():
    """Load weight tracking data."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"entries": [], "goal": None}

def save_data(data):
    """Save weight data."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def log_weight(weight_kg, notes=""):
    """Log a new weight entry."""
    data = load_data()
    entry = {
        "date": str(date.today()),
        "datetime": datetime.now().isoformat(),
        "weight_kg": round(float(weight_kg), 1),
        "weight_lbs": round(float(weight_kg) * 2.20462, 1),
        "notes": notes
    }
    data["entries"].append(entry)
    save_data(data)
    return entry, data

def get_latest(data=None):
    """Get latest weight entry."""
    if data is None:
        data = load_data()
    if not data["entries"]:
        return None
    return data["entries"][-1]

def get_trend(data=None, days=7):
    """Get weight trend over last N days."""
    if data is None:
        data = load_data()
    
    entries = data["entries"][-days:]
    if len(entries) < 2:
        return None
    
    first = entries[0]["weight_kg"]
    last = entries[-1]["weight_kg"]
    change = round(last - first, 1)
    
    return {
        "days": len(entries),
        "change_kg": change,
        "change_lbs": round(change * 2.20462, 1),
        "direction": "down" if change < 0 else "up" if change > 0 else "stable"
    }

def format_status():
    """Format weight status."""
    data = load_data()
    latest = get_latest(data)
    
    if not latest:
        return "📊 No weight data yet. Log your first entry!"
    
    trend = get_trend(data)
    goal = data.get("goal")
    
    lines = [
        f"⚖️ **Weight Check-in**",
        f"",
        f"**Today:** {latest['weight_kg']} kg ({latest['weight_lbs']} lbs)"
    ]
    
    if len(data["entries"]) > 1:
        prev = data["entries"][-2]
        change = round(latest['weight_kg'] - prev['weight_kg'], 1)
        if change != 0:
            direction = "📉" if change < 0 else "📈"
            lines.append(f"**Change:** {direction} {abs(change)} kg from yesterday")
    
    if trend:
        emoji = "📉" if trend["direction"] == "down" else "📈" if trend["direction"] == "up" else "➡️"
        lines.append(f"**7-day trend:** {emoji} {abs(trend['change_kg'])} kg {trend['direction']}")
    
    if goal:
        diff = round(latest['weight_kg'] - goal, 1)
        if diff > 0:
            lines.append(f"**Goal:** {goal} kg ({diff} kg to go)")
        else:
            lines.append(f"**Goal:** {goal} kg (✅ {abs(diff)} kg below!)")
    
    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'log':
        weight = sys.argv[2]
        notes = sys.argv[3] if len(sys.argv) > 3 else ""
        entry, data = log_weight(weight, notes)
        print(f"✅ Logged: {entry['weight_kg']} kg")
        print(format_status())
    elif len(sys.argv) > 1 and sys.argv[1] == 'status':
        print(format_status())
    elif len(sys.argv) > 1 and sys.argv[1] == 'goal':
        goal = float(sys.argv[2])
        data = load_data()
        data["goal"] = goal
        save_data(data)
        print(f"🎯 Goal set: {goal} kg")
    else:
        print(format_status())
