#!/usr/bin/env python3
"""
D1 Client using wrangler CLI
Directly queries D1 database - no API calls needed
"""

import os
import subprocess
import json
import re
from datetime import datetime, timedelta

D1_DB = "trak-db"

def run_wrangler(command):
    """Run wrangler command and return results - ALWAYS use remote"""
    # Force remote execution
    result = subprocess.run(
        f"wrangler d1 execute {D1_DB} --command=\"{command}\" --remote 2>&1",
        shell=True,
        capture_output=True,
        text=True,
        timeout=30
    )
    # Check for errors
    if "error" in result.stderr.lower() or result.returncode != 0:
        # Try one more time
        result = subprocess.run(
            f"wrangler d1 execute {D1_DB} --command=\"{command}\" --remote",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
    return result.stdout + result.stderr

def get_results(output):
    """Extract results from wrangler JSON output"""
    try:
        # Find JSON array in output (skip wrangler banner)
        match = re.search(r'\[\s*\{.*\}\s*\]', output, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            if isinstance(data, list) and len(data) > 0:
                if 'results' in data[0]:
                    return data[0]['results']
        return []
    except Exception as e:
        print(f"Parse error: {e}")
        return []

class D1Client:
    def __init__(self):
        pass
    
    # ============== TASKS ==============
    def get_tasks(self):
        """Get all tasks"""
        try:
            output = run_wrangler("SELECT * FROM tat_tasks ORDER BY due_date ASC")
            return get_results(output)
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def create_task(self, task_name, category, priority="Medium", notes=None):
        """Create new task"""
        import uuid
        task_id = "rec" + str(uuid.uuid4().hex[:10])
        date_created = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=category)).strftime('%Y-%m-%d')
        
        task_name = task_name.replace("'", "''")
        notes = (notes or "").replace("'", "''")
        
        sql = f"""INSERT INTO tat_tasks (id, task_name, category, status, priority, date_created, due_date, notes)
                  VALUES ('{task_id}', '{task_name}', {category}, 'Not Started', '{priority}', '{date_created}', '{due_date}', '{notes}')"""
        
        try:
            run_wrangler(sql)
            return {"success": True, "id": task_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== HABITS ==============
    def get_habits(self, date=None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            output = run_wrangler(f"SELECT * FROM habits WHERE date = '{date}'")
            return get_results(output)
        except:
            return []

    # ============== NUTRITION ==============
    def get_nutrition(self, date=None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            output = run_wrangler(f"SELECT * FROM nutrition WHERE date = '{date}'")
            return get_results(output)
        except:
            return []

    def create_nutrition(self, date, meal_type, description, calories=None, protein=None, carbs=None, fat=None, source="manual"):
        import uuid
        nut_id = "nut" + str(uuid.uuid4().hex[:8])
        desc = (description or "").replace("'", "''")
        
        sql = f"""INSERT INTO nutrition (id, date, meal_type, description, calories, protein, carbs, fat, source)
                  VALUES ('{nut_id}', '{date}', '{meal_type}', '{desc}', {calories or 'NULL'}, {protein or 'NULL'}, {carbs or 'NULL'}, {fat or 'NULL'}, '{source}')"""
        try:
            run_wrangler(sql)
            return {"success": True, "id": nut_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== EXERCISE ==============
    def get_exercise(self, date=None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            output = run_wrangler(f"SELECT * FROM exercise WHERE date = '{date}'")
            return get_results(output)
        except:
            return []

    def create_exercise(self, date, workout_type, duration_minutes=None, strain=None, notes=None, source="manual"):
        import uuid
        exe_id = "exe" + str(uuid.uuid4().hex[:8])
        
        workout_type = (workout_type or "").replace("'", "''")
        notes = (notes or "").replace("'", "''")
        
        sql = f"""INSERT INTO exercise (id, date, workout_type, duration_minutes, strain, notes, source)
                  VALUES ('{exe_id}', '{date}', '{workout_type}', {duration_minutes or 'NULL'}, {strain or 'NULL'}, '{notes}', '{source}')"""
        try:
            run_wrangler(sql)
            return {"success": True, "id": exe_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== HABITS ==============
    def get_habits(self, date=None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            output = run_wrangler(f"SELECT * FROM habits WHERE date = '{date}'")
            return get_results(output)
        except:
            return []

    def create_habit(self, habit_name, date, completed=True, notes=None):
        import uuid
        hab_id = "hab" + str(uuid.uuid4().hex[:8])
        
        habit_name = (habit_name or "").replace("'", "''")
        notes = (notes or "").replace("'", "''")
        
        sql = f"""INSERT INTO habits (id, habit_name, date, completed, notes)
                  VALUES ('{hab_id}', '{habit_name}', '{date}', {1 if completed else 0}, {f"'{notes}'" if notes else 'NULL'})"""
        try:
            run_wrangler(sql)
            return {"success": True, "id": hab_id}
        except Exception as e:
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    client = D1Client()
    print("Testing D1 Client...")
    
    tasks = client.get_tasks()
    print(f"Tasks: {len(tasks)}")
    for t in tasks:
        print(f"  - {t.get('task_name')} (Cat: {t.get('category')})")
