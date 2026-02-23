#!/usr/bin/env python3
"""Check water from memory file instead of Airtable"""

from datetime import datetime
from pathlib import Path

def check_water():
    memory_file = Path("/home/samsclaw/.openclaw/workspace/memory/2026-02-22.md")
    
    if not memory_file.exists():
        print("water: 0/8")
        return 0
    
    content = memory_file.read_text()
    
    # Parse water from memory
    if "Water:" in content:
        for line in content.split('\n'):
            if line.startswith("💧 Water:") or "Water:" in line:
                # Extract number
                import re
                match = re.search(r'(\d+)/8', line)
                if match:
                    water = int(match.group(1))
                    print(f"water: {water}/8")
                    return water
    
    print("water: 0/8")
    return 0

if __name__ == "__main__":
    check_water()
