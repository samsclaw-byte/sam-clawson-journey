# WHOOP API v2 Fix for Sleep & Workout Data

## The Problem
- WHOOP API v1 endpoints (`/developer/v1/sleep`, `/developer/v1/activity`) return 404
- Webhooks send notification IDs that don't match API resource IDs
- Need to use v2 endpoints with proper authentication

## The Solution

### 1. API Endpoint Mapping

| Data Type | v1 Endpoint (Broken) | v2 Endpoint (Working) |
|-----------|---------------------|----------------------|
| Sleep | `/developer/v1/sleep/{id}` | `/v2/activity/sleep/{sleepId}` |
| Workout | `/developer/v1/activity/{id}` | `/v2/activity/workout/{workoutId}` |
| Recovery | `/developer/v1/recovery/{id}` | `/v2/cycle/{cycleId}/recovery` |
| Cycles | `/developer/v1/cycle` | `/v2/cycle` (works) |

### 2. Updated API Client Code

```python
import requests
from datetime import datetime, timedelta

class WhoopAPIv2:
    BASE_URL = "https://api.prod.whoop.com"
    
    def __init__(self, access_token):
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_sleep(self, sleep_id):
        """Fetch sleep data from v2 API"""
        url = f"{self.BASE_URL}/v2/activity/sleep/{sleep_id}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_workout(self, workout_id):
        """Fetch workout data from v2 API"""
        url = f"{self.BASE_URL}/v2/activity/workout/{workout_id}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_recovery(self, cycle_id):
        """Fetch recovery via cycle endpoint"""
        url = f"{self.BASE_URL}/v2/cycle/{cycle_id}/recovery"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def list_recent_sleep(self, days=7):
        """List recent sleep (using cycle data)"""
        # v2 doesn't have direct list endpoint for sleep
        # Need to fetch cycles and extract sleep data
        cycles = self.get_cycles(days)
        sleep_data = []
        for cycle in cycles:
            if cycle.get('sleep'):
                sleep_data.append(cycle['sleep'])
        return sleep_data
    
    def list_recent_workouts(self, days=7):
        """List recent workouts (using cycle data)"""
        cycles = self.get_cycles(days)
        workouts = []
        for cycle in cycles:
            if cycle.get('workouts'):
                workouts.extend(cycle['workouts'])
        return workouts
    
    def get_cycles(self, days=7):
        """Fetch cycles (works in v1 and v2)"""
        url = f"{self.BASE_URL}/developer/v1/cycle"
        params = {
            'start': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
            'end': datetime.now().strftime('%Y-%m-%d')
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get('records', [])
        return []

# Usage example
api = WhoopAPIv2(access_token="your_token_here")

# Fetch specific sleep by ID
sleep = api.get_sleep("90447461-1680-49f2-a126-8a42c9befc59")

# Fetch specific workout by ID
workout = api.get_workout("workout-id-here")

# List all recent sleep
recent_sleep = api.list_recent_sleep(days=7)

# List all recent workouts
recent_workouts = api.list_recent_workouts(days=7)
```

### 3. Webhook Server Update

Update the webhook server to use v2 endpoints:

```python
def fetch_whoop_data_v2(endpoint, record_id, tokens):
    """Fetch data from WHOOP v2 API"""
    base_url = "https://api.prod.whoop.com"
    
    # Map event types to v2 endpoints
    endpoint_map = {
        'sleep': f'/v2/activity/sleep/{record_id}',
        'workout': f'/v2/activity/workout/{record_id}',
        'recovery': f'/v2/cycle/{record_id}/recovery',
    }
    
    url = base_url + endpoint_map.get(endpoint, '')
    headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 401:
        # Token expired, refresh and retry
        new_tokens = refresh_token(tokens['refresh_token'])
        headers = {'Authorization': f'Bearer {new_tokens["access_token"]}'}
        response = requests.get(url, headers=headers)
    
    return response.json() if response.status_code == 200 else None
```

### 4. Backfill Missing Data

To fetch historical sleep/workout data:

```python
# Fetch all cycles (includes linked sleep and workouts)
cycles = api.get_cycles(days=30)

for cycle in cycles:
    # Extract sleep data
    if cycle.get('sleep'):
        sleep = cycle['sleep']
        save_to_airtable('WHOOP Sleep', {
            'Date': sleep['start'][:10],
            'Sleep ID': sleep['id'],
            'Performance': sleep['score']['sleep_performance_percentage'],
            'Duration': sleep['score']['stage_summary']['total_in_bed_time_milli'] / 3600000,
        })
    
    # Extract workout data
    for workout in cycle.get('workouts', []):
        save_to_airtable('WHOOP Workouts', {
            'Date': workout['start'][:10],
            'Workout ID': workout['id'],
            'Sport': workout['sport_name'],
            'Strain': workout['score']['strain'],
            'Duration': workout['duration'] / 60000,
        })
```

### 5. Key Differences v1 vs v2

| Feature | v1 API | v2 API |
|---------|--------|--------|
| Base Path | `/developer/v1/` | `/v2/` |
| Sleep Endpoint | ❌ 404 | ✅ `/v2/activity/sleep/{id}` |
| Workout Endpoint | ❌ 404 | ✅ `/v2/activity/workout/{id}` |
| Cycle Endpoint | ✅ Works | ✅ Works |
| List Endpoints | ✅ Available | ❌ Use cycle data instead |
| Data Structure | Nested | Flatter |

### 6. Testing the Fix

```python
# Test script
from whoop_client import WhoopAPIv2

api = WhoopAPIv2(access_token="your_token")

# Test sleep
print("Testing sleep fetch...")
sleep = api.get_sleep("your-sleep-id")
print(f"Sleep data: {sleep}")

# Test workout
print("\nTesting workout fetch...")
workout = api.get_workout("your-workout-id")
print(f"Workout data: {workout}")

# Test cycles (includes sleep & workout refs)
print("\nTesting cycles...")
cycles = api.get_cycles(days=3)
for cycle in cycles:
    print(f"Cycle {cycle['id']}: Strain {cycle['score']['strain']}")
    if cycle.get('sleep'):
        print(f"  → Sleep: {cycle['sleep']['id']}")
    for workout in cycle.get('workouts', []):
        print(f"  → Workout: {workout['sport_name']}")
```

## Next Steps

1. **Update webhook server** to use v2 endpoints
2. **Test v2 API calls** with your tokens
3. **Backfill historical data** using cycle endpoint
4. **Save to Airtable** with proper field mapping

## Troubleshooting

**401 Unauthorized:**
- Token expired, refresh using `/oauth/oauth2/token`

**404 Not Found:**
- ID doesn't exist or wrong endpoint
- Use cycle endpoint to get valid IDs

**No Sleep/Workout Data:**
- Check if you actually recorded sleep/workouts in WHOOP
- Verify date range includes activity

---

*Last Updated: Feb 20, 2026*
