#!/usr/bin/env python3
"""
Water Tracker - Daily hydration goal with reminders
"""

import json
import os
from datetime import datetime, date

STATE_FILE = "/home/samsclaw/.openclaw/workspace/data/water_tracker.json"

def load_state():
    """Load today's water tracking state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            data = json.load(f)
            # Reset if it's a new day
            if data.get('date') != str(date.today()):
                return new_day()
            return data
    return new_day()

def new_day():
    """Initialize new day."""
    return {
        'date': str(date.today()),
        'glasses': 0,
        'goal': 8,  # Default 8 glasses
        'log': []
    }

def save_state(state):
    """Save state to file."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def add_water(glasses=1):
    """Add water intake."""
    state = load_state()
    state['glasses'] += glasses
    state['log'].append({
        'time': datetime.now().isoformat(),
        'glasses': glasses
    })
    save_state(state)
    return state

def get_status():
    """Get current hydration status."""
    state = load_state()
    remaining = max(0, state['goal'] - state['glasses'])
    progress = (state['glasses'] / state['goal']) * 100
    return state, remaining, progress

def format_status():
    """Format status for display."""
    state, remaining, progress = get_status()
    bar_length = 10
    filled = int((progress / 100) * bar_length)
    bar = '💧' * filled + '⚪' * (bar_length - filled)
    
    return f"""💧 **Water Tracker**
{bar} {state['glasses']}/{state['goal']} glasses ({progress:.0f}%)

**Today's Log:**
""" + "\n".join([
        f"  {entry['time'][11:16]} - +{entry['glasses']} glass{'es' if entry['glasses'] > 1 else ''}"
        for entry in state['log'][-5:]  # Last 5 entries
    ]) + (f"\n\n🎯 {remaining} more to reach your goal!" if remaining > 0 else "\n\n✅ Goal reached! Great job!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        print(format_status())
    elif len(sys.argv) > 1 and sys.argv[1] == 'add':
        glasses = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        state = add_water(glasses)
        print(f"✅ Added {glasses} glass(es)!")
        print(format_status())
    else:
        print(format_status())
