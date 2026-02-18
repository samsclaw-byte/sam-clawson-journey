# Trak App Wireframes - Google Stitch Input Prompts

## Screen 1: Login Screen

**Prompt:**
```
Mobile app login screen for a nutrition tracking app called "Trak". Clean white background. Centered on screen: A large green gradient app icon (square with rounded corners, 80x80px) showing a leaf or food emoji. Below that, bold black text "Trak" as the app name. Underneath, smaller gray text "Simple nutrition tracking for busy people". Large white button with Google "G" logo on the left and text "Continue with Google" - button has subtle gray border. At the very bottom, small light gray text "By continuing, you agree to our Terms of Service and Privacy Policy". Minimalist design, lots of white space, friendly and approachable. iPhone mockup frame.
```

---

## Screen 2: Profile Setup

**Prompt:**
```
Mobile app profile setup screen. White background. At top: thin progress bar showing 50% complete in green. Large bold heading "Your Profile" with smaller gray subheading "Help us calculate your daily nutrition goals" below it. Form fields stacked vertically: "Name" label with rounded text input showing "Sarah". "Age" label with number input showing "34". "Weight" label with number input showing "70" and a toggle switch below showing "kg" selected (white button on green) vs "lbs" (gray). "Height" label with number input showing "170" and toggle "cm" vs "inches". "Gender" label with three equal-width buttons side by side: "Female" with female symbol (selected/green), "Male" with male symbol, "Prefer not to say". At bottom: Large green gradient button "Continue to Dashboard" and smaller gray text button "Skip for now" below it. Clean form design, rounded inputs, friendly green accent color. iPhone mockup frame.
```

---

## Screen 3: Dashboard (Main Screen)

**Prompt:**
```
Mobile app dashboard for nutrition tracking. White background. Top header: Left side large bold text "Hello, Sarah! 👋", right side circular profile avatar with letter "S" in green circle. Below header: Large green gradient card (rounded corners, spans full width) with white text. Card shows "Today's Calories" label with gear/settings icon top-right. Large bold numbers "1,450 / 2,200" showing calories consumed vs goal. Below that, white progress bar showing 65% filled. Small text "65% of daily goal • 750 remaining". Below card: Section header "Today's Meals" with "See all" link on right. Three meal cards stacked vertically with light gray background, rounded corners, green left border accent. Each card shows: meal type in green (Breakfast, Lunch, Snack), time in gray (8:30 AM, 1:00 PM, 4:00 PM), meal name in black, calories in gray. Below meals: "Macronutrients" section with colorful donut chart showing carbs (green), protein (blue), fat (orange) segments. Legend below chart. Bottom right corner: Floating green circular "+" button for adding meals. Clean, modern, iOS-style design. iPhone mockup frame.
```

---

## Screen 4: Add Meal (Modal/Bottom Sheet)

**Prompt:**
```
Mobile app bottom sheet modal sliding up from bottom, dark overlay on background. White rounded-top card. Header: "Log a Meal" with X close button top-right. Form fields: "Meal Type" label with horizontal scrollable pill buttons: Breakfast (selected/green), Lunch, Dinner, Snack. "What did you eat?" label with large rounded text input area (multiline, placeholder "e.g., Chicken salad sandwich"). "Calories (optional)" label with number input showing placeholder "Auto-estimate or enter manually". "Time" label with time picker showing current time. Large green gradient button "Save Meal" full width at bottom. Clean white background, green accent color, rounded inputs, friendly and quick to use. iPhone mockup frame with bottom sheet.
```

---

## Screen 5: Meal Detail / Edit

**Prompt:**
```
Mobile app meal detail screen. White background. Top navigation bar: Back arrow left, "Meal Details" centered, Edit button right. Large card showing: Meal type badge "Lunch" in green pill. Large bold meal name "Chicken Salad Sandwich". Time "Today at 1:00 PM" in gray. Large calorie number "650" with "calories" label below. Section "Nutrition Estimate" with three items in a row: Carbs 45g with progress bar, Protein 35g with progress bar, Fat 22g with progress bar. "Ingredients detected" list showing: Grilled chicken, Mixed greens, Whole grain bread, Light mayo. At bottom: Two buttons side by side - "Edit Meal" (green outline) and "Delete" (red text). Clean, informative, easy to scan. iPhone mockup frame.
```

---

## Screen 6: Weekly Summary

**Prompt:**
```
Mobile app weekly summary screen. White background. Top: "This Week" title with date range "Feb 12-18" below. Large summary card with light green background showing: "Average Daily Calories" big number "1,890", small text "Goal: 2,200". Horizontal bar chart showing 7 days (Mon-Sun) with green bars of varying heights representing daily calories. Below chart: Day labels Mon, Tue, Wed, Thu, Fri, Sat, Sun. Summary stats in row: "Logged 42 meals" with checkmark icon, "On track 5/7 days" with green indicator, "Avg 1,890 cal/day". Section "Best Day" showing: "Wednesday Feb 14" with "2,100 cal • All meals logged". Section "Needs Work" showing: "Saturday Feb 17" with "2,800 cal • Over goal". Motivational message at bottom: "You're building healthy habits! 🎉". Clean data visualization, encouraging tone, green and white color scheme. iPhone mockup frame.
```

---

## Screen 7: Settings

**Prompt:**
```
Mobile app settings screen. White background. Top: "Settings" title. List of settings options with icons, each as a row with right arrow: Profile (person icon), Daily Goal (target icon, shows "2,200 cal" on right), Notifications (bell icon, toggle switch on right), Units (scale icon, shows "Metric" on right), Connected Apps (link icon), Help & Support (question mark icon), About (info icon), Sign Out (logout icon in red text). Each row has light gray background, rounded corners, padding. Dividers between sections: "Account", "Preferences", "Support". At bottom: App version "Trak v1.0.0" and "Made with 💚". Clean iOS-style settings, green accent for toggles, gray icons. iPhone mockup frame.
```

---

## Design System Tokens for Stitch

**Colors:**
- Primary Green: #22c55e (buttons, accents, progress)
- Primary Green Dark: #16a34a (gradients)
- Background: #ffffff (white)
- Card Background: #f9fafb (light gray)
- Text Primary: #1a1a2e (near black)
- Text Secondary: #666666 (gray)
- Text Tertiary: #9ca3af (light gray)
- Success: #22c55e
- Error: #ef4444 (red)
- Warning: #f59e0b (orange)
- Info: #3b82f6 (blue)

**Typography:**
- Font: System font (SF Pro / Roboto)
- Heading: 24px bold
- Subheading: 16px regular
- Body: 14px regular
- Caption: 12px regular

**Spacing:**
- Screen padding: 24px
- Card padding: 16-20px
- Section gaps: 24px
- Element gaps: 12-16px

**Components:**
- Buttons: 16px padding, 12px border-radius, full width for primary actions
- Inputs: 16px padding, 12px border-radius, 2px border #e5e7eb
- Cards: 12-16px border-radius, subtle shadow
- Icons: 24px for navigation, 20px for inline
