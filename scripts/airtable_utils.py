"""
Airtable utility functions
"""

from datetime import datetime, timedelta

def get_date_range(days=7):
    """Get date range for queries"""
    end = datetime.now()
    start = end - timedelta(days=days)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def format_date(date_obj):
    """Format date for Airtable"""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime('%Y-%m-%d')
