#!/usr/bin/env python3
"""
Fetch Work Tasks data from Airtable for Mission Control
"""
import requests
import json
import os
from datetime import datetime, timedelta

def fetch_work_data():
    AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
    
    # TAT Work Tasks table
    PRODUCTIVITY_BASE = 'appuWxergK3HUJd8i'  # Your new Work base
    WORK_TABLE = 'tblqM03kLHq9VjoCd'  # TAT Work Tasks table
    PROJECTS_TABLE = 'tblUzMNkbcfnwCeYz'  # TAT Work Projects table
    DELIVERABLES_TABLE = 'tbl5KhVCQC2iKRucz'  # TAT Project Deliverables table
    
    headers = {'Authorization': f'Bearer {AIRTABLE_KEY}'}
    
    try:
        # Fetch Tasks
        url = f'https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/{WORK_TABLE}'
        response = requests.get(
            f'{url}?filterByFormula=Status!="Complete"&maxRecords=100&sort[0][field]=Priority&sort[0][direction]=desc',
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Note: Work table not yet created or accessible")
            return get_sample_work_data()
        
        data = response.json()
        
        tasks = []
        recurring = []
        
        for record in data.get('records', []):
            fields = record.get('fields', {})
            item_type = fields.get('Type', 'Task')
            
            item = {
                'id': record['id'],
                'name': fields.get('Name', ''),
                'detail': fields.get('Detail', ''),
                'type': item_type,
                'tat': fields.get('TAT Days', 3),
                'due_date': fields.get('Due Date', ''),
                'category': fields.get('Category', ''),
                'source': fields.get('Source', ''),
                'project': fields.get('Project', ''),
                'stakeholder': fields.get('Stakeholder', ''),
                'assigned': fields.get('Assigned To', ''),
                'status': fields.get('Status', 'Not Started'),
                'priority': fields.get('Priority', 'P2'),
                'effort': fields.get('Effort', 'Medium'),
                'blocked_reason': fields.get('Blocked Reason', ''),
                'created': fields.get('Date Created', '')
            }
            
            if item_type == 'Task':
                tasks.append(item)
            elif item_type == 'Recurring':
                item['frequency'] = fields.get('Frequency', 'Monthly')
                item['next_due'] = fields.get('Next Due', '')
                item['template'] = fields.get('Template', '')
                recurring.append(item)
        
        # Fetch Projects with Deliverables
        projects = fetch_projects_with_deliverables(PRODUCTIVITY_BASE, PROJECTS_TABLE, DELIVERABLES_TABLE, headers)
        
        return {
            'tasks': tasks,
            'projects': projects,
            'recurring': recurring,
            'last_updated': datetime.now().isoformat(),
            'summary': {
                'total_active': len(tasks) + len(projects),
                'urgent': sum(1 for t in tasks if t['priority'] == 'P0'),
                'blocked': sum(1 for t in tasks if t['status'] == 'Blocked'),
                'due_this_week': sum(1 for t in tasks if is_due_this_week(t['due_date']))
            }
        }
        
    except Exception as e:
        print(f"Using sample data: {e}")
        return get_sample_work_data()

def fetch_projects_with_deliverables(base_id, projects_table, deliverables_table, headers):
    """Fetch projects with their deliverables from Airtable"""
    projects = []
    
    try:
        # Fetch deliverables first
        deliv_url = f'https://api.airtable.com/v0/{base_id}/{deliverables_table}'
        deliv_response = requests.get(
            f'{deliv_url}?maxRecords=100',
            headers=headers,
            timeout=30
        )
        
        deliverables_map = {}
        if deliv_response.status_code == 200:
            for record in deliv_response.json().get('records', []):
                fields = record.get('fields', {})
                # Get linked project IDs
                project_links = fields.get('Project', [])
                
                deliv = {
                    'id': record['id'],
                    'name': fields.get('Name', ''),
                    'status': fields.get('Status', 'Not Started'),
                    'owner': fields.get('Owner', ''),
                    'due_date': fields.get('Due Date', ''),
                    'weight': fields.get('Weight', 0),
                    'progress': fields.get('Progress', 0),
                    'blocked_reason': fields.get('Blocked Reason', ''),
                    'notes': fields.get('Notes', '')
                }
                
                # Map deliverables to projects
                for proj_id in project_links:
                    if proj_id not in deliverables_map:
                        deliverables_map[proj_id] = []
                    deliverables_map[proj_id].append(deliv)
        
        # Fetch projects
        proj_url = f'https://api.airtable.com/v0/{base_id}/{projects_table}'
        proj_response = requests.get(
            f'{proj_url}?filterByFormula=Status!="Complete"&maxRecords=50',
            headers=headers,
            timeout=30
        )
        
        if proj_response.status_code == 200:
            for record in proj_response.json().get('records', []):
                fields = record.get('fields', {})
                proj_id = record['id']
                
                project = {
                    'id': proj_id,
                    'name': fields.get('Name', ''),
                    'description': fields.get('Description', ''),
                    'status': fields.get('Status', 'Planning'),
                    'progress': fields.get('Progress', 0),
                    'start_date': fields.get('Start Date', ''),
                    'target_end_date': fields.get('Target End Date', ''),
                    'project_lead': fields.get('Project Lead', ''),
                    'stakeholder': fields.get('Stakeholder', ''),
                    'notes_context': fields.get('Notes/Context', ''),
                    'cram_notes': fields.get('CRAM Notes', ''),
                    'deliverables': deliverables_map.get(proj_id, [])
                }
                
                # Calculate overall progress from deliverables if available
                if project['deliverables']:
                    total_weight = sum(d['weight'] for d in project['deliverables'])
                    if total_weight > 0:
                        weighted_progress = sum(d['progress'] * d['weight'] for d in project['deliverables']) / total_weight
                        project['progress'] = round(weighted_progress)
                
                projects.append(project)
        
        return projects
        
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []

def is_due_this_week(due_date_str):
    if not due_date_str:
        return False
    try:
        due = datetime.strptime(due_date_str, '%Y-%m-%d')
        today = datetime.now()
        week_later = today + timedelta(days=7)
        return today <= due <= week_later
    except:
        return False

def get_sample_work_data():
    """Return sample data for demo/development"""
    today = datetime.now()
    
    return {
        'tasks': [
            {
                'id': 'sample1',
                'name': 'MGC fees for digital card',
                'detail': 'Create unit comparison DGC vs Physical, Scenario table',
                'type': 'Task',
                'tat': 3,
                'due_date': (today + timedelta(days=2)).strftime('%Y-%m-%d'),
                'category': 'Analysis',
                'source': 'In Person',
                'project': 'Digital Card Strategy',
                'stakeholder': 'Dem',
                'assigned': 'Me',
                'status': 'In Progress',
                'priority': 'P1',
                'effort': 'Medium',
                'blocked_reason': ''
            },
            {
                'id': 'sample2',
                'name': 'Aylin card campaign invoicing',
                'detail': 'Process invoice for card campaign',
                'type': 'Task',
                'tat': 3,
                'due_date': (today + timedelta(days=1)).strftime('%Y-%m-%d'),
                'category': 'Financial',
                'source': 'Email',
                'project': 'Card Campaign',
                'stakeholder': 'Aylin',
                'assigned': 'Me',
                'status': 'In Progress',
                'priority': 'P1',
                'effort': 'Small',
                'blocked_reason': ''
            },
            {
                'id': 'sample3',
                'name': 'No objection certificate',
                'detail': 'Obtain NOC for project approval',
                'type': 'Task',
                'tat': 7,
                'due_date': (today + timedelta(days=5)).strftime('%Y-%m-%d'),
                'category': 'Admin',
                'source': 'Email',
                'project': 'Project X',
                'stakeholder': 'Ahmed',
                'assigned': 'Me',
                'status': 'Not Started',
                'priority': 'P1',
                'effort': 'Small',
                'blocked_reason': ''
            }
        ],
        'projects': [
            {
                'id': 'proj1',
                'name': 'Umair contract renewal',
                'detail': 'Contract renewal process with Umair',
                'type': 'Project',
                'tat': 7,
                'due_date': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
                'category': 'Operations',
                'source': 'In Person',
                'project': 'Osman Contract',
                'stakeholder': 'Osman',
                'assigned': 'Me',
                'status': 'In Progress',
                'priority': 'P0',
                'effort': 'Large',
                'blocked_reason': 'Awaiting legal review',
                'phases': [
                    {'name': 'Initial Review', 'status': 'Complete', 'due': '2026-02-10'},
                    {'name': 'Legal Review', 'status': 'Blocked', 'due': '2026-02-18'},
                    {'name': 'Final Approval', 'status': 'Not Started', 'due': '2026-02-25'}
                ],
                'progress': 30
            }
        ],
        'recurring': [
            {
                'id': 'rec1',
                'name': 'Month-end finance close',
                'detail': 'GL entries, reconciliations, variance analysis',
                'type': 'Recurring',
                'category': 'Financial',
                'stakeholder': 'CFO',
                'assigned': 'Me',
                'status': 'Not Started',
                'priority': 'P0',
                'frequency': 'Monthly',
                'next_due': '2026-02-28',
                'template': '1. GL entries 2. Reconciliations 3. Variance analysis 4. Management pack'
            },
            {
                'id': 'rec2',
                'name': 'Marketing spend report',
                'detail': 'Calculate fully loaded marketing spend',
                'type': 'Recurring',
                'category': 'Financial',
                'stakeholder': 'Raffy',
                'assigned': 'Me',
                'status': 'Complete',
                'priority': 'P1',
                'frequency': 'Monthly',
                'next_due': '2026-03-05',
                'template': '1. Collect channel data 2. Calculate ROI 3. Compare to budget'
            }
        ],
        'last_updated': datetime.now().isoformat(),
        'summary': {
            'total_active': 4,
            'urgent': 1,
            'blocked': 1,
            'due_this_week': 3
        }
    }

def main():
    data = fetch_work_data()
    
    output_path = '/home/samsclaw/.openclaw/workspace/mission-control/data/work_data.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Work data saved to {output_path}")
    print(f"   Tasks: {len(data['tasks'])}")
    print(f"   Projects: {len(data['projects'])}")
    print(f"   Recurring: {len(data['recurring'])}")

if __name__ == '__main__':
    main()
