#!/usr/bin/env python3
"""Reorder cards in health-nutrition.html"""

with open('mission-control/health-nutrition.html', 'r') as f:
    content = f.read()

# Find the two cards
today_meals_start = content.find('<!-- Today\'s Meals -->')
macros_start = content.find('<!-- Macros Pie Chart -->')
timeline_start = content.find('<!-- 7-Day Timeline -->')

if today_meals_start == -1 or macros_start == -1 or timeline_start == -1:
    print("Could not find card markers")
    exit(1)

# Extract the cards
today_meals_card = content[today_meals_start:macros_start]
macros_card = content[macros_start:timeline_start]

# Reorder: put macros first, then today meals
new_section = macros_card + today_meals_card

# Replace in content
new_content = content[:today_meals_start] + new_section + content[timeline_start:]

with open('mission-control/health-nutrition.html', 'w') as f:
    f.write(new_content)

print("✅ Cards reordered: Macronutrient Breakdown now above Today's Meals")
