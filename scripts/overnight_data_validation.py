#!/usr/bin/env python3
"""
Overnight Data Validation for Airtable Tables
Runs at 2:00 AM daily via cron
Validates data integrity across all tracking tables
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

class DataValidator:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {AIRTABLE_KEY}",
            "Content-Type": "application/json"
        }
        self.validation_report = {
            "timestamp": datetime.now().isoformat(),
            "date_checked": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            "tables": {},
            "summary": {
                "total_issues": 0,
                "critical_issues": 0,
                "warnings": 0,
                "auto_fixed": 0
            }
        }
    
    # ============================================================================
    # FOOD LOG VALIDATIONS
    # ============================================================================
    def validate_food_log(self, date):
        """Validate Food Log table integrity"""
        print("\n" + "="*60)
        print("🍽️  VALIDATING FOOD LOG")
        print("="*60)
        
        url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
        issues = []
        warnings = []
        auto_fixed = 0
        
        try:
            # Get all records for the date
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'&maxRecords=50",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                issues.append(f"Cannot fetch Food Log: HTTP {response.status_code}")
                return {"status": "ERROR", "issues": issues, "warnings": warnings}
            
            records = response.json().get('records', [])
            
            # Validation 1: Check for required fields
            required_fields = ['Date', 'Meal Type', 'Food Items', 'Calories']
            for r in records:
                f = r.get('fields', {})
                for field in required_fields:
                    if field not in f or f[field] is None or f[field] == '':
                        issues.append(f"Record {r['id'][:10]}: Missing required field '{field}'")
            
            # Validation 2: Check Meal Type is valid
            valid_meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
            for r in records:
                f = r.get('fields', {})
                meal_type = f.get('Meal Type', '')
                if meal_type and meal_type not in valid_meal_types:
                    issues.append(f"Record {r['id'][:10]}: Invalid Meal Type '{meal_type}'")
            
            # Validation 3: Check Calories is positive number
            for r in records:
                f = r.get('fields', {})
                calories = f.get('Calories', 0)
                if calories is not None and (not isinstance(calories, (int, float)) or calories < 0):
                    issues.append(f"Record {r['id'][:10]}: Invalid Calories value '{calories}'")
            
            # Validation 4: Check for exact duplicates
            seen_meals = defaultdict(list)
            for r in records:
                f = r.get('fields', {})
                key = f"{f.get('Meal Type', '')}:{f.get('Food Items', '')[:30]}"
                seen_meals[key].append(r['id'])
            
            for key, ids in seen_meals.items():
                if len(ids) > 1:
                    issues.append(f"Duplicate meals found ({len(ids)} copies): {key}")
            
            # Validation 5: Edamam Data consistency
            # If Edamam Data = True, should have all 24 nutrients
            # If Edamam Data = False/empty, should at least have Calories
            for r in records:
                f = r.get('fields', {})
                has_edamam = f.get('Edamam Data', False)
                has_protein = f.get('Protein (g)')
                
                if has_edamam and not has_protein:
                    warnings.append(f"Record {r['id'][:10]}: Edamam Data=True but missing protein - data may be incomplete")
                elif not has_edamam and has_protein:
                    # Auto-fix: Set Edamam Data = True since we have protein data
                    try:
                        fix_resp = requests.patch(
                            f"{url}/{r['id']}",
                            headers=self.headers,
                            json={"fields": {"Edamam Data": True}},
                            timeout=10
                        )
                        if fix_resp.status_code == 200:
                            auto_fixed += 1
                    except:
                        pass
            
            # Validation 6: Check for orphaned records (no date)
            for r in records:
                f = r.get('fields', {})
                if 'Date' not in f or not f['Date']:
                    issues.append(f"Record {r['id'][:10]}: Missing Date (orphaned record)")
            
            # Validation 7: Nutrition totals seem reasonable
            total_calories = sum(r['fields'].get('Calories', 0) for r in records if 'Calories' in r['fields'])
            if total_calories > 5000:
                warnings.append(f"Total calories ({total_calories}) seems unusually high - verify entries")
            elif total_calories < 500 and len(records) > 0:
                warnings.append(f"Total calories ({total_calories}) seems unusually low - verify entries")
            
            result = {
                "status": "PASS" if not issues else "FAIL",
                "records_checked": len(records),
                "total_calories": total_calories,
                "issues": issues,
                "warnings": warnings,
                "auto_fixed": auto_fixed
            }
            
            print(f"  Records checked: {len(records)}")
            print(f"  Total calories: {total_calories}")
            print(f"  Issues: {len(issues)}")
            print(f"  Warnings: {len(warnings)}")
            print(f"  Auto-fixed: {auto_fixed}")
            
            return result
            
        except Exception as e:
            issues.append(f"Exception during validation: {str(e)}")
            return {"status": "ERROR", "issues": issues, "warnings": warnings}
    
    # ============================================================================
    # DAILY HABITS VALIDATIONS
    # ============================================================================
    def validate_daily_habits(self, date):
        """Validate Daily Habits table integrity"""
        print("\n" + "="*60)
        print("📊 VALIDATING DAILY HABITS")
        print("="*60)
        
        url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
        issues = []
        warnings = []
        
        try:
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'&maxRecords=10",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                issues.append(f"Cannot fetch Daily Habits: HTTP {response.status_code}")
                return {"status": "ERROR", "issues": issues, "warnings": warnings}
            
            records = response.json().get('records', [])
            
            # Validation 1: Check for duplicate dates
            if len(records) > 1:
                issues.append(f"Multiple habit records found for {date} ({len(records)} records) - should be unique per day")
            
            # Validation 2: Check data types
            for r in records:
                f = r.get('fields', {})
                
                # Water should be integer 0-20
                water = f.get('Water')
                if water is not None:
                    if not isinstance(water, (int, float)):
                        issues.append(f"Record {r['id'][:10]}: Water field should be numeric")
                    elif water < 0 or water > 20:
                        warnings.append(f"Record {r['id'][:10]}: Water value ({water}) seems unusual")
                
                # Boolean fields should be boolean
                boolean_fields = ['Multivitamin', 'Fruit', 'Exercise', 'Creatine']
                for field in boolean_fields:
                    value = f.get(field)
                    if value is not None and not isinstance(value, bool):
                        issues.append(f"Record {r['id'][:10]}: {field} should be boolean (checkbox)")
            
            # Validation 3: Check for missing record
            if not records:
                warnings.append(f"No habit record found for {date}")
            
            # Validation 4: Cross-reference with Food Log
            food_issues = self._cross_validate_habits_food(date)
            issues.extend(food_issues)
            
            result = {
                "status": "PASS" if not issues else "FAIL",
                "records_checked": len(records),
                "issues": issues,
                "warnings": warnings
            }
            
            print(f"  Records checked: {len(records)}")
            print(f"  Issues: {len(issues)}")
            print(f"  Warnings: {len(warnings)}")
            
            return result
            
        except Exception as e:
            issues.append(f"Exception during validation: {str(e)}")
            return {"status": "ERROR", "issues": issues, "warnings": warnings}
    
    def _cross_validate_habits_food(self, date):
        """Cross-validate habits with food log"""
        issues = []
        
        try:
            # Get habits
            habits_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
            habits_resp = requests.get(
                f"{habits_url}?filterByFormula=Date='{date}'",
                headers=self.headers,
                timeout=10
            )
            
            if habits_resp.status_code != 200:
                return issues
            
            habits_records = habits_resp.json().get('records', [])
            if not habits_records:
                return issues
            
            habits = habits_records[0]['fields']
            
            # Get food log
            food_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
            food_resp = requests.get(
                f"{food_url}?filterByFormula=Date='{date}'",
                headers=self.headers,
                timeout=10
            )
            
            if food_resp.status_code != 200:
                return issues
            
            food_records = food_resp.json().get('records', [])
            food_text = ' '.join([r['fields'].get('Food Items', '') for r in food_records]).lower()
            
            # Check: If multivitamin in food log, should be checked in habits
            if 'multivitamin' in food_text and not habits.get('Multivitamin'):
                issues.append("Multivitamin found in Food Log but not checked in Daily Habits")
            
            # Check: If fruit in food log, should be checked in habits
            fruit_keywords = ['apple', 'banana', 'date', 'fruit', 'berry']
            has_fruit_in_food = any(f in food_text for f in fruit_keywords)
            if has_fruit_in_food and not habits.get('Fruit'):
                issues.append("Fruit found in Food Log but not checked in Daily Habits")
            
        except Exception as e:
            pass
        
        return issues
    
    # ============================================================================
    # TAT TASKS VALIDATIONS
    # ============================================================================
    def validate_tat_tasks(self, date):
        """Validate TAT Tasks table integrity"""
        print("\n" + "="*60)
        print("📋 VALIDATING TAT TASKS")
        print("="*60)
        
        url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblkbuvkZUSpm1IgJ"
        issues = []
        warnings = []
        
        try:
            # Get tasks created on this date
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'&maxRecords=50",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                issues.append(f"Cannot fetch TAT Tasks: HTTP {response.status_code}")
                return {"status": "ERROR", "issues": issues, "warnings": warnings}
            
            records = response.json().get('records', [])
            
            # Validation 1: Check for required fields
            required_fields = ['Task Name', 'Category', 'Status']
            for r in records:
                f = r.get('fields', {})
                for field in required_fields:
                    if field not in f or f[field] is None or f[field] == '':
                        issues.append(f"Record {r['id'][:10]}: Missing required field '{field}'")
            
            # Validation 2: Validate Category values
            valid_categories = ['1', '3', '7', '30']
            for r in records:
                f = r.get('fields', {})
                category = f.get('Category', '')
                if category and category not in valid_categories:
                    issues.append(f"Record {r['id'][:10]}: Invalid Category '{category}'")
            
            # Validation 3: Validate Status values
            valid_statuses = ['Not Started', 'In Progress', 'Blocked', 'Complete', 'Cancelled']
            for r in records:
                f = r.get('fields', {})
                status = f.get('Status', '')
                if status and status not in valid_statuses:
                    issues.append(f"Record {r['id'][:10]}: Invalid Status '{status}'")
            
            # Validation 4: Check Due Date formula correctness
            for r in records:
                f = r.get('fields', {})
                date_created = f.get('Date Created')
                category = f.get('Category')
                due_date = f.get('Due Date')
                
                if date_created and category and due_date:
                    # Calculate expected due date
                    try:
                        created = datetime.fromisoformat(date_created.replace('Z', '+00:00'))
                        expected_due = created + timedelta(days=int(category))
                        actual_due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                        
                        if abs((expected_due - actual_due).days) > 1:
                            issues.append(f"Record {r['id'][:10]}: Due Date doesn't match formula (Category={category})")
                    except:
                        pass
            
            # Validation 5: Check for overdue tasks without status update
            for r in records:
                f = r.get('fields', {})
                days_remaining = f.get('Days Remaining')
                status = f.get('Status', '')
                
                if days_remaining is not None and days_remaining < 0 and status not in ['Complete', 'Cancelled']:
                    warnings.append(f"Record {r['id'][:10]}: Task is overdue ({days_remaining} days) but status is '{status}'")
            
            result = {
                "status": "PASS" if not issues else "FAIL",
                "records_checked": len(records),
                "issues": issues,
                "warnings": warnings
            }
            
            print(f"  Records checked: {len(records)}")
            print(f"  Issues: {len(issues)}")
            print(f"  Warnings: {len(warnings)}")
            
            return result
            
        except Exception as e:
            issues.append(f"Exception during validation: {str(e)}")
            return {"status": "ERROR", "issues": issues, "warnings": warnings}
    
    # ============================================================================
    # GENERATE VALIDATION REPORT
    # ============================================================================
    def generate_report(self):
        """Generate final validation report"""
        print("\n" + "="*60)
        print("📊 GENERATING VALIDATION REPORT")
        print("="*60)
        
        # Calculate summary
        total_issues = 0
        total_warnings = 0
        total_auto_fixed = 0
        
        for table_name, result in self.validation_report['tables'].items():
            total_issues += len(result.get('issues', []))
            total_warnings += len(result.get('warnings', []))
            total_auto_fixed += result.get('auto_fixed', 0)
        
        self.validation_report['summary'] = {
            "total_issues": total_issues,
            "critical_issues": total_issues,  # All issues are considered critical for now
            "warnings": total_warnings,
            "auto_fixed": total_auto_fixed,
            "overall_status": "PASS" if total_issues == 0 else "FAIL"
        }
        
        # Save report to file
        report_file = f'/home/samsclaw/.openclaw/workspace/data/validation_report_{self.validation_report["date_checked"]}.json'
        with open(report_file, 'w') as f:
            json.dump(self.validation_report, f, indent=2)
        
        print(f"  Total issues: {total_issues}")
        print(f"  Warnings: {total_warnings}")
        print(f"  Auto-fixed: {total_auto_fixed}")
        print(f"  Overall status: {self.validation_report['summary']['overall_status']}")
        print(f"  Report saved: {report_file}")
        
        return self.validation_report
    
    # ============================================================================
    # SEND MORNING REPORT
    # ============================================================================
    def send_morning_report(self, report):
        """Send validation report summary to user"""
        summary = report['summary']
        date = report['date_checked']
        
        # Build message
        if summary['overall_status'] == 'PASS':
            icon = "✅"
            status_text = "All validations passed!"
        else:
            icon = "⚠️"
            status_text = f"{summary['total_issues']} issue(s) found"
        
        message = f"""{icon} **Overnight Data Validation - {date}**

**Overall Status:** {status_text}

**Summary:**
• Records checked: Food Log, Daily Habits, TAT Tasks
• Issues found: {summary['total_issues']}
• Warnings: {summary['warnings']}
• Auto-fixed: {summary['auto_fixed']}

"""
        
        # Add details for tables with issues
        for table_name, result in report['tables'].items():
            if result['issues'] or result['warnings']:
                message += f"\n**{table_name}:**\n"
                for issue in result['issues'][:5]:  # Show max 5 issues per table
                    message += f"• ❌ {issue}\n"
                for warning in result['warnings'][:3]:  # Show max 3 warnings
                    message += f"• ⚠️ {warning}\n"
        
        if summary['overall_status'] == 'PASS':
            message += "\n🎉 All data integrity checks passed! Your tables are in good shape."
        else:
            message += "\n💡 Review the issues above. Critical items may need manual correction."
        
        # Send via Telegram (using message tool)
        try:
            # This would call the message tool in actual implementation
            print(f"\nMorning report generated:\n{message}")
            return message
        except Exception as e:
            print(f"Failed to send report: {e}")
            return None
    
    # ============================================================================
    # MAIN VALIDATION RUN
    # ============================================================================
    def run_validations(self, date=None):
        """Run all validations for a given date"""
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        print("="*60)
        print(f"🔍 OVERNIGHT DATA VALIDATION - {date}")
        print("="*60)
        
        # Run validations for each table
        self.validation_report['tables']['Food Log'] = self.validate_food_log(date)
        self.validation_report['tables']['Daily Habits'] = self.validate_daily_habits(date)
        self.validation_report['tables']['TAT Tasks'] = self.validate_tat_tasks(date)
        
        # Generate report
        report = self.generate_report()
        
        # Send morning summary
        self.send_morning_report(report)
        
        return report

# ============================================================================
# Main execution
# ============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Overnight Data Validation')
    parser.add_argument('--date', help='Date to validate (YYYY-MM-DD)', default=None)
    parser.add_argument('--report-only', action='store_true', help='Only generate report from last run')
    
    args = parser.parse_args()
    
    validator = DataValidator()
    
    if args.report_only:
        # Just read and display last report
        date = args.date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        report_file = f'/home/samsclaw/.openclaw/workspace/data/validation_report_{date}.json'
        if os.path.exists(report_file):
            with open(report_file) as f:
                report = json.load(f)
            validator.send_morning_report(report)
        else:
            print(f"No report found for {date}")
    else:
        # Run full validation
        validator.run_validations(args.date)
