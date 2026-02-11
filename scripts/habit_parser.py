#!/usr/bin/env python3
"""
Natural Language Habit Parser for OpenClaw
Auto-detects habit mentions and updates Notion
"""

import re
import sys
import os

# Add workspace to path
sys.path.insert(0, '/home/samsclaw/.openclaw/workspace')

# Habit detection patterns
HABIT_PATTERNS = {
    'water': {
        'keywords': ['water', 'glass', 'glasses', 'drank', 'drink', 'hydrated'],
        'number_patterns': [
            r'(\d+)\s*glass(?:es)?',
            r'(\d+)\s*more',
            r'total\s*(?:of\s*)?(\d+)',
            r'(\d+)\s*total',
            r'had\s*(\d+)',
        ],
        'database_field': 'Water',
        'type': 'increment'
    },
    'exercise': {
        'keywords': ['run', 'running', 'ran', 'swim', 'swam', 'swimming', 'cycle', 'cycling', 'cycled', 'walk', 'walking', 'walked', 'exercise', 'exercising', 'workout', 'training', 'gym', 'yoga', 'pilates'],
        'number_patterns': [
            r'(\d+)\s*(?:min|minute|minutes)',
            r'(\d+)\s*(?:km|kilometer|kilometers|mile|miles)',
            r'for\s*(\d+)',
        ],
        'database_field': 'Exercise',
        'type': 'boolean',
        'duration_field': 'Exercise Duration (min)'
    },
    'fruit': {
        'keywords': ['fruit', 'apple', 'banana', 'orange', 'berries', ' portions', 'servings'],
        'number_patterns': [
            r'(\d+)\s*(?:portion|portions|serving|servings?)',
            r'(\d+)\s*(?:piece|pieces)',
        ],
        'database_field': 'Fruit',
        'type': 'boolean'
    },
    'multivitamin': {
        'keywords': ['vitamin', 'multi', 'multivitamin', 'supplement', 'pill', 'tablet'],
        'number_patterns': [],
        'database_field': 'Multivitamin',
        'type': 'boolean'
    }
}

def parse_habit_update(message):
    """Parse a message for habit updates"""
    message_lower = message.lower()
    updates = []
    
    for habit_name, config in HABIT_PATTERNS.items():
        # Check if any keyword is present (with word boundaries for short words)
        found = False
        for keyword in config['keywords']:
            if len(keyword) <= 4:
                # Use word boundaries for short words
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, message_lower):
                    found = True
                    break
            else:
                if keyword in message_lower:
                    found = True
                    break
        
        if found:
            update = {
                'habit': habit_name,
                'field': config['database_field'],
                'type': config['type']
            }
            
            # Try to extract number
            value = None
            for pattern in config['number_patterns']:
                match = re.search(pattern, message_lower)
                if match:
                    value = int(match.group(1))
                    break
            
            if value:
                update['value'] = value
            
            # Special handling for specific phrases
            if habit_name == 'water':
                if 'another' in message_lower or 'more' in message_lower or '+' in message:
                    update['increment'] = True
            
            updates.append(update)
    
    return updates

def format_confirmation(updates):
    """Format confirmation message"""
    if not updates:
        return None
    
    confirmations = []
    for update in updates:
        habit = update['habit']
        if update['type'] == 'boolean':
            confirmations.append(f"✅ {habit.title()}")
        elif 'value' in update:
            if update.get('increment'):
                confirmations.append(f"🥤 {habit.title()}: +{update['value']}")
            else:
                confirmations.append(f"🥤 {habit.title()}: {update['value']}")
        else:
            confirmations.append(f"✅ {habit.title()}")
    
    return "Updated: " + " | ".join(confirmations)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 habit_parser.py '<message>'")
        sys.exit(1)
    
    message = sys.argv[1]
    updates = parse_habit_update(message)
    
    if updates:
        confirmation = format_confirmation(updates)
        print(confirmation)
        print("\nParsed updates:")
        for update in updates:
            print(f"  - {update}")
    else:
        print("No habit updates detected")
