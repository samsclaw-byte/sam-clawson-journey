#!/usr/bin/env python3
"""
Skill Security Validator
Checks skills before installation for security issues
"""

import os
import subprocess
import json
import sys

def check_skill_security(skill_name, skill_path=None):
    """
    Perform security checks on a skill before installation
    Returns: (is_safe, warnings, recommendations)
    """
    warnings = []
    recommendations = []
    
    print(f"🔍 Security Check: {skill_name}")
    print("=" * 50)
    
    # Check 1: Verify skill exists in registry
    result = subprocess.run(
        ['clawhub', 'info', skill_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        warnings.append(f"⚠️ Skill '{skill_name}' not found in ClawHub registry")
        recommendations.append("Verify skill name or install from local path")
    else:
        print("✅ Found in ClawHub registry")
    
    # Check 2: Look for suspicious permissions
    if skill_path and os.path.exists(skill_path):
        # Check for executable scripts
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                filepath = os.path.join(root, file)
                if os.access(filepath, os.X_OK):
                    warnings.append(f"⚠️ Executable file found: {file}")
    
    # Check 3: Check for network access requirements
    network_skills = ['web-search', 'twitter', 'api', 'http', 'network']
    if any(ns in skill_name.lower() for ns in network_skills):
        warnings.append("⚠️ Network access required - verify endpoint security")
        recommendations.append("Check if skill uses HTTPS only")
        recommendations.append("Verify API key storage is secure")
    
    # Check 4: Check for file system access
    fs_skills = ['file', 'disk', 'storage', 'write', 'delete']
    if any(fs in skill_name.lower() for fs in fs_skills):
        warnings.append("⚠️ File system access required - review scope")
        recommendations.append("Verify skill only accesses allowed directories")
    
    # Check 5: Check for credential storage
    cred_skills = ['auth', 'login', 'password', 'token', 'key']
    if any(cs in skill_name.lower() for cs in cred_skills):
        warnings.append("⚠️ Credential handling detected")
        recommendations.append("Ensure credentials stored in ~/.config/ with 600 permissions")
        recommendations.append("Verify no hardcoded secrets in skill code")
    
    print("\n📋 Summary:")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  {w}")
    
    if recommendations:
        print("\nRecommendations:")
        for r in recommendations:
            print(f"  • {r}")
    
    if not warnings and not recommendations:
        print("✅ No major security concerns detected")
    
    # Determine if safe to install
    is_safe = len([w for w in warnings if w.startswith("❌")]) == 0
    
    return is_safe, warnings, recommendations

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skill_security_check.py <skill-name>")
        print("Example: python3 skill_security_check.py duckduckgo-search")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    is_safe, warnings, recommendations = check_skill_security(skill_name)
    
    print(f"\n{'✅' if is_safe else '⚠️'} Safe to install: {is_safe}")
    
    if not is_safe:
        sys.exit(1)
