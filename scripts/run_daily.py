#!/usr/bin/env python3
"""
Daily Curator Pipeline
Runs: SCAN → SCORE → GENERATE → PUBLISH
"""

import sys
from datetime import datetime
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

from scanner import run_scan
from scorer import score_all_tools
from generator_elite import generate_elite_html as generate_html
from publisher import git_push

def run_daily_update():
    """Run the full daily update pipeline"""
    print("\n" + "=" * 60)
    print(f"🚀 AI TOOLS CURATOR - DAILY UPDATE")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S PST')}")
    print("=" * 60)
    
    steps = [
        ("SCAN", run_scan),
        ("SCORE", score_all_tools),
        ("GENERATE", generate_html),
        ("PUBLISH", git_push)
    ]
    
    results = {}
    for name, func in steps:
        try:
            result = func()
            results[name] = "✓"
        except Exception as e:
            print(f"\n❌ {name} FAILED: {e}")
            results[name] = f"✗ {e}"
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    for name, status in results.items():
        print(f"  {name}: {status}")
    
    success = all(v == "✓" for v in results.values())
    print(f"\n{'✅ All steps completed!' if success else '⚠️ Some steps failed'}")
    
    return success

if __name__ == "__main__":
    success = run_daily_update()
    sys.exit(0 if success else 1)
