#!/usr/bin/env python3
"""
Morning Brief Generator - Integrated WHOOP + Fitness + Tasks
Run daily at 6:00 AM to generate comprehensive morning briefing
Uses Airtable for all data sources
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from airtable_client import get_health_client, get_productivity_client

# Try to import WHOOP client
try:
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
    """Get Category 1 (Today) + overdue TAT tasks from Airtable"""
    try:
        client = get_productivity_client()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get urgent tasks from Airtable
        urgent_tasks = client.get_urgent_tat_tasks()
        
        tasks = []
        for task in urgent_tasks[:5]:  # Limit to top 5
            fields = task.get('fields', {})
            
            name = fields.get('Task Name', '')
            category = fields.get('Category', '')
            due_date = fields.get('Due Date', '')
            priority = fields.get('Priority', '')
            
            # Check if overdue
            is_overdue = due_date and due_date < today
            is_urgent = category == '1' or is_overdue
            
            if name and is_urgent:
                tasks.append({
                    'name': name,
                    'category': category,
                    'due_date': due_date,
                    'priority': priority,
                    'overdue': is_overdue
                })
        
        return tasks
        
    except Exception as e:
        print(f"⚠️ Error fetching TAT tasks: {e}")
        return []

def get_yesterday_health_summary():
    """Get yesterday's health summary from Airtable"""
    try:
        client = get_health_client()
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Get food entries - filter locally
        all_food = client.get_food_entries(days=2)
        food_entries = [f for f in all_food if f['fields'].get('Date') == yesterday]
        total_calories = sum(
            f['fields'].get('Calories', 0) or 0 
            for f in food_entries
        )
        
        # Get habits - filter locally
        habits = client.get_habits()
        yesterday_habits = [
            h for h in habits 
            if h['fields'].get('Date') == yesterday and h['fields'].get('Completed')
        ]
        
        # Get workouts - filter locally
        workouts = client.get_workouts(days=2)
        yesterday_workouts = [
            w for w in workouts 
            if w['fields'].get('Date') == yesterday
        ]
        
        return {
            'calories': total_calories,
            'habits_completed': len(yesterday_habits),
            'workouts': len(yesterday_workouts),
            'food_entries': len(food_entries)
        }
        
    except Exception as e:
        print(f"⚠️ Error fetching health summary: {e}")
        return None

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
            cat_display = "Today" if task['category'] == '1' else f"Cat {task['category']}"
            priority_emoji = {"🔥 Critical": "🔥", "⚡ High": "⚡", "📋 Medium": "📋", "💤 Low": "💤"}.get(task['priority'], "")
            print(f"  {overdue_marker}{priority_emoji} {task['name']} [{cat_display}]")
        print()
    else:
        print("\n✅ No urgent TAT tasks - you're all caught up!")
    
    # 2. Yesterday's Health Summary
    health_summary = get_yesterday_health_summary()
    if health_summary:
        print("\n📊 YESTERDAY'S HEALTH SUMMARY")
        print("-" * 40)
        print(f"  🍽️  Food entries: {health_summary['food_entries']}")
        print(f"  🔥 Calories: {health_summary['calories']}")
        print(f"  ✅ Habits completed: {health_summary['habits_completed']}")
        print(f"  💪 Workouts: {health_summary['workouts']}")
        print()
    
    # 3. WHOOP Data
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
    elif whoop_data['status'] == 'error':
        print(f"⚠️ WHOOP Error: {whoop_data.get('message', 'Unknown error')}")
    else:
        print(f"Recovery Score: {whoop_data.get('recovery_score', 'N/A')}%")
        print(f"Sleep Performance: {whoop_data.get('sleep_performance', 'N/A')}%")
        print(f"Status: {whoop_data.get('status', 'unknown').upper()}")
        print(f"\n📝 {whoop_data.get('message', '')}")
    
    # 4. Workout Recommendation
    print("\n🏋️ TODAY'S WORKOUT")
    print("-" * 40)
    
    workout = get_workout_recommendation(whoop_data, day_name)
    
    print(f"Recovery Zone: {workout['zone']}")
    print(f"Workout Type: {workout['type']}")
    print(f"Intensity: {workout['intensity']}")
    print(f"Focus: {workout['focus']}")
    print(f"Duration: {workout['duration']}")
    print(f"\n💡 Trainer Advice: {workout['advice']}")
    
    # 5. Sample workout (when WHOOP is configured)
    print("\n📋 SAMPLE WORKOUT OPTIONS")
    print("-" * 40)
    
    recovery_score = whoop_data.get('recovery_score') or 0
    if whoop_data.get('status') in ['green', 'excellent', 'good'] or recovery_score >= 67:
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
    
    # 6. Calf Warm-up (always required for hard days)
    if recovery_score >= 67:
        print("\n🦵 MANDATORY CALF WARM-UP (5-7 minutes)")
        print("-" * 40)
        print("  1. Ankle circles: 10 each direction per foot")
        print("  2. Calf raises (slow, no weight): 2x15")
        print("  3. Foam roll calves: 1 min each")
        print("  4. Dynamic leg swings: 10 each leg")
        print("  5. Test: 10 bodyweight calf raises - any pain?")
        print()
        print("  ⚠️ If pain during test: Switch to active recovery day")
    
    # 7. Daily Checklist
    print("\n✅ DAILY CHECKLIST")
    print("-" * 40)
    print("  [ ] Check WHOOP recovery score")
    print("  [ ] Complete calf warm-up (if hard workout)")
    print("  [ ] 30-min workout as recommended")
    print("  [ ] Log workout in Airtable")
    print("  [ ] Track meals with Clawson")
    print("  [ ] Hit water goal (8 glasses)")
    print("  [ ] Take multivitamin")
    
    # 8. Trainer's Corner
    print("\n💪 TRAINER'S CORNER")
    print("-" * 40)
    
    tips = [
        "Remember: Consistency > Intensity. Better to do 70% effort and come back tomorrow than 100% and get injured.",
        "If you feel calf tightness at ANY point, stop immediately and switch to upper body only.",
        "Sleep is your #1 recovery tool. With a newborn, prioritize sleep over workouts when needed.",
        "Track how you feel, not just numbers. Energy levels matter more than calories burned.",
        "Friday afternoons are your long session window - use them!",
        "Drink water before you feel thirsty. Dehydration hits performance before you notice.",
        "Protein within 30 minutes post-workout helps recovery. Keep a shake handy!"
    ]
    
    # Rotate tips based on day of week
    day_index = today.weekday()
    print(f"  💡 {tips[day_index % len(tips)]}")
    
    # 9. Upcoming Week Preview
    print("\n📅 THIS WEEK PREVIEW")
    print("-" * 40)
    
    # Calculate week dates
    week_start = today - timedelta(days=today.weekday())
    week_days = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_str = day.strftime('%a %d')
        # Simple alternating pattern
        if i % 2 == 0:
            week_days.append(f"  {day_str}: Hard workout")
        else:
            week_days.append(f"  {day_str}: Active recovery")
    
    for day_info in week_days:
        marker = ">>>" if day_name[:3] in day_info else "   "
        print(f"{marker} {day_info}")
    
    # 10. Save brief to file
    print("\n" + "=" * 60)
    
    brief_path = os.path.expanduser(f'~/.openclaw/workspace/research/morning-briefs/{date_str}-brief.md')
    os.makedirs(os.path.dirname(brief_path), exist_ok=True)
    
    # Save summary
    with open(brief_path, 'w') as f:
        f.write(f"# Morning Brief - {day_name}, {date_str}\n\n")
        
        if urgent_tasks:
            f.write(f"## 🔥 Urgent TAT Tasks\n")
            for task in urgent_tasks[:3]:
                f.write(f"- {task['name']}\n")
            f.write("\n")
        
        f.write(f"## WHOOP Recovery\n")
        f.write(f"- Recovery Score: {whoop_data.get('recovery_score', 'N/A')}%\n")
        f.write(f"- Zone: {workout['zone']}\n\n")
        
        f.write(f"## Workout Recommendation\n")
        f.write(f"- Type: {workout['type']}\n")
        f.write(f"- Focus: {workout['focus']}\n")
        f.write(f"- Advice: {workout['advice']}\n\n")
        
        if health_summary:
            f.write(f"## Yesterday's Stats\n")
            f.write(f"- Calories: {health_summary['calories']}\n")
            f.write(f"- Habits: {health_summary['habits_completed']}\n")
            f.write(f"- Workouts: {health_summary['workouts']}\n\n")
        
        f.write(f"## Trainer Tip\n")
        f.write(f"{tips[day_index % len(tips)]}\n")
    
    print(f"📄 Brief saved: {brief_path}")
    print("\nHave a great day! 💪🦞")
    
    return {
        'date': date_str,
        'urgent_tasks_count': len(urgent_tasks),
        'recovery_score': whoop_data.get('recovery_score'),
        'workout_type': workout['type'],
        'health_summary': health_summary
    }

if __name__ == "__main__":
    result = generate_morning_brief()
    
    # Output JSON for automation
    print(f"\n---JSON_RESULT---")
    print(json.dumps(result, indent=2, default=str))
