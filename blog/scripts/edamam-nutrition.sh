#!/bin/bash
# Edamam Nutrition API Integration
# Auto-lookup nutrition data for food items

EDAMAM_APP_ID_FILE="$HOME/.config/edamam/app_id"
EDAMAM_API_KEY_FILE="$HOME/.config/edamam/api_key"

# Ensure secure directory exists
mkdir -p "$HOME/.config/edamam"
chmod 700 "$HOME/.config/edamam"

# Check if credentials exist
if [ ! -f "$EDAMAM_APP_ID_FILE" ] || [ ! -f "$EDAMAM_API_KEY_FILE" ]; then
    echo "❌ Edamam credentials not found"
    echo "Please run: ./setup-edamam.sh"
    exit 1
fi

APP_ID=$(cat "$EDAMAM_APP_ID_FILE")
API_KEY=$(cat "$EDAMAM_API_KEY_FILE")

# Function to analyze food
analyze_food() {
    local food="$1"
    
    echo "🔍 Analyzing: $food"
    
    # Call Edamam API
    response=$(curl -s "https://api.edamam.com/api/nutrition-data?app_id=$APP_ID&app_key=$API_KEY&ingr=$food" 2>/dev/null)
    
    # Parse response
    calories=$(echo "$response" | grep -o '"calories":[0-9]*' | cut -d':' -f2)
    protein=$(echo "$response" | grep -o '"PROCNT":[0-9.]*' | cut -d':' -f2)
    fat=$(echo "$response" | grep -o '"FAT":[0-9.]*' | cut -d':' -f2)
    carbs=$(echo "$response" | grep -o '"CHOCDF":[0-9.]*' | cut -d':' -f2)
    
    echo "📊 Results:"
    echo "  Calories: ${calories:-N/A} kcal"
    echo "  Protein: ${protein:-N/A}g"
    echo "  Carbs: ${carbs:-N/A}g"
    echo "  Fat: ${fat:-N/A}g"
}

# Main
if [ -z "$1" ]; then
    echo "Usage: $0 'food description'"
    echo "Example: $0 '1 cup rice'"
    exit 1
fi

analyze_food "$1"
