#!/usr/bin/env python3
"""
TAT v3 API Client - Updated for Formula Due Dates
No manual due date calculation - Airtable handles it via formula
"""

import os
import requests
from datetime import datetime

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
BASE_ID = "appvUbV8IeGhxmcPn"
TABLE_ID = "tblkbuvkZUSpm1IgJ"

class TATClient:
    def __init__(self):
        self.api_key = AIRTABLE_KEY
        self.base_url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def add_task(self, task_name, category, status="Not Started", priority="Medium", notes="", tags=None):
        """
        Add TAT task - Due Date auto-calculated by Airtable formula
        
        Required fields:
        - task_name: str
        - category: "1", "3", "7", or "30"
        
        Optional:
        - status: "Not Started" (default), "In Progress", "Blocked", "Complete", "Cancelled"
        - priority: "Critical", "High", "Medium", "Low"
        - notes: str
        - tags: list of tags
        """
        
        if not task_name or not task_name.strip():
            raise ValueError("Task Name is required")
        
        if category not in ['1', '3', '7', '30']:
            raise ValueError("Category must be 1, 3, 7, or 30")
        
        fields = {
            "Task Name": task_name.strip(),
            "Category": category,
            "Status": status,
            "Priority": priority,
        }
        
        if notes:
            fields["Notes"] = notes
        
        if tags:
            fields["Tags"] = tags
        
        # Note: Due Date is NOT included - it's auto-calculated by formula
        # Due Date = DATEADD({Date Created}, VALUE({Category}), 'days')
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json={"fields": fields}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ TAT Task created: {task_name}")
            print(f"   Category: {category} days")
            print(f"   Status: {status}")
            print(f"   Due Date: (auto-calculated by formula)")
            return result
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            raise Exception(f"Failed to create task: {error_msg}")
    
    def update_task(self, record_id, **updates):
        """Update task fields. Cannot update Due Date (formula field)."""
        
        # Remove formula fields if accidentally passed
        forbidden_fields = ['Due Date', 'TAT Days', 'Days Remaining', 'Urgency Level', 'Days to Complete']
        for field in forbidden_fields:
            if field in updates:
                del updates[field]
        
        response = requests.patch(
            f"{self.base_url}/{record_id}",
            headers=self.headers,
            json={"fields": updates}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            raise Exception(f"Failed to update task: {error_msg}")
    
    def complete_task(self, record_id):
        """Mark task as complete - triggers automation to set Completed Date"""
        return self.update_task(record_id, Status="Complete")
    
    def get_pending_tasks(self):
        """Get all non-completed tasks"""
        formula = "OR({Status}='Not Started', {Status}='In Progress', {Status}='Blocked')"
        response = requests.get(
            f"{self.base_url}?filterByFormula={formula}&sort[0][field]=Due Date&sort[0][direction]=asc",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json().get('records', [])
        return []
    
    def get_overdue_tasks(self):
        """Get overdue tasks (Days Remaining < 0)"""
        formula = "AND({Days Remaining}<0, {Status}!='Complete', {Status}!='Cancelled')"
        response = requests.get(
            f"{self.base_url}?filterByFormula={formula}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json().get('records', [])
        return []
    
    def get_tasks_due_today(self):
        """Get tasks due today (Days Remaining = 0)"""
        formula = "AND({Days Remaining}=0, {Status}!='Complete', {Status}!='Cancelled')"
        response = requests.get(
            f"{self.base_url}?filterByFormula={formula}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json().get('records', [])
        return []

# Convenience function for quick use
def add_tat_task_v3(task_name, category, **kwargs):
    """Quick add TAT task with v3 structure"""
    client = TATClient()
    return client.add_task(task_name, category, **kwargs)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("TAT v3 - Formula Due Dates")
        print("")
        print("Usage: python3 tat_client_v3.py 'Task Name' CATEGORY [options]")
        print("")
        print("Examples:")
        print("  python3 tat_client_v3.py 'Fix printer' 1")
        print("  python3 tat_client_v3.py 'Research flights' 3 --priority High")
        print("  python3 tat_client_v3.py 'Quarterly review' 30 --notes 'Prepare slides'")
        print("")
        print("Categories: 1, 3, 7, 30 (days)")
        print("Due Date: Auto-calculated by Airtable formula")
        sys.exit(1)
    
    task_name = sys.argv[1]
    category = sys.argv[2]
    
    # Parse optional args
    priority = "Medium"
    notes = ""
    
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--priority' and i + 1 < len(sys.argv):
            priority = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--notes' and i + 1 < len(sys.argv):
            notes = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    add_tat_task_v3(task_name, category, priority=priority, notes=notes)
