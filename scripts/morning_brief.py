#!/usr/bin/env python3
"""
Morning Brief Generator - Integrated WHOOP + Fitness + Tasks
Run daily at 6:00 AM to generate comprehensive morning briefing
"""

import os
import json
from datetime import datetime, timedelta

# Try to import WHOOP client (will work once credentials are configured)
try:
    import sys
    sys.path.append(os.path.expanduser('~/.openclaw/workspace/skills/whoop-integration/scripts'))
    from whoop_client import WhoopClient
    WHOOP_AVAILABLE = True
except ImportError:
    WHOOP_AVAILABLE = False

def get_whoop_data():
    """Get WHOOP data if available"""
    if not WHOOP_AVAILABLE:
        return {
            'status': 'not_configured',
            'recovery_score': None,
            'sleep_performance': None,
            'message': 'WHOOP integration pending - add WHOOP_CLIENT_ID/SECRET to config'
        }
    
    try:
        client = WhoopClient()
        summary = client.get_sleep_performance_summary()
        return summary
    except Exception as e:
        return {
            'status': 'error',
            'recovery_score': None,
            'message': f'WHOOP error: {e}'
        }

def get_urgent_tat_tasks():
    """Get Category 1 (Today) + overdue TAT tasks from Notion"""
    try:
        import requests
        
        # Get Notion API key
        notion_key_path = os.path.expanduser('~/.config/notion/api_key')
        if not os.path.exists(notion_key_path):
            return []
        
        with open(notion_key_path, 'r') as f:
            notion_key = f.read().strip()
        
        # TAT Database ID
        db_id = "2fcf2cb1-2276-81d6-aebe-f388bdb09b8e"
        
        headers = {
            "Authorization": f"Bearer {notion_key}",
            "Notion-Version": "2025-09-03",
            "Content-Type": "application/json"
        }
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Query for Category 1 + overdue tasks
        # Filter: Category == "1" OR (Due Date exists AND Due Date < today)
        query = {
            "filter": {
                "or": [
                    {
                        "property": "Category",
                        "select": {
                            "equals": "1"
                        }
                    },
                    {
                        "and": [
                            {
                                "property": "Due Date",
                                "date": {
                                    "is_not_empty": True
                                }
                            },
                            {
                                "property": "Due Date",
                                "date": {
                                    "before": today
                                }
                            }
                        ]
                    }
                ]
            },
            "sorts": [
                {
                    "property": "Due Date",
                    "direction": "ascending"
                }
            ]
        }
        
        response = requests.post(
            f"https://api.notion.com/v1/databases/{db_id}/query",
            headers=headers,
            json=query
        )
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        tasks = []
        
        for page in data.get('results', [])[:5]:  # Limit to top 5
            props = page.get('properties', {})
            
            # Get task name
            name = ""
            if 'Task Name' in props:
                title_items = props['Task Name'].get('title', [])
                if title_items:
                    name = title_items[0].get('text', {}).get('content', '')
            
            # Get category
            category = props.get('Category', {}).get('select', {}).get('name', '')
            
            # Get due date
            due_date = props.get('Due Date', {}).get('date', {}).get('start', '')
            
            # Check if overdue
            is_overdue = False
            if due_date and due_date < today:
                is_overdue = True
            
            # Handle both old format (🔥 Today) and new format (1)
            is_urgent = category in ['1', '🔥 Today'] or is_overdue
            
            if name and is_urgent:
                tasks.append({
                    'name': name,
                    'category': category,
                    'due_date': due_date,
                    'overdue': is_overdue
                })
        
        return tasks
        
    except Exception as e:
        return []

def get_workout_recommendation(whoop_data, fitness_program_day):
    """
    Generate workout recommendation based on WHOOP recovery
    and fitness program schedule
    """
    recovery_score = whoop_data.get('recovery_score', 0) or 0
    
    # Recovery zones
    if recovery_score >= 67:
        zone = "🟢 GREEN"
        recommendation = {
            'type': 'HARD',
            'intensity': 'Full intensity workout',
            'focus': 'Strength or cardio as planned',
            'duration': '30-45 minutes',
            'advice': "Great recovery! Push yourself but maintain good form."
        }
    elif recovery_score >= 50:
        zone = "🟡 YELLOW"
        recommendation = {
            'type': 'ACTIVE RECOVERY',
            'intensity': 'Moderate effort',
            'focus': 'Swimming, easy bike, or light kettlebell flow',
            'duration': '20-30 minutes',
            'advice': "Moderate recovery. Keep it easy, focus on movement quality."
        }
    else:
        zone = "🔴 RED"
        recommendation = {
            'type': 'REST',
            'intensity': 'Complete rest or mobility only',
            'focus': '15-minute stretch/mobility or full rest day',
            'duration': '0-15 minutes',
            'advice': "Prioritize rest and sleep. Your body needs recovery."
        }
    
    recommendation['zone'] = zone
    recommendation['recovery_score'] = recovery_score
    
    return recommendation

def generate_morning_brief():
    """Generate complete morning brief"""
    
    today = datetime.now()
    day_name = today.strftime('%A')
    date_str = today.strftime('%Y-%m-%d')
    
    print("=" * 60)
    print(f"🌅 GOOD MORNING SAM - {day_name}, {date_str}")
    print("=" * 60)
    
    # 1. URGENT TAT TASKS (NEW - Category 1 + overdue)
    urgent_tasks = get_urgent_tat_tasks()
    if urgent_tasks:
        print("\n🔥 URGENT TAT TASKS (Today + Overdue)")
        print("-" * 40)
        for task in urgent_tasks[:5]:  # Show top 5
            overdue_marker = "⚠️ OVERDUE: " if task['overdue'] else "• "
            cat_display = "Today" if task['category'] in ['1', '🔥 Today'] else f"Cat {task['category']}"
            print(f"  {overdue_marker}{task['name']} [{cat_display}]")
        print()
    
    # 2. WHOOP Data
    print("\n💓 WHOOP RECOVERY STATUS")
    print("-" * 40)
    
    whoop_data = get_whoop_data()
    
    if whoop_data['status'] == 'not_configured':
        print("⏳ WHOOP integration pending")
        print("   Add WHOOP_CLIENT_ID and WHOOP_CLIENT_SECRET to:")
        print("   ~/.openclaw/openclaw.json (skills.entries.whoop-integration)")
        print("\n   Once configured, this will show:")
        print("   • Recovery score (Green/Yellow/Red)")
        print("   • Sleep performance")
        print("   • HRV and resting heart rate")
    else:
        print(f"Recovery Score: {whoop_data.get('recovery_score', 'N/A')}")
        print(f"Sleep Performance: {whoop_data.get('sleep_performance', 'N/A')}%")
        print(f"Status: {whoop_data.get('status', 'unknown').upper()}")
        print(f"\n📝 {whoop_data.get('message', '')}")
    
    # 2. Workout Recommendation
    print("\n🏋️ TODAY'S WORKOUT")
    print("-" * 40)
    
    workout = get_workout_recommendation(whoop_data, day_name)
    
    print(f"Recovery Zone: {workout['zone']}")
    print(f"Workout Type: {workout['type']}")
    print(f"Intensity: {workout['intensity']}")
    print(f"Focus: {workout['focus']}")
    print(f"Duration: {workout['duration']}")
    print(f"\n💡 Trainer Advice: {workout['advice']}")
    
    # 3. Sample workout (when WHOOP is configured)
    print("\n📋 SAMPLE WORKOUT OPTIONS")
    print("-" * 40)
    
    if whoop_data.get('status') in ['green', 'excellent', 'good']:
        print("HARD DAY Options:")
        print("  • Kettlebell Circuit A (20 min)")
        print("    - Goblet squats: 3x10")
        print("    - Kettlebell swings: 3x15")
        print("    - Rows: 3x12 each arm")
        print("    - Overhead press: 3x8")
        print("    - Calf raises (slow): 3x15")
        print()
        print("  • OR Gym Session (if accessible)")
        print("  • OR Swimming (25m pool, 30 min)")
    else:
        print("ACTIVE RECOVERY Options:")
        print("  • Swimming - easy laps (20-30 min)")
        print("  • Static bike - easy pace (20 min)")
        print("  • Walk in park - leisurely (20-30 min)")
        print("  • Yoga/Stretching - gentle flow (15 min)")
    
    # 4. Calf Warm-up (always required for hard days)
    if whoop_data.get('recovery_score', 0) and whoop_data['recovery_score'] >= 67:
        print("\n🦵 MANDATORY CALF WARM-UP (5-7 minutes)")
        print("-" * 40)
        print("  1. Ankle circles: 10 each direction per foot")
        print("  2. Calf raises (slow, no weight): 2x15")
        print("  3. Foam roll calves: 1 min each")
        print("  4. Dynamic leg swings: 10 each leg")
        print("  5. Test: 10 bodyweight calf raises - any pain?")
        print()
        print("  ⚠️ If pain during test: Switch to active recovery day")
    
    # 5. Daily Checklist
    print("\n✅ DAILY CHECKLIST")
    print("-" * 40)
    print("  [ ] Check WHOOP recovery score")
    print("  [ ] Complete calf warm-up (if hard workout)")
    print("  [ ] 30-min workout as recommended")
    print("  [ ] Log workout in Notion")
    print("  [ ] Track meals with Clawson")
    print("  [ ] Hit water goal (8 glasses)")
    print("  [ ] Take multivitamin")
    
    # 6. Trainer's Corner
    print("\n💪 TRAINER'S CORNER")
    print("-" * 40)
    
    tips = [
        "Remember: Consistency > Intensity. Better to do 70% effort and come back tomorrow than 100% and get injured.",
        "If you feel calf tightness at ANY point, stop immediately and switch to upper body only.",
        "Sleep is your #1 recovery tool. With a newborn, prioritize sleep over workouts when needed.",
        "Track how you feel, not just numbers. Energy levels matter more than calories burned.",
        "Friday afternoons are your long session window - use them!"
    ]
    
    # Rotate tips based on day of week
    day_index = today.weekday()
    print(f"  💡 {tips[day_index % len(tips)]}")
    
    # 7. Upcoming Events (when configured)
    print("\n📅 THIS WEEK")
    print("-" * 40)
    
    # Calculate week dates
    week_start = today - timedelta(days=today.weekday())
    week_days = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_str = day.strftime('%a %d')
        # Simple alternating pattern for demo
        if i % 2 == 0:
            week_days.append(f"  {day_str}: Hard workout")
        else:
            week_days.append(f"  {day_str}: Active recovery")
    
    for day_info in week_days:
        marker = ">>>" if day_name[:3] in day_info else "   "
        print(f"{marker} {day_info}")
    
    # 8. Save brief to file
    print("\n" + "=" * 60)
    
    brief_path = os.path.expanduser(f'~/.openclaw/workspace/research/morning-briefs/{date_str}-brief.md')
    os.makedirs(os.path.dirname(brief_path), exist_ok=True)
    
    # Save summary (actual file writing would include all sections)
    with open(brief_path, 'w') as f:
        f.write(f"# Morning Brief - {day_name}, {date_str}\n\n")
        f.write(f"## WHOOP Recovery\n")
        f.write(f"- Recovery Score: {whoop_data.get('recovery_score', 'N/A')}\n")
        f.write(f"- Zone: {workout['zone']}\n\n")
        f.write(f"## Workout Recommendation\n")
        f.write(f"- Type: {workout['type']}\n")
        f.write(f"- Focus: {workout['focus']}\n")
        f.write(f"- Advice: {workout['advice']}\n\n")
        f.write(f"## Trainer Tip\n")
        f.write(f"{tips[day_index % len(tips)]}\n")
    
    print(f"📄 Brief saved: {brief_path}")
    print("\nHave a great day! 💪🦞")

if __name__ == "__main__":
    generate_morning_brief()
