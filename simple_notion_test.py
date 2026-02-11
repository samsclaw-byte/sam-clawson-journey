#!/usr/bin/env python3
import requests
import os

# Your token
NOTION_TOKEN = os.environ.get('NOTION_TOKEN', 'YOUR_TOKEN_HERE')
headers = {
    \"Authorization\": f\"Bearer {NOTION_TOKEN}\",
    \"Notion-Version\": \"2022-06-28\",
    \"Content-Type\": \"application/json\"
}

# Test 1: Basic connectivity
