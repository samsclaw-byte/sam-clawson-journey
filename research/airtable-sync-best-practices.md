# Airtable Sync Best Practices

## Overview

This document outlines best practices for syncing data between OpenClaw workflows and Airtable, including error handling, rate limiting, conflict resolution, and recommendations for bidirectional sync.

---

## Rate Limiting

### Airtable API Limits
- **Standard Plan**: 5 requests per second per base
- **Enterprise Plan**: 50 requests per second per base
- **Burst Capacity**: Brief spikes allowed but sustained high rates will be throttled

### Implementation Strategy

```python
# Built-in rate limiting in airtable_client.py
import time

def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
    """Make API request with rate limiting and error handling"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, headers=self.headers, timeout=30, **kwargs)
            
            # Handle rate limiting (429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"⚠️ Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue
            
            # Handle other errors
            if response.status_code >= 400:
                raise Exception(f"Airtable API error: {response.status_code}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
            else:
                raise
```

### Recommendations
1. **Batch Operations**: Group multiple records into single API calls when possible
2. **Exponential Backoff**: Increase delay between retries (1s, 2s, 4s)
3. **Request Queuing**: Queue requests during high-traffic periods
4. **Caching**: Cache table IDs and schema to reduce metadata requests

---

## Error Handling

### Common Error Types

| Error Code | Description | Handling Strategy |
|------------|-------------|-------------------|
| 401 | Unauthorized | Check API key, re-authenticate |
| 403 | Forbidden | Check permissions on base/table |
| 404 | Not Found | Table/record doesn't exist |
| 422 | Invalid Request | Validate field types and data |
| 429 | Rate Limited | Implement backoff and retry |
| 500 | Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Wait and retry |

### Error Handling Pattern

```python
class AirtableSyncError(Exception):
    """Base exception for sync errors"""
    pass

class RecordNotFoundError(AirtableSyncError):
    """Record not found in Airtable"""
    pass

class ValidationError(AirtableSyncError):
    """Data validation failed"""
    pass

def safe_sync(operation, *args, **kwargs):
    """Wrapper for safe sync operations with comprehensive error handling"""
    try:
        return operation(*args, **kwargs)
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        
        if status_code == 404:
            raise RecordNotFoundError(f"Record not found: {e}")
        elif status_code == 422:
            raise ValidationError(f"Validation failed: {e}")
        elif status_code == 429:
            # Already handled by retry logic
            raise AirtableSyncError(f"Rate limit exceeded: {e}")
        else:
            raise AirtableSyncError(f"HTTP {status_code}: {e}")
    except requests.exceptions.RequestException as e:
        raise AirtableSyncError(f"Network error: {e}")
    except Exception as e:
        raise AirtableSyncError(f"Unexpected error: {e}")
```

---

## Conflict Resolution

### Conflict Scenarios

1. **Simultaneous Updates**: Two sources update the same record
2. **Offline Changes**: Changes made while disconnected
3. **Schema Changes**: Field modifications in Airtable
4. **Data Type Mismatches**: Type coercion failures

### Conflict Resolution Strategies

#### 1. Last-Write-Wins (Default)
```python
def update_with_timestamp(record_id, fields):
    """Update record with automatic timestamp"""
    fields['Last Modified'] = datetime.now().isoformat()
    return client.update_record(base_id, table_name, record_id, fields)
```

#### 2. Optimistic Locking
```python
def update_with_version(record_id, fields, expected_version):
    """Update only if version matches"""
    current = client.get_record(base_id, table_name, record_id)
    if current['fields'].get('Version') != expected_version:
        raise ConflictError("Record was modified by another process")
    
    fields['Version'] = expected_version + 1
    return client.update_record(base_id, table_name, record_id, fields)
```

#### 3. Merge Strategy
```python
def merge_records(local_data, remote_data):
    """Intelligently merge conflicting records"""
    merged = remote_data.copy()
    
    for key, local_value in local_data.items():
        if key not in merged:
            merged[key] = local_value
        elif isinstance(local_value, (int, float)):
            # For numeric fields, take the maximum (e.g., habit counts)
            merged[key] = max(merged[key], local_value)
        elif isinstance(local_value, str) and len(local_value) > len(merged.get(key, '')):
            # For text fields, take the longer/more detailed
            merged[key] = local_value
    
    return merged
```

---

## Bidirectional Sync Recommendations

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Local     │◄───►│   Sync      │◄───►│  Airtable   │
│   System    │     │   Engine    │     │   Cloud     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │  Queue  │   │  Cache  │
              └─────────┘   └─────────┘
```

### Sync Engine Components

```python
class BidirectionalSync:
    """Handles bidirectional sync between local system and Airtable"""
    
    def __init__(self, client, sync_state_file):
        self.client = client
        self.sync_state_file = sync_state_file
        self.sync_state = self._load_sync_state()
        self.pending_queue = []
    
    def _load_sync_state(self):
        """Load last sync timestamps and checksums"""
        if os.path.exists(self.sync_state_file):
            with open(self.sync_state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_sync_state(self):
        """Persist sync state to disk"""
        with open(self.sync_state_file, 'w') as f:
            json.dump(self.sync_state, f, indent=2)
    
    def sync_to_airtable(self, table_name, local_records):
        """Push local changes to Airtable"""
        for record in local_records:
            if self._needs_update(record):
                try:
                    if 'airtable_id' in record:
                        # Update existing
                        self.client.update_record(
                            self.client.base_id, 
                            table_name, 
                            record['airtable_id'], 
                            record['fields']
                        )
                    else:
                        # Create new
                        result = self.client.create_record(
                            self.client.base_id,
                            table_name,
                            record['fields']
                        )
                        record['airtable_id'] = result['id']
                    
                    self._mark_synced(record)
                    
                except Exception as e:
                    self.pending_queue.append({
                        'operation': 'update',
                        'record': record,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        self._save_sync_state()
    
    def sync_from_airtable(self, table_name, since=None):
        """Pull changes from Airtable"""
        if not since:
            since = self.sync_state.get(table_name, {}).get('last_sync')
        
        filter_formula = None
        if since:
            filter_formula = f"IS_AFTER(LAST_MODIFIED_TIME(), '{since}')"
        
        records = self.client.query_records(
            self.client.base_id,
            table_name,
            filter_formula=filter_formula
        )
        
        self.sync_state[table_name] = {
            'last_sync': datetime.now().isoformat(),
            'record_count': len(records)
        }
        self._save_sync_state()
        
        return records
```

### Sync Best Practices

1. **Timestamp Tracking**: Always track `createdTime` and `LAST_MODIFIED_TIME()`
2. **Checksums**: Store MD5 checksums of records to detect changes
3. **Batch Operations**: Sync in batches of 10-100 records
4. **Queue Failed Operations**: Don't lose data on transient failures
5. **Idempotency**: Ensure operations can be retried safely
6. **Conflict Log**: Maintain a log of all conflicts and resolutions

---

## Data Validation

### Schema Validation

```python
from datetime import datetime
from typing import Any, Dict

class FieldValidator:
    """Validate field types before sending to Airtable"""
    
    VALIDATORS = {
        'singleLineText': lambda x: isinstance(x, str) and len(x) <= 1000,
        'multilineText': lambda x: isinstance(x, str) and len(x) <= 100000,
        'number': lambda x: isinstance(x, (int, float)),
        'checkbox': lambda x: isinstance(x, bool),
        'date': lambda x: isinstance(x, str) and self._is_valid_date(x),
        'email': lambda x: isinstance(x, str) and '@' in x,
        'url': lambda x: isinstance(x, str) and x.startswith('http'),
        'select': lambda x: isinstance(x, str),
    }
    
    @staticmethod
    def _is_valid_date(date_str: str) -> bool:
        try:
            datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return True
        except:
            return False
    
    def validate_record(self, fields: Dict[str, Any], schema: Dict) -> tuple[bool, list]:
        """Validate all fields against schema"""
        errors = []
        
        for field_name, field_config in schema.items():
            if field_name not in fields:
                if field_config.get('required'):
                    errors.append(f"Required field missing: {field_name}")
                continue
            
            field_type = field_config.get('type')
            value = fields[field_name]
            
            if field_type in self.VALIDATORS:
                if not self.VALIDATORS[field_type](value):
                    errors.append(f"Invalid value for {field_name}: {value}")
        
        return len(errors) == 0, errors
```

---

## Security Considerations

### API Key Management
```python
# ~/.config/airtable/api_key
# - 0600 permissions (owner read/write only)
# - Never commit to git
# - Rotate quarterly

def load_api_key():
    """Securely load API key with permissions check"""
    key_path = os.path.expanduser("~/.config/airtable/api_key")
    
    # Check file permissions
    stat = os.stat(key_path)
    if stat.st_mode & 0o077:
        raise SecurityError("API key file has overly permissive permissions")
    
    with open(key_path, 'r') as f:
        return f.read().strip()
```

### Data Sanitization
```python
def sanitize_for_airtable(value: Any) -> Any:
    """Sanitize values before sending to Airtable"""
    if isinstance(value, str):
        # Remove control characters
        value = ''.join(char for char in value if ord(char) >= 32 or char == '\n')
        # Truncate long strings
        if len(value) > 100000:
            value = value[:100000] + "... [truncated]"
    return value
```

---

## Monitoring & Alerting

### Sync Health Metrics

```python
class SyncMonitor:
    """Monitor sync health and performance"""
    
    def __init__(self, log_file):
        self.log_file = log_file
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'rate_limited': 0,
            'avg_response_time': 0
        }
    
    def log_request(self, endpoint, status_code, duration):
        """Log API request metrics"""
        self.metrics['requests'] += 1
        
        if status_code >= 400:
            self.metrics['errors'] += 1
        
        if status_code == 429:
            self.metrics['rate_limited'] += 1
        
        # Update average response time
        total = self.metrics['avg_response_time'] * (self.metrics['requests'] - 1)
        self.metrics['avg_response_time'] = (total + duration) / self.metrics['requests']
        
        # Write to log
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()},{endpoint},{status_code},{duration}\n")
    
    def get_health_report(self):
        """Generate health report"""
        error_rate = self.metrics['errors'] / max(self.metrics['requests'], 1)
        
        return {
            'healthy': error_rate < 0.05,  # Less than 5% errors
            'error_rate': error_rate,
            'rate_limit_rate': self.metrics['rate_limited'] / max(self.metrics['requests'], 1),
            'avg_response_time': self.metrics['avg_response_time'],
            'total_requests': self.metrics['requests']
        }
```

---

## Testing Strategy

### Unit Tests
```python
import unittest
from unittest.mock import Mock, patch

class TestAirtableSync(unittest.TestCase):
    
    def setUp(self):
        self.client = AirtableClient(api_key="test_key")
    
    @patch('requests.request')
    def test_rate_limit_retry(self, mock_request):
        """Test that 429 responses trigger retry"""
        mock_request.side_effect = [
            Mock(status_code=429, headers={'Retry-After': '1'}),
            Mock(status_code=200, json=lambda: {'records': []})
        ]
        
        result = self.client.query_records("base123", "Table1")
        self.assertEqual(mock_request.call_count, 2)
    
    def test_conflict_resolution(self):
        """Test merge strategy for conflicting records"""
        local = {'calories': 500, 'protein': 30}
        remote = {'calories': 450, 'carbs': 50}
        
        merged = merge_records(local, remote)
        self.assertEqual(merged['calories'], 500)  # Takes max
        self.assertEqual(merged['protein'], 30)    # Adds missing
```

---

## Summary Checklist

- [ ] Implement rate limiting with exponential backoff
- [ ] Cache table IDs to reduce API calls
- [ ] Handle all HTTP error codes appropriately
- [ ] Queue failed operations for retry
- [ ] Track sync timestamps and checksums
- [ ] Validate data before sending to Airtable
- [ ] Implement conflict resolution strategy
- [ ] Secure API key storage (0600 permissions)
- [ ] Monitor sync health and performance
- [ ] Log all sync operations for debugging
- [ ] Write tests for sync logic
- [ ] Document schema changes

---

## Resources

- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [Airtable Rate Limits](https://airtable.com/developers/web/api/rate-limits)
- [pyAirtable Library](https://github.com/gtalarico/pyairtable)
