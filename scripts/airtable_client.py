#!/usr/bin/env python3
"""
Airtable Client Helper Module
Unified interface for interacting with Sam's Airtable bases
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests

# Base Configuration
HEALTH_BASE_ID = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE_ID = "appvUbV8IeGhxmcPn"

# Table IDs (will be discovered dynamically or cached)
TABLE_CACHE_FILE = os.path.expanduser("~/.openclaw/workspace/.airtable_table_cache.json")

class AirtableClient:
    """Unified Airtable API client for Health & Productivity bases"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Airtable client with API key"""
        self.api_key = api_key or self._load_api_key()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.airtable.com/v0"
        self.table_cache = self._load_table_cache()
        
    def _load_api_key(self) -> str:
        """Load API key from config file"""
        key_path = os.path.expanduser("~/.config/airtable/api_key")
        try:
            with open(key_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise ValueError(f"Airtable API key not found at {key_path}")
    
    def _load_table_cache(self) -> Dict:
        """Load cached table IDs"""
        if os.path.exists(TABLE_CACHE_FILE):
            try:
                with open(TABLE_CACHE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_table_cache(self):
        """Save table IDs to cache"""
        os.makedirs(os.path.dirname(TABLE_CACHE_FILE), exist_ok=True)
        with open(TABLE_CACHE_FILE, 'w') as f:
            json.dump(self.table_cache, f, indent=2)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make API request with rate limiting and error handling"""
        url = f"{self.base_url}/{endpoint}"
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = requests.request(
                    method, 
                    url, 
                    headers=self.headers, 
                    timeout=30,
                    **kwargs
                )
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    print(f"⚠️ Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                # Handle other errors
                if response.status_code >= 400:
                    error_msg = f"Airtable API error: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('error', {}).get('message', response.text)}"
                    except:
                        error_msg += f" - {response.text}"
                    raise Exception(error_msg)
                
                return response.json()
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"⚠️ Request timeout, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Request error: {e}, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
        
        raise Exception("Max retries exceeded")
    
    def get_tables(self, base_id: str) -> List[Dict]:
        """Get all tables in a base"""
        result = self._make_request("GET", f"meta/bases/{base_id}/tables")
        return result.get('tables', [])
    
    def get_table_id(self, base_id: str, table_name: str) -> Optional[str]:
        """Get table ID by name, using cache if available"""
        cache_key = f"{base_id}:{table_name}"
        
        if cache_key in self.table_cache:
            return self.table_cache[cache_key]
        
        # Discover tables
        tables = self.get_tables(base_id)
        for table in tables:
            if table['name'] == table_name:
                table_id = table['id']
                self.table_cache[cache_key] = table_id
                self._save_table_cache()
                return table_id
        
        return None
    
    def query_records(self, base_id: str, table_name: str, 
                      filter_formula: Optional[str] = None,
                      sort: Optional[List[Dict]] = None,
                      max_records: int = 100) -> List[Dict]:
        """Query records from a table"""
        table_id = self.get_table_id(base_id, table_name)
        if not table_id:
            raise ValueError(f"Table '{table_name}' not found in base {base_id}")
        
        endpoint = f"{base_id}/{table_id}"
        
        # Build query params - Airtable expects specific format for sort
        params = {"maxRecords": max_records}
        if filter_formula:
            params["filterByFormula"] = filter_formula
        
        result = self._make_request("GET", endpoint, params=params)
        records = result.get('records', [])
        
        # Sort locally if needed
        if sort and records:
            for sort_item in reversed(sort):
                field = sort_item.get('field')
                direction = sort_item.get('direction', 'asc')
                if field:
                    records = sorted(
                        records, 
                        key=lambda x: x.get('fields', {}).get(field, ''),
                        reverse=(direction == 'descending')
                    )
        
        return records
    
    def create_record(self, base_id: str, table_name: str, 
                     fields: Dict[str, Any]) -> Dict:
        """Create a new record"""
        table_id = self.get_table_id(base_id, table_name)
        if not table_id:
            raise ValueError(f"Table '{table_name}' not found in base {base_id}")
        
        endpoint = f"{base_id}/{table_id}"
        payload = {"fields": fields}
        
        return self._make_request("POST", endpoint, json=payload)
    
    def update_record(self, base_id: str, table_name: str, 
                     record_id: str, fields: Dict[str, Any]) -> Dict:
        """Update an existing record"""
        table_id = self.get_table_id(base_id, table_name)
        if not table_id:
            raise ValueError(f"Table '{table_name}' not found in base {base_id}")
        
        endpoint = f"{base_id}/{table_id}/{record_id}"
        payload = {"fields": fields}
        
        return self._make_request("PATCH", endpoint, json=payload)
    
    def delete_record(self, base_id: str, table_name: str, 
                     record_id: str) -> bool:
        """Delete a record"""
        table_id = self.get_table_id(base_id, table_name)
        if not table_id:
            raise ValueError(f"Table '{table_name}' not found in base {base_id}")
        
        endpoint = f"{base_id}/{table_id}/{record_id}"
        
        try:
            self._make_request("DELETE", endpoint)
            return True
        except:
            return False


# Productivity Base Specific Methods
class ProductivityAirtableClient(AirtableClient):
    """Client specifically for Productivity base"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_id = PRODUCTIVITY_BASE_ID
    
    # TAT Tasks
    def get_tat_tasks(self, category: Optional[str] = None, 
                     status: Optional[str] = None) -> List[Dict]:
        """Get TAT tasks with optional filters"""
        filters = []
        
        if category:
            filters.append(f"{{Category}} = '{category}'")
        if status:
            filters.append(f"{{Status}} = '{status}'")
        
        filter_formula = " AND ".join(filters) if filters else None
        
        return self.query_records(self.base_id, "TAT Tasks v2",
                                 filter_formula=filter_formula,
                                 sort=[{"field": "Due Date", "direction": "asc"}])
    
    def get_urgent_tat_tasks(self) -> List[Dict]:
        """Get urgent TAT tasks (Category 1 = Today)"""
        # Get Category 1 tasks (Today)
        cat1_tasks = self.get_tat_tasks(category="1")
        
        # Get Not Started or In Progress tasks (excluding Complete)
        active_tasks = self.get_tat_tasks(status="Not Started") + self.get_tat_tasks(status="In Progress")
        
        # Combine and deduplicate
        seen_ids = set()
        urgent = []
        for task in cat1_tasks + active_tasks:
            if task['id'] not in seen_ids:
                seen_ids.add(task['id'])
                urgent.append(task)
        
        return urgent
    
    def add_tat_task(self, task_name: str, category: str = "7",
                    priority: str = "Medium", notes: str = "",
                    due_date: Optional[str] = None) -> Dict:
        """Add a new TAT task"""
        if not due_date:
            # Calculate due date based on category
            days = int(category) if category.isdigit() else 7
            due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        fields = {
            "Task Name": task_name,
            "Category": category,
            "TAT Category Days": int(category) if category.isdigit() else 7,
            "Status": "Not Started",
            "Date Created": datetime.now().strftime('%Y-%m-%d')
        }
        
        # Add notes to task name if provided
        if notes:
            fields["Task Name"] = f"{task_name} - {notes}"
        
        return self.create_record(self.base_id, "TAT Tasks v2", fields)
    
    def update_tat_status(self, record_id: str, status: str) -> Dict:
        """Update TAT task status"""
        return self.update_record(self.base_id, "TAT Tasks v2", record_id, 
                                 {"Status": status})
    
    # Daily Habits
    def get_habits(self, days: int = 7) -> List[Dict]:
        """Get habit entries"""
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        filter_formula = f"IS_AFTER({{Date}}, '{start_date}')"
        
        return self.query_records(self.base_id, "Daily Habits",
                                 filter_formula=filter_formula,
                                 sort=[{"field": "Date", "direction": "desc"}])
    
    def add_habit(self, habit_name: str, completed: bool = True,
                 date: Optional[str] = None) -> Dict:
        """Add a habit entry"""
        fields = {
            "Habit": habit_name,
            "Completed": completed,
            "Date": date or datetime.now().strftime('%Y-%m-%d')
        }
        
        return self.create_record(self.base_id, "Daily Habits", fields)


# Health Base Specific Methods
class HealthAirtableClient(AirtableClient):
    """Client specifically for Health & Nutrition base"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_id = HEALTH_BASE_ID
    
    # Food Log
    def get_food_entries(self, date: Optional[str] = None, days: int = 7) -> List[Dict]:
        """Get food entries for a date range"""
        # Get last N days and filter locally
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        filter_formula = f"{{Date}} >= '{start_date}'"
        
        records = self.query_records(self.base_id, "Food Log", 
                                 filter_formula=filter_formula,
                                 sort=[{"field": "Date", "direction": "desc"}])
        
        # Filter by specific date if provided
        if date and records:
            records = [r for r in records if r['fields'].get('Date') == date]
        
        return records
    
    def add_food_entry(self, food_name: str, calories: Optional[int] = None,
                      protein: Optional[float] = None, carbs: Optional[float] = None,
                      fat: Optional[float] = None, meal_type: str = "Snack",
                      date: Optional[str] = None) -> Dict:
        """Add a food entry"""
        fields = {
            "Food Name": food_name,
            "Meal Type": meal_type,
            "Date": date or datetime.now().strftime('%Y-%m-%d')
        }
        if calories:
            fields["Calories"] = calories
        if protein:
            fields["Protein (g)"] = protein
        if carbs:
            fields["Carbs (g)"] = carbs
        if fat:
            fields["Fat (g)"] = fat
        
        return self.create_record(self.base_id, "Food Log", fields)
    
    # Weight
    def get_weight_entries(self, days: int = 30) -> List[Dict]:
        """Get weight entries"""
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        filter_formula = f"IS_AFTER({{Date}}, '{start_date}')"
        
        return self.query_records(self.base_id, "Weight Tracker",
                                 filter_formula=filter_formula,
                                 sort=[{"field": "Date", "direction": "desc"}])
    
    def add_weight_entry(self, weight: float, date: Optional[str] = None,
                        notes: str = "") -> Dict:
        """Add a weight entry"""
        fields = {
            "Weight": weight,
            "Date": date or datetime.now().strftime('%Y-%m-%d')
        }
        if notes:
            fields["Notes"] = notes
        
        return self.create_record(self.base_id, "Weight Tracker", fields)
    
    # Workouts
    def get_workouts(self, days: int = 7) -> List[Dict]:
        """Get recent workouts"""
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        filter_formula = f"IS_AFTER({{Date}}, '{start_date}')"
        
        return self.query_records(self.base_id, "Workouts",
                                 filter_formula=filter_formula,
                                 sort=[{"field": "Date", "direction": "desc"}])
    
    def add_workout(self, workout_type: str, duration: int,
                   calories: Optional[int] = None, notes: str = "",
                   date: Optional[str] = None) -> Dict:
        """Add a workout entry"""
        fields = {
            "Workout Type": workout_type,
            "Duration (min)": duration,
            "Date": date or datetime.now().strftime('%Y-%m-%d')
        }
        if calories:
            fields["Calories Burned"] = calories
        if notes:
            fields["Notes"] = notes
        
        return self.create_record(self.base_id, "Workouts", fields)
    
    # Habits - use Productivity base
    def get_habits(self, days: int = 7) -> List[Dict]:
        """Get habit entries from Daily Habits table in Productivity base"""
        prod_client = ProductivityAirtableClient(self.api_key)
        return prod_client.get_habits(days=days)
    
    def add_habit(self, habit_name: str, completed: bool = True,
                 date: Optional[str] = None) -> Dict:
        """Add a habit entry"""
        prod_client = ProductivityAirtableClient(self.api_key)
        return prod_client.add_habit(habit_name, completed, date)
    
    # WHOOP Data
    def save_whoop_recovery(self, recovery_score: int, hrv: Optional[float] = None,
                           resting_hr: Optional[int] = None, date: Optional[str] = None) -> Dict:
        """Save WHOOP recovery data"""
        fields = {
            "Recovery Score": recovery_score,
            "Date": date or datetime.now().strftime('%Y-%m-%d')
        }
        if hrv:
            fields["HRV"] = hrv
        if resting_hr:
            fields["Resting HR"] = resting_hr
        
        return self.create_record(self.base_id, "WHOOP Data", fields)
    
    def save_whoop_sleep(self, sleep_performance: float, duration_hours: float,
                        efficiency: Optional[float] = None, date: Optional[str] = None) -> Dict:
        """Save WHOOP sleep data"""
        fields = {
            "Sleep Performance": sleep_performance,
            "Sleep Duration": duration_hours,
            "Date": date or datetime.now().strftime('%Y-%m-%d')
        }
        if efficiency:
            fields["Sleep Efficiency"] = efficiency
        
        return self.create_record(self.base_id, "WHOOP Data", fields)


# Convenience function to get configured client
def get_health_client() -> HealthAirtableClient:
    """Get configured Health Airtable client"""
    return HealthAirtableClient()

def get_productivity_client() -> ProductivityAirtableClient:
    """Get configured Productivity Airtable client"""
    return ProductivityAirtableClient()


if __name__ == "__main__":
    # Test the client
    print("🧪 Testing Airtable Client...")
    
    try:
        # Test Health client
        health = get_health_client()
        print(f"✅ Health client initialized")
        
        # Test Productivity client
        productivity = get_productivity_client()
        print(f"✅ Productivity client initialized")
        
        # Test getting tables
        print("\n📊 Health Base Tables:")
        for table in health.get_tables(HEALTH_BASE_ID)[:5]:
            print(f"  - {table['name']}")
        
        print("\n📊 Productivity Base Tables:")
        for table in productivity.get_tables(PRODUCTIVITY_BASE_ID)[:5]:
            print(f"  - {table['name']}")
        
        print("\n✅ Airtable client working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
