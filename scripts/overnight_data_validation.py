#!/usr/bin/env python3
"""
Overnight Data Validation for Airtable Tables - v2 with Severity Levels
Runs at 2:00 AM daily via cron
Validates data integrity across all tracking tables
Categorizes issues: SEVERE vs MINOR
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
                "total_records": 0,
                "severe_errors": 0,
                "minor_errors": 0,
                "warnings": 0,
                "auto_fixed": 0,
                "missing_fields_count": 0,
                "overall_status": "PASS"
            }
        }
    
    def classify_issue(self, issue_type, description):
        """
        Classify issue as SEVERE or MINOR
        SEVERE: Data corruption, missing required fields, duplicates
        MINOR: Missing optional data, recommendations, formatting
        """
        severe_keywords = [
            'missing required', 'cannot fetch', 'exception', 'duplicate', 
            'invalid', 'orphaned', 'multiple records', 'data type',
            'corrupt', 'empty', 'null'
        ]
        
        issue_lower = description.lower()
        if any(keyword in issue_lower for keyword in severe_keywords):
            return 'SEVERE'
        return 'MINOR'
    
    # ============================================================================
    # FOOD LOG VALIDATIONS
    # ============================================================================
    def validate_food_log(self, date):
        """Validate Food Log table integrity with field completeness checks"""
        print("\n" + "="*60)
        print("🍽️  VALIDATING FOOD LOG")
        print("="*60)
        
        url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
        severe_issues = []
        minor_issues = []
        warnings = []
        auto_fixed = 0
        missing_fields_total = 0
        
        # Define field completeness expectations
        required_fields = {
            'Date': 'Date of meal',
            'Meal Type': 'Type of meal (Breakfast/Lunch/Dinner/Snack)',
            'Food Items': 'Description of food consumed',
            'Calories': 'Calorie count'
        }
        
        optional_fields = {
            'Protein (g)': 'Protein content',
            'Carbs (g)': 'Carbohydrate content',
            'Fat (g)': 'Fat content',
            'Edamam Data': 'Whether data came from Edamam API'
        }
        
        try:
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'&maxRecords=50",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                severe_issues.append(f"SEVERE: Cannot fetch Food Log: HTTP {response.status_code}")
                return {
                    "status": "ERROR", 
                    "severe": severe_issues, 
                    "minor": minor_issues,
                    "warnings": warnings,
                    "missing_fields": 0
                }
            
            records = response.json().get('records', [])
            
            for r in records:
                f = r.get('fields', {})
                record_id = r['id'][:10]
                missing_in_record = 0
                
                # Check 1: Required fields - SEVERE if missing
                for field, description in required_fields.items():
                    if field not in f or f[field] is None or f[field] == '':
                        severe_issues.append(f"SEVERE: Record {record_id}: Missing required field '{field}' ({description})")
                        missing_in_record += 1
                
                # Check 2: Optional fields - MINOR if missing
                for field, description in optional_fields.items():
                    if field not in f or f[field] is None or f[field] == '':
                        minor_issues.append(f"MINOR: Record {record_id}: Missing optional field '{field}' ({description})")
                        missing_in_record += 1
                
                missing_fields_total += missing_in_record
                
                # Check 3: Data type validations - SEVERE
                meal_type = f.get('Meal Type', '')
                if meal_type and meal_type not in ['Breakfast', 'Lunch', 'Dinner', 'Snack']:
                    severe_issues.append(f"SEVERE: Record {record_id}: Invalid Meal Type '{meal_type}'")
                
                calories = f.get('Calories')
                if calories is not None:
                    if not isinstance(calories, (int, float)):
                        severe_issues.append(f"SEVERE: Record {record_id}: Calories must be numeric, got {type(calories)}")
                    elif calories < 0:
                        severe_issues.append(f"SEVERE: Record {record_id}: Calories cannot be negative ({calories})")
                    elif calories == 0:
                        warnings.append(f"⚠️ Record {record_id}: Calories is 0 - verify this is correct")
                
                # Check 4: Date format - SEVERE
                record_date = f.get('Date', '')
                if record_date:
                    try:
                        datetime.strptime(record_date, '%Y-%m-%d')
                    except:
                        severe_issues.append(f"SEVERE: Record {record_id}: Invalid Date format '{record_date}' (expected YYYY-MM-DD)")
            
            # Check 5: Duplicates - SEVERE
            seen_meals = defaultdict(list)
            for r in records:
                f = r.get('fields', {})
                key = f"{f.get('Date', '')}:{f.get('Meal Type', '')}:{f.get('Food Items', '')[:30]}"
                seen_meals[key].append(r['id'][:10])
            
            for key, ids in seen_meals.items():
                if len(ids) > 1:
                    severe_issues.append(f"SEVERE: Duplicate meals found ({len(ids)} copies with IDs: {', '.join(ids)}): {key[:50]}")
            
            # Check 6: Data quality warnings - MINOR
            total_calories = sum(r['fields'].get('Calories', 0) for r in records if 'Calories' in r['fields'])
            if total_calories > 5000:
                warnings.append(f"⚠️ Total calories ({total_calories}) unusually high - verify entries")
            elif total_calories < 500 and len(records) > 0:
                warnings.append(f"⚠️ Total calories ({total_calories}) unusually low - verify entries")
            
            # Check 7: Edamam Data consistency - MINOR
            for r in records:
                f = r.get('fields', {})
                has_edamam = f.get('Edamam Data', False)
                has_protein = f.get('Protein (g)')
                
                if has_edamam and not has_protein:
                    minor_issues.append(f"MINOR: Record {r['id'][:10]}: Edamam Data=True but missing protein - incomplete nutrition")
                elif not has_edamam and has_protein:
                    # Auto-fix
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
            
            result = {
                "status": "PASS" if not severe_issues else "FAIL",
                "records_checked": len(records),
                "total_calories": total_calories,
                "severe": severe_issues,
                "minor": minor_issues,
                "warnings": warnings,
                "auto_fixed": auto_fixed,
                "missing_fields": missing_fields_total
            }
            
            print(f"  Records checked: {len(records)}")
            print(f"  Severe issues: {len(severe_issues)}")
            print(f"  Minor issues: {len(minor_issues)}")
            print(f"  Warnings: {len(warnings)}")
            print(f"  Missing fields: {missing_fields_total}")
            print(f"  Auto-fixed: {auto_fixed}")
            
            return result
            
        except Exception as e:
            severe_issues.append(f"SEVERE: Exception during validation: {str(e)}")
            return {
                "status": "ERROR", 
                "severe": severe_issues, 
                "minor": minor_issues,
                "warnings": warnings,
                "missing_fields": 0
            }
    
    # ============================================================================
    # DAILY HABITS VALIDATIONS
    # ============================================================================
    def validate_daily_habits(self, date):
        """Validate Daily Habits table with field completeness checks"""
        print("\n" + "="*60)
        print("📊 VALIDATING DAILY HABITS")
        print("="*60)
        
        url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
        severe_issues = []
        minor_issues = []
        warnings = []
        missing_fields_total = 0
        
        required_fields = {
            'Date': 'Date of habit tracking'
        }
        
        optional_fields = {
            'Multivitamin': 'Multivitamin taken (checkbox)',
            'Fruit': 'Fruit consumed (checkbox)',
            'Exercise': 'Exercise completed (checkbox)',
            'Creatine': 'Creatine taken (checkbox)',
            'Water': 'Water intake (number of glasses)'
        }
        
        try:
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'&maxRecords=10",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                severe_issues.append(f"SEVERE: Cannot fetch Daily Habits: HTTP {response.status_code}")
                return {
                    "status": "ERROR", 
                    "severe": severe_issues, 
                    "minor": minor_issues,
                    "warnings": warnings,
                    "missing_fields": 0
                }
            
            records = response.json().get('records', [])
            
            # Check 1: Duplicate records - SEVERE
            if len(records) > 1:
                ids = [r['id'][:10] for r in records]
                severe_issues.append(f"SEVERE: Multiple habit records for {date} ({len(records)} records: {', '.join(ids)}) - should be unique per day")
            
            for r in records:
                f = r.get('fields', {})
                record_id = r['id'][:10]
                missing_in_record = 0
                
                # Check required fields
                for field, description in required_fields.items():
                    if field not in f or not f[field]:
                        severe_issues.append(f"SEVERE: Record {record_id}: Missing required field '{field}' ({description})")
                        missing_in_record += 1
                
                # Check optional fields (minor)
                for field, description in optional_fields.items():
                    if field not in f:
                        minor_issues.append(f"MINOR: Record {record_id}: Missing field '{field}' ({description})")
                        missing_in_record += 1
                
                # Check data types
                water = f.get('Water')
                if water is not None:
                    if not isinstance(water, (int, float)):
                        severe_issues.append(f"SEVERE: Record {record_id}: Water must be numeric, got {type(water)}")
                    elif water < 0 or water > 20:
                        warnings.append(f"⚠️ Record {record_id}: Water value ({water}) seems unusual")
                
                # Check boolean fields
                boolean_fields = ['Multivitamin', 'Fruit', 'Exercise', 'Creatine']
                for field in boolean_fields:
                    value = f.get(field)
                    if value is not None and not isinstance(value, bool):
                        severe_issues.append(f"SEVERE: Record {record_id}: {field} should be boolean (checkbox), got {type(value)}")
                
                missing_fields_total += missing_in_record
            
            # Check 2: Missing record - WARNING
            if not records:
                warnings.append(f"⚠️ No habit record found for {date}")
            
            # Check 3: Cross-reference with Food Log - MINOR
            food_issues = self._cross_validate_habits_food(date)
            minor_issues.extend(food_issues)
            
            result = {
                "status": "PASS" if not severe_issues else "FAIL",
                "records_checked": len(records),
                "severe": severe_issues,
                "minor": minor_issues,
                "warnings": warnings,
                "missing_fields": missing_fields_total
            }
            
            print(f"  Records checked: {len(records)}")
            print(f"  Severe issues: {len(severe_issues)}")
            print(f"  Minor issues: {len(minor_issues)}")
            print(f"  Warnings: {len(warnings)}")
            print(f"  Missing fields: {missing_fields_total}")
            
            return result
            
        except Exception as e:
            severe_issues.append(f"SEVERE: Exception during validation: {str(e)}")
            return {
                "status": "ERROR", 
                "severe": severe_issues, 
                "minor": minor_issues,
                "warnings": warnings,
                "missing_fields": 0
            }
    
    def _cross_validate_habits_food(self, date):
        """Cross-validate habits with food log - returns minor issues"""
        minor_issues = []
        
        try:
            # Get habits
            habits_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
            habits_resp = requests.get(
                f"{habits_url}?filterByFormula=Date='{date}'",
                headers=self.headers,
                timeout=10
            )
            
            if habits_resp.status_code != 200:
                return minor_issues
            
            habits_records = habits_resp.json().get('records', [])
            if not habits_records:
                return minor_issues
            
            habits = habits_records[0]['fields']
            
            # Get food log
            food_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
            food_resp = requests.get(
                f"{food_url}?filterByFormula=Date='{date}'",
                headers=self.headers,
                timeout=10
            )
            
            if food_resp.status_code != 200:
                return minor_issues
            
            food_records = food_resp.json().get('records', [])
            food_text = ' '.join([r['fields'].get('Food Items', '') for r in food_records]).lower()
            
            # Check: If multivitamin in food log, should be checked in habits
            if 'multivitamin' in food_text and not habits.get('Multivitamin'):
                minor_issues.append("MINOR: Multivitamin found in Food Log but not checked in Daily Habits")
            
            # Check: If fruit in food log, should be checked in habits
            fruit_keywords = ['apple', 'banana', 'date', 'fruit', 'berry']
            has_fruit_in_food = any(f in food_text for f in fruit_keywords)
            if has_fruit_in_food and not habits.get('Fruit'):
                minor_issues.append("MINOR: Fruit found in Food Log but not checked in Daily Habits")
            
        except Exception as e:
            pass
        
        return minor_issues
    
    # ============================================================================
    # TAT TASKS VALIDATIONS
    # ============================================================================
    def validate_tat_tasks(self, date):
        """Validate TAT Tasks table with field completeness checks"""
        print("\n" + "="*60)
        print("📋 VALIDATING TAT TASKS")
        print("="*60)
        
        url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblkbuvkZUSpm1IgJ"
        severe_issues = []
        minor_issues = []
        warnings = []
        missing_fields_total = 0
        
        required_fields = {
            'Task Name': 'Description of the task',
            'Category': 'TAT category (1/3/7/30 days)',
            'Status': 'Current status of the task'
        }
        
        optional_fields = {
            'Priority': 'Task priority level',
            'Notes': 'Additional notes',
            'Tags': 'Task tags'
        }
        
        try:
            # TAT Tasks don't have a Date field - use Date Created instead
            # Get tasks created recently (last 7 days) or filter by Due Date
            from datetime import datetime, timedelta
            week_ago = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')
            response = requests.get(
                f"{url}?filterByFormula=IS_AFTER({{Date Created}}, '{week_ago}')&maxRecords=50",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                severe_issues.append(f"SEVERE: Cannot fetch TAT Tasks: HTTP {response.status_code}")
                return {
                    "status": "ERROR", 
                    "severe": severe_issues, 
                    "minor": minor_issues,
                    "warnings": warnings,
                    "missing_fields": 0
                }
            
            records = response.json().get('records', [])
            
            for r in records:
                f = r.get('fields', {})
                record_id = r['id'][:10]
                missing_in_record = 0
                
                # Check required fields
                for field, description in required_fields.items():
                    if field not in f or not f[field]:
                        severe_issues.append(f"SEVERE: Record {record_id}: Missing required field '{field}' ({description})")
                        missing_in_record += 1
                
                # Check optional fields
                for field, description in optional_fields.items():
                    if field not in f:
                        minor_issues.append(f"MINOR: Record {record_id}: Missing field '{field}' ({description})")
                        missing_in_record += 1
                
                # Check Category valid values
                category = f.get('Category', '')
                if category and category not in ['1', '3', '7', '30']:
                    severe_issues.append(f"SEVERE: Record {record_id}: Invalid Category '{category}' (must be 1, 3, 7, or 30)")
                
                # Check Status valid values
                status = f.get('Status', '')
                valid_statuses = ['Not Started', 'In Progress', 'Blocked', 'Complete', 'Cancelled']
                if status and status not in valid_statuses:
                    severe_issues.append(f"SEVERE: Record {record_id}: Invalid Status '{status}' (must be one of: {', '.join(valid_statuses)})")
                
                # Check Due Date formula
                date_created = f.get('Date Created')
                cat = f.get('Category')
                due_date = f.get('Due Date')
                
                if date_created and cat and due_date:
                    try:
                        created = datetime.fromisoformat(date_created.replace('Z', '+00:00'))
                        expected_due = created + timedelta(days=int(cat))
                        actual_due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                        
                        if abs((expected_due - actual_due).days) > 1:
                            severe_issues.append(f"SEVERE: Record {record_id}: Due Date formula error - expected {expected_due.date()}, got {actual_due.date()}")
                    except:
                        pass
                
                # Check overdue tasks
                days_remaining = f.get('Days Remaining')
                if days_remaining is not None and days_remaining < 0 and status not in ['Complete', 'Cancelled']:
                    warnings.append(f"⚠️ Record {record_id}: Task overdue ({days_remaining} days) with status '{status}'")
                
                missing_fields_total += missing_in_record
            
            result = {
                "status": "PASS" if not severe_issues else "FAIL",
                "records_checked": len(records),
                "severe": severe_issues,
                "minor": minor_issues,
                "warnings": warnings,
                "missing_fields": missing_fields_total
            }
            
            print(f"  Records checked: {len(records)}")
            print(f"  Severe issues: {len(severe_issues)}")
            print(f"  Minor issues: {len(minor_issues)}")
            print(f"  Warnings: {len(warnings)}")
            print(f"  Missing fields: {missing_fields_total}")
            
            return result
            
        except Exception as e:
            severe_issues.append(f"SEVERE: Exception during validation: {str(e)}")
            return {
                "status": "ERROR", 
                "severe": severe_issues, 
                "minor": minor_issues,
                "warnings": warnings,
                "missing_fields": 0
            }
    
    # ============================================================================
    # GENERATE VALIDATION REPORT
    # ============================================================================
    def generate_report(self):
        """Generate final validation report with severity counts"""
        print("\n" + "="*60)
        print("📊 GENERATING VALIDATION REPORT")
        print("="*60)
        
        # Calculate summary
        total_records = 0
        severe_count = 0
        minor_count = 0
        warning_count = 0
        auto_fixed_count = 0
        missing_fields_total = 0
        
        for table_name, result in self.validation_report['tables'].items():
            total_records += result.get('records_checked', 0)
            severe_count += len(result.get('severe', []))
            minor_count += len(result.get('minor', []))
            warning_count += len(result.get('warnings', []))
            auto_fixed_count += result.get('auto_fixed', 0)
            missing_fields_total += result.get('missing_fields', 0)
        
        self.validation_report['summary'] = {
            "total_records": total_records,
            "severe_errors": severe_count,
            "minor_errors": minor_count,
            "warnings": warning_count,
            "auto_fixed": auto_fixed_count,
            "missing_fields_count": missing_fields_total,
            "overall_status": "PASS" if severe_count == 0 else "FAIL"
        }
        
        # Save report to file
        report_file = f'/home/samsclaw/.openclaw/workspace/data/validation_report_{self.validation_report["date_checked"]}.json'
        with open(report_file, 'w') as f:
            json.dump(self.validation_report, f, indent=2)
        
        print(f"  Total records: {total_records}")
        print(f"  🔴 SEVERE errors: {severe_count}")
        print(f"  🟡 MINOR errors: {minor_count}")
        print(f"  ⚠️  Warnings: {warning_count}")
        print(f"  📝 Missing fields: {missing_fields_total}")
        print(f"  🔧 Auto-fixed: {auto_fixed_count}")
        print(f"  Overall: {self.validation_report['summary']['overall_status']}")
        print(f"  Report saved: {report_file}")
        
        return self.validation_report
    
    # ============================================================================
    # SEND MORNING REPORT
    # ============================================================================
    def send_morning_report(self, report):
        """Send validation report summary with severity breakdown"""
        summary = report['summary']
        date = report['date_checked']
        
        # Determine icon and status
        if summary['overall_status'] == 'PASS':
            icon = "✅"
            status_text = "All validations PASSED"
        elif summary['severe_errors'] > 0:
            icon = "🔴"
            status_text = f"{summary['severe_errors']} SEVERE error(s) found"
        else:
            icon = "🟡"
            status_text = f"{summary['minor_errors']} minor issue(s) found"
        
        message = f"""{icon} **Overnight Data Validation - {date}**

**Overall Status:** {status_text}

📊 **Summary:**
• Records checked: {summary['total_records']}
• 🔴 Severe errors: {summary['severe_errors']}
• 🟡 Minor errors: {summary['minor_errors']}
• ⚠️ Warnings: {summary['warnings']}
• 📝 Missing fields: {summary['missing_fields_count']}
• 🔧 Auto-fixed: {summary['auto_fixed']}

"""
        
        # Add details for tables with issues
        for table_name, result in report['tables'].items():
            if result.get('severe') or result.get('minor'):
                message += f"\n**{table_name}:**\n"
                
                # Show severe issues first
                for issue in result.get('severe', [])[:3]:
                    # Extract just the description part
                    issue_clean = issue.replace('SEVERE: ', '')
                    message += f"🔴 {issue_clean}\n"
                
                # Show minor issues
                for issue in result.get('minor', [])[:2]:
                    issue_clean = issue.replace('MINOR: ', '')
                    message += f"🟡 {issue_clean}\n"
                
                if len(result.get('severe', [])) > 3 or len(result.get('minor', [])) > 2:
                    message += f"... and {len(result.get('severe', [])) + len(result.get('minor', [])) - 5} more issues\n"
        
        if summary['overall_status'] == 'PASS':
            message += "\n🎉 All data integrity checks passed! Your tables are in good shape."
        elif summary['severe_errors'] > 0:
            message += "\n🔴 **Action Required:** Severe errors need manual correction."
            message += "\n💡 Minor issues can be addressed when convenient."
        else:
            message += "\n🟡 Minor issues found - no urgent action needed."
        
        print(f"\nMorning report:\n{message}")
        return message
    
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
    
    parser = argparse.ArgumentParser(description='Overnight Data Validation with Severity Levels')
    parser.add_argument('--date', help='Date to validate (YYYY-MM-DD)', default=None)
    parser.add_argument('--report-only', action='store_true', help='Only generate report from last run')
    
    args = parser.parse_args()
    
    validator = DataValidator()
    
    if args.report_only:
        date = args.date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        report_file = f'/home/samsclaw/.openclaw/workspace/data/validation_report_{date}.json'
        if os.path.exists(report_file):
            with open(report_file) as f:
                report = json.load(f)
            validator.send_morning_report(report)
        else:
            print(f"No report found for {date}")
    else:
        validator.run_validations(args.date)
