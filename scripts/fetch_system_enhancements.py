#!/usr/bin/env python3
"""
Fetch System Enhancement tasks from TAT and save for Mission Control architecture page.
"""
import requests
import json
import os

def fetch_system_enhancements():
    AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
    PRODUCTIVITY_BASE = 'appvUbV8IeGhxmcPn'
    TAT_TABLE = 'tblkbuvkZUSpm1IgJ'
    
    url = f'https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/{TAT_TABLE}'
    headers = {'Authorization': f'Bearer {AIRTABLE_KEY}'}
    
    # Fetch all non-complete tasks and filter locally
    response = requests.get(
        f'{url}?filterByFormula=Status!="Complete"&maxRecords=100',
        headers=headers,
        timeout=30
    )
    
    data = response.json()
    
    enhancements = []
    for record in data.get('records', []):
        fields = record.get('fields', {})
        category = fields.get('Category', '')
        # Filter for System Enhancement category
        if 'System Enhancement' in category:
            enhancements.append({
                'name': fields.get('Task Name', ''),
                'urgency': fields.get('Urgency Level', '🟢 Normal'),
                'status': fields.get('Status', 'Not Started'),
                'days_remaining': fields.get('Days Remaining', 'N/A'),
                'workflow': infer_workflow(fields.get('Task Name', ''))
            })
    
    return enhancements

def infer_workflow(task_name):
    """Map task to workflow based on keywords."""
    name_lower = task_name.lower()
    
    if 'voice' in name_lower or 'tts' in name_lower or 'transcribe' in name_lower:
        return '🎙️ Voice Transcribe'
    elif 'whoop' in name_lower or 'webhook' in name_lower or 'recovery' in name_lower:
        return '💓 WHOOP Recovery'
    elif 'dashboard' in name_lower or 'layout' in name_lower or 'pages' in name_lower:
        return '📊 Dashboard Update'
    elif 'tat' in name_lower or 'task' in name_lower or 'schema' in name_lower:
        return '📋 TAT System'
    elif 'calendar' in name_lower:
        return '📅 Calendar Sync'
    elif 'cron' in name_lower or 'schedule' in name_lower:
        return '🌅 Morning Brief'
    elif 'water' in name_lower:
        return '💧 Water Tracker'
    elif 'security' in name_lower or 'update' in name_lower:
        return '🛡️ Security Sentinel'
    elif 'ai' in name_lower or 'clawson' in name_lower or 'search' in name_lower:
        return '🤖 AI Development'
    else:
        return '🔧 System'

def main():
    enhancements = fetch_system_enhancements()
    
    output_path = '/home/samsclaw/.openclaw/workspace/mission-control/data/system_enhancements.json'
    
    with open(output_path, 'w') as f:
        json.dump({'enhancements': enhancements, 'last_updated': str(os.popen('date -Iseconds').read().strip())}, f, indent=2)
    
    print(f"✅ Saved {len(enhancements)} system enhancements to {output_path}")
    
    # Print summary
    for e in enhancements[:10]:
        print(f"  • {e['workflow']}: {e['name'][:50]}... ({e['urgency']})")

if __name__ == '__main__':
    main()
