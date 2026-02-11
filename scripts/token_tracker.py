#!/usr/bin/env python3
"""
Token usage tracker for OpenClaw
Logs usage by category for daily reporting
"""

import json
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/home/samsclaw/.openclaw/workspace/logs")
LOG_FILE = LOG_DIR / f"token-usage-{datetime.now().strftime('%Y-%m-%d')}.jsonl"

def ensure_log_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_usage(category, tokens_in, tokens_out, model="moonshot/kimi-k2.5", task_details=""):
    """Log token usage for a specific task"""
    ensure_log_dir()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "total_tokens": tokens_in + tokens_out,
        "task_details": task_details
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_daily_summary(date_str=None):
    """Get summary of token usage for a specific date"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    log_file = LOG_DIR / f"token-usage-{date_str}.jsonl"
    
    if not log_file.exists():
        return None
    
    summary = {
        "date": date_str,
        "categories": {},
        "total_in": 0,
        "total_out": 0,
        "total": 0,
        "entries": 0
    }
    
    with open(log_file) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                cat = entry.get("category", "unknown")
                
                if cat not in summary["categories"]:
                    summary["categories"][cat] = {
                        "in": 0, "out": 0, "total": 0, "runs": 0
                    }
                
                summary["categories"][cat]["in"] += entry.get("tokens_in", 0)
                summary["categories"][cat]["out"] += entry.get("tokens_out", 0)
                summary["categories"][cat]["total"] += entry.get("total_tokens", 0)
                summary["categories"][cat]["runs"] += 1
                
                summary["total_in"] += entry.get("tokens_in", 0)
                summary["total_out"] += entry.get("tokens_out", 0)
                summary["total"] += entry.get("total_tokens", 0)
                summary["entries"] += 1
            except:
                continue
    
    return summary

def format_summary_for_briefing(summary):
    """Format summary for morning briefing"""
    if not summary:
        return "📊 **Token Usage (Yesterday):** No data available"
    
    lines = ["📊 **Token Usage (Last 24h):**"]
    lines.append("")
    
    # Sort categories by total usage
    sorted_cats = sorted(
        summary["categories"].items(),
        key=lambda x: x[1]["total"],
        reverse=True
    )
    
    for cat, data in sorted_cats:
        runs = data["runs"]
        total = data["total"]
        avg = total // runs if runs > 0 else 0
        lines.append(f"• {cat}: {total:,} tokens ({runs} runs, ~{avg:,} avg)")
    
    lines.append("")
    lines.append(f"**Total:** {summary['total']:,} tokens")
    lines.append(f"**Est. Cost:** ~${summary['total'] / 1000 * 0.01:.2f} (Kimi K1) / ~${summary['total'] / 1000 * 0.015:.2f} (Kimi K2.5)")
    
    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        summary = get_daily_summary(date)
        print(format_summary_for_briefing(summary))
    else:
        # Test logging
        log_usage("test", 500, 50, "moonshot/kimi-k2.5", "Test entry")
        print("Logged test entry")
