#!/usr/bin/env python3
"""
Log nutrition to D1
Usage: python3 log_nutrition.py <meal_type> <description> [calories]
Example: python3 log_nutrition.py breakfast "Eggs and toast" 400
"""

import sys
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def main():
    client = D1Client()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if len(sys.argv) < 3:
        print("Usage: log_nutrition.py <meal_type> <description> [calories]")
        print("Example: log_nutrition.py breakfast 'Eggs and toast' 400")
        sys.exit(1)
    
    meal_type = sys.argv[1]
    description = sys.argv[2]
    calories = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    result = client.create_nutrition(
        date=today,
        meal_type=meal_type,
        description=description,
        calories=calories,
        source='manual'
    )
    
    if result.get('success'):
        print(f"✅ Logged: {meal_type} - {description} ({calories or 'N/A'} cal)")
    else:
        print(f"❌ Failed: {result.get('error')}")

if __name__ == "__main__":
    main()
