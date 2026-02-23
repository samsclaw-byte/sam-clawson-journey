#!/usr/bin/env python3
"""
D1 API Client for Trak
Replaces airtable_client.py
"""

import os
import requests
import json

# Worker URL
D1_API_URL = os.environ.get("D1_API_URL", "https://trak-api.samsclaw-498.workers.dev")

class D1Client:
    def __init__(self, api_url=D1_API_URL):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    # ============== TASKS ==============
    def get_tasks(self):
        """Get all tasks"""
        resp = self.session.get(f"{self.api_url}/api/tasks")
        resp.raise_for_status()
        return resp.json()
    
    def get_task(self, task_id):
        """Get single task"""
        resp = self.session.get(f"{self.api_url}/api/tasks/{task_id}")
        resp.raise_for_status()
        return resp.json()
    
    def create_task(self, task_name, category, priority="Medium", notes=None):
        """Create new task"""
        data = {
            "task_name": task_name,
            "category": category,
            "priority": priority,
            "notes": notes
        }
        resp = self.session.post(f"{self.api_url}/api/tasks", json=data)
        resp.raise_for_status()
        return resp.json()
    
    def update_task(self, task_id, status=None, notes=None):
        """Update task status/notes"""
        data = {}
        if status:
            data["status"] = status
        if notes:
            data["notes"] = notes
        resp = self.session.put(f"{self.api_url}/api/tasks/{task_id}", json=data)
        resp.raise_for_status()
        return resp.json()
    
    def delete_task(self, task_id):
        """Delete task"""
        resp = self.session.delete(f"{self.api_url}/api/tasks/{task_id}")
        resp.raise_for_status()
        return resp.json()
    
    # ============== HABITS ==============
    def get_habits(self, date=None):
        """Get habits for date"""
        if date:
            resp = self.session.get(f"{self.api_url}/api/habits?date={date}")
        else:
            resp = self.session.get(f"{self.api_url}/api/habits")
        resp.raise_for_status()
        return resp.json()
    
    def create_habit(self, habit_name, date=None, completed=False, notes=None):
        """Create/update habit"""
        data = {
            "habit_name": habit_name,
            "date": date,
            "completed": completed,
            "notes": notes
        }
        resp = self.session.post(f"{self.api_url}/api/habits", json=data)
        resp.raise_for_status()
        return resp.json()
    
    # ============== NUTRITION ==============
    def get_nutrition(self, date=None):
        """Get nutrition for date"""
        if date:
            resp = self.session.get(f"{self.api_url}/api/nutrition?date={date}")
        else:
            resp = self.session.get(f"{self.api_url}/api/nutrition")
        resp.raise_for_status()
        return resp.json()
    
    def create_nutrition(self, date, meal_type, description, calories=None, 
                         protein=None, carbs=None, fat=None, source="manual"):
        """Create nutrition entry"""
        data = {
            "date": date,
            "meal_type": meal_type,
            "description": description,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "source": source
        }
        resp = self.session.post(f"{self.api_url}/api/nutrition", json=data)
        resp.raise_for_status()
        return resp.json()
    
    # ============== EXERCISE ==============
    def get_exercise(self, date=None):
        """Get exercise for date"""
        if date:
            resp = self.session.get(f"{self.api_url}/api/exercise?date={date}")
        else:
            resp = self.session.get(f"{self.api_url}/api/exercise")
        resp.raise_for_status()
        return resp.json()
    
    def create_exercise(self, date, workout_type, duration_minutes=None, 
                       strain=None, notes=None, source="manual"):
        """Create exercise entry"""
        data = {
            "date": date,
            "workout_type": workout_type,
            "duration_minutes": duration_minutes,
            "strain": strain,
            "notes": notes,
            "source": source
        }
        resp = self.session.post(f"{self.api_url}/api/exercise", json=data)
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    # Quick test
    client = D1Client()
    print("Testing D1 API...")
    
    # Health check
    try:
        resp = requests.get(f"{D1_API_URL}/api/health")
        print(f"Health: {resp.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
