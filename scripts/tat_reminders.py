#!/usr/bin/env python3
"""
TAT Reminder System - Cron Jobs for Overdue/Upcoming Tasks
Runs at 9am daily or triggered manually
"""

import sys
import os
sys.path.insert(0, '/home/samsclaw/.openclaw/workspace/scripts')

from tat_client_v3 import TATClient

def send_notification(message):
    """Send Telegram notification"""
    try:
        # Try to use the telegram notify if available
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID', '8210116595')
        
        if bot_token:
            import requests
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            requests.post(url, json=payload)
    except:
        pass
    
    # Always print
    print(message)

def check_tat_reminders():
    """Check for overdue and due-soon TAT tasks"""
    client = TATClient()
    
    messages = []
    messages.append("📋 <b>TAT Task Reminder</b>\n")
    
    # Get overdue tasks
    overdue = client.get_overdue_tasks()
    if overdue:
        messages.append(f"🔴 <b>OVERDUE ({len(overdue)} tasks):</b>")
        for task in overdue[:5]:  # Show max 5
            fields = task.get('fields', {})
            name = fields.get('Task Name', 'Unnamed')
            days = fields.get('Days Remaining', '??')
            messages.append(f"  • {name} ({days} days overdue)")
        if len(overdue) > 5:
            messages.append(f"  ... and {len(overdue) - 5} more")
        messages.append("")
    
    # Get tasks due today
    due_today = client.get_tasks_due_today()
    if due_today:
        messages.append(f"🟠 <b>DUE TODAY ({len(due_today)} tasks):</b>")
        for task in due_today[:5]:
            fields = task.get('fields', {})
            name = fields.get('Task Name', 'Unnamed')
            priority = fields.get('Priority', 'Medium')
            messages.append(f"  • {name} ({priority})")
        if len(due_today) > 5:
            messages.append(f"  ... and {len(due_today) - 5} more")
        messages.append("")
    
    # Get pending tasks summary
    pending = client.get_pending_tasks()
    if not overdue and not due_today and pending:
        messages.append(f"✅ <b>No urgent tasks!</b>")
        messages.append(f"   You have {len(pending)} pending tasks, none overdue.")
    elif not pending:
        messages.append("🎉 <b>All tasks complete!</b> No pending TAT tasks.")
    
    # Send consolidated message
    full_message = "\n".join(messages)
    send_notification(full_message)
    
    return {
        'overdue': len(overdue),
        'due_today': len(due_today),
        'pending': len(pending)
    }

def urgent_check():
    """Quick check for only overdue + due today - for frequent reminders"""
    client = TATClient()
    
    overdue = client.get_overdue_tasks()
    due_today = client.get_tasks_due_today()
    
    if overdue or due_today:
        messages = ["⏰ <b>TAT Urgent Tasks:</b>\n"]
        
        if overdue:
            messages.append(f"🔴 {len(overdue)} overdue")
        if due_today:
            messages.append(f"🟠 {len(due_today)} due today")
        
        send_notification("\n".join(messages))
        return True
    
    return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='TAT Reminder System')
    parser.add_argument('--urgent', action='store_true', help='Only check urgent (overdue + today)')
    parser.add_argument('--quiet', action='store_true', help='Only notify if there are tasks')
    
    args = parser.parse_args()
    
    if args.urgent:
        has_urgent = urgent_check()
        if not has_urgent and not args.quiet:
            print("✅ No urgent TAT tasks")
    else:
        stats = check_tat_reminders()
        print(f"\nSummary: {stats['overdue']} overdue, {stats['due_today']} due today, {stats['pending']} pending")
