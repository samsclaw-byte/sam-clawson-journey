#!/usr/bin/env python3
"""
Log exercise to D1
Usage: python3 log_exercise.py <workout_type> [duration] [strain]
Example: python3 log_exercise.py Swimming 23 9.7
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def main():
    client = D1Client()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if len(sys.argv) < 2:
        print("Usage: log_exercise.py <workout_type> [duration] [strain]")
        print("Example: log_exercise.py Swimming 23 9.7")
        sys.exit(1)
    
    workout_type = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else None
    strain = float(sys.argv[3]) if len(sys.argv) > 3 else None
    
    result = client.create_exercise(
        date=today,
        workout_type=workout_type,
        duration_minutes=duration,
        strain=strain
    )
    
    if result.get('success'):
        print(f"✅ Logged: {workout_type} ({duration} min, strain {strain or 'N/A'})")
    else:
        print(f"❌ Failed: {result.get('error')}")

if __name__ == "__main__":
    main()
