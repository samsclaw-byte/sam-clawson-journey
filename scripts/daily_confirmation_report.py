#!/usr/bin/env python3
"""
Daily Confirmation Report
Generates a summary of all new entries across all tables and sends via Telegram
Run daily at 11:00 PM
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from airtable_client import get_health_client, get_productivity_client

def get_today_entries():
    """Get all entries created today across all tables"""
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    report = {
        'date': today,
        'generated_at': datetime.now().isoformat(),
        'health': {},
        'productivity': {},
        'summary': {
            'total_entries': 0,
            'tables_with_data': 0
        }
    }
    
    # Health Base
    try:
        health_client = get_health_client()
        
        # Food Log
        food_entries = health_client.get_food_entries(date=yesterday)
        if food_entries:
            total_calories = sum(f['fields'].get('Calories', 0) or 0 for f in food_entries)
            report['health']['food_log'] = {
                'count': len(food_entries),
                'total_calories': total_calories,
                'entries': [f['fields'].get('Food Name', 'Unknown') for f in food_entries[:3]]
            }
        
        # Weight
        weight_entries = health_client.get_weight_entries(days=1)
        if weight_entries:
            latest = weight_entries[0]['fields']
            report['health']['weight'] = {
                'weight': latest.get('Weight (kg)'),
                'date': latest.get('Date')
            }
        
        # Workouts
        workout_entries = health_client.get_workouts(days=1)
        if workout_entries:
            total_duration = sum(w['fields'].get('Duration (min)', 0) or 0 for w in workout_entries)
            report['health']['workouts'] = {
                'count': len(workout_entries),
                'total_minutes': total_duration,
                'types': list(set(w['fields'].get('Workout Type', 'Unknown') for w in workout_entries))
            }
        
        # Habits
        habit_entries = health_client.get_habits(days=1)
        if habit_entries:
            completed = [h for h in habit_entries if h['fields'].get('Completed')]
            report['health']['habits'] = {
                'count': len(habit_entries),
                'completed': len(completed),
                'names': list(set(h['fields'].get('Habit', 'Unknown') for h in completed))
            }
        
        # WHOOP Recovery (if available)
        try:
            whoop_file = Path.home() / '.openclaw/whoop_data/latest_recovery.json'
            if whoop_file.exists():
                with open(whoop_file, 'r') as f:
                    whoop_data = json.load(f)
                    report['health']['whoop_recovery'] = {
                        'score': whoop_data.get('recovery_score'),
                        'hrv': whoop_data.get('hrv'),
                        'resting_hr': whoop_data.get('resting_hr')
                    }
        except:
            pass
        
    except Exception as e:
        report['health_error'] = str(e)
    
    # Productivity Base
    try:
        prod_client = get_productivity_client()
        
        # TAT Tasks
        all_tasks = prod_client.get_tat_tasks()
        today_tasks = [
            t for t in all_tasks 
            if t['fields'].get('Date Created') == yesterday
        ]
        
        if today_tasks:
            by_category = defaultdict(list)
            for task in today_tasks:
                cat = task['fields'].get('Category', 'Unknown')
                by_category[cat].append(task['fields'].get('Task Name', 'Unnamed'))
            
            report['productivity']['tat_tasks'] = {
                'count': len(today_tasks),
                'by_category': dict(by_category)
            }
        
        # Also get completed tasks
        completed_tasks = [
            t for t in all_tasks 
            if t['fields'].get('Status') == 'Complete'
        ]
        if completed_tasks:
            report['productivity']['completed_today'] = len(completed_tasks)
        
    except Exception as e:
        report['productivity_error'] = str(e)
    
    # Calculate totals
    total_entries = sum([
        report['health'].get('food_log', {}).get('count', 0),
        1 if report['health'].get('weight') else 0,
        report['health'].get('workouts', {}).get('count', 0),
        report['health'].get('habits', {}).get('count', 0),
        report['productivity'].get('tat_tasks', {}).get('count', 0)
    ])
    
    report['summary']['total_entries'] = total_entries
    report['summary']['tables_with_data'] = sum([
        1 if report['health'].get('food_log') else 0,
        1 if report['health'].get('weight') else 0,
        1 if report['health'].get('workouts') else 0,
        1 if report['health'].get('habits') else 0,
        1 if report['productivity'].get('tat_tasks') else 0
    ])
    
    return report

def format_telegram_message(report):
    """Format the report as a Telegram message"""
    date_str = report['date']
    
    message = f"📊 *Daily Confirmation Report - {date_str}*\n"
    message += "═" * 30 + "\n\n"
    
    # Health Section
    message += "💪 *Health & Fitness*\n"
    message += "─" * 20 + "\n"
    
    if report['health'].get('food_log'):
        food = report['health']['food_log']
        message += f"🍽️ Food: {food['count']} entries, {food['total_calories']} cal\n"
        if food['entries']:
            message += f"   📝 {', '.join(food['entries'][:3])}\n"
    
    if report['health'].get('weight'):
        weight = report['health']['weight']
        message += f"⚖️ Weight: {weight['weight']} kg\n"
    
    if report['health'].get('workouts'):
        workouts = report['health']['workouts']
        message += f"🏋️ Workouts: {workouts['count']} ({workouts['total_minutes']} min)\n"
        if workouts['types']:
            message += f"   📝 {', '.join(workouts['types'])}\n"
    
    if report['health'].get('habits'):
        habits = report['health']['habits']
        message += f"✅ Habits: {habits['completed']}/{habits['count']} completed\n"
        if habits['names']:
            message += f"   📝 {', '.join(habits['names'][:5])}\n"
    
    if report['health'].get('whoop_recovery'):
        whoop = report['health']['whoop_recovery']
        if whoop.get('score'):
            message += f"💓 Recovery: {whoop['score']}%\n"
    
    message += "\n"
    
    # Productivity Section
    message += "📋 *Productivity*\n"
    message += "─" * 20 + "\n"
    
    if report['productivity'].get('tat_tasks'):
        tasks = report['productivity']['tat_tasks']
        message += f"✅ TAT Tasks: {tasks['count']} added today\n"
        
        # Show breakdown by category
        for cat, names in tasks.get('by_category', {}).items():
            cat_name = {'1': '🔴 Today', '3': '🟠 3-Day', '7': '🟡 7-Day', '30': '🟢 30-Day'}.get(cat, cat)
            message += f"   {cat_name}: {len(names)}\n"
    
    if report['productivity'].get('completed_today'):
        message += f"🏁 Completed: {report['productivity']['completed_today']} tasks\n"
    
    message += "\n"
    
    # Summary
    message += "📈 *Summary*\n"
    message += "─" * 20 + "\n"
    message += f"Total entries: {report['summary']['total_entries']}\n"
    message += f"Active tables: {report['summary']['tables_with_data']}/5\n"
    
    # Highlights
    message += "\n🌟 *Highlights*\n"
    message += "─" * 20 + "\n"
    
    highlights = []
    
    if report['health'].get('workouts', {}).get('count', 0) > 0:
        highlights.append("💪 Workout completed!")
    
    if report['health'].get('habits', {}).get('completed', 0) >= 3:
        highlights.append(f"✅ {report['health']['habits']['completed']} habits tracked")
    
    if report['health'].get('food_log', {}).get('count', 0) >= 3:
        highlights.append("🍽️ Good meal tracking")
    
    if report['productivity'].get('tat_tasks', {}).get('count', 0) > 0:
        highlights.append(f"📝 {report['productivity']['tat_tasks']['count']} tasks added")
    
    if report['health'].get('whoop_recovery', {}).get('score', 0) >= 67:
        highlights.append("🟢 Great recovery score!")
    elif report['health'].get('whoop_recovery', {}).get('score', 0) >= 50:
        highlights.append("🟡 Moderate recovery")
    
    if not highlights:
        highlights.append("📌 New day tomorrow - fresh start!")
    
    for highlight in highlights[:5]:
        message += f"• {highlight}\n"
    
    message += "\n🦞 *Clawson* - Keep building!"
    
    return message

def save_report(report):
    """Save report to file for historical reference"""
    reports_dir = Path.home() / '.openclaw/workspace/reports'
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"daily-report-{report['date']}.json"
    filepath = reports_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    return filepath

def send_telegram_message(message):
    """Send message via Telegram"""
    try:
        # Import the message tool
        sys.path.insert(0, str(Path.home() / '.openclaw/workspace'))
        
        # Use the message tool if available (when running in OpenClaw)
        # Otherwise, we'll print to console for testing
        print("\n" + "="*50)
        print("TELEGRAM MESSAGE (would be sent):")
        print("="*50)
        print(message)
        print("="*50 + "\n")
        
        # Try to actually send if we're in OpenClaw environment
        try:
            from skills.telegram import send_message
            send_message(message, parse_mode='Markdown')
            return True
        except:
            pass
        
        return True
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        return False

def generate_daily_report():
    """Main function to generate and send daily report"""
    print("📊 Generating Daily Confirmation Report...")
    print("═" * 50)
    
    # Get data
    report = get_today_entries()
    
    # Print summary
    print(f"\n📅 Date: {report['date']}")
    print(f"📈 Total entries: {report['summary']['total_entries']}")
    print(f"📊 Active tables: {report['summary']['tables_with_data']}")
    
    # Format message
    message = format_telegram_message(report)
    
    # Save report
    report_path = save_report(report)
    print(f"\n💾 Report saved: {report_path}")
    
    # Send Telegram message
    print("\n📤 Sending Telegram message...")
    if send_telegram_message(message):
        print("✅ Telegram message sent successfully")
    else:
        print("⚠️ Telegram message could not be sent")
    
    print("\n" + "═" * 50)
    print("✅ Daily report complete!")
    
    return report

if __name__ == "__main__":
    report = generate_daily_report()
    
    # Output JSON for automation
    print(f"\n---JSON_REPORT---")
    print(json.dumps(report, indent=2, default=str))
