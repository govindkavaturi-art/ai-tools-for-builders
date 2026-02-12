#!/usr/bin/env python3
"""
Publisher - Commit and push changes to GitHub Pages
"""

import subprocess
from datetime import datetime
from pathlib import Path
import json

BASE_DIR = Path(__file__).parent.parent
CHANGELOG_FILE = BASE_DIR / "changelog.md"
SCORES_FILE = BASE_DIR / "data" / "scores.json"

def update_changelog():
    """Add today's changes to changelog"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load score changes
    changes = []
    if SCORES_FILE.exists():
        with open(SCORES_FILE) as f:
            data = json.load(f)
            changes = data.get("state_changes", [])
    
    # Build changelog entry
    entry = f"\n## {today}\n\n"
    if changes:
        entry += "### State Changes\n"
        for c in changes:
            entry += f"- **{c['name']}**: {c['old_state']} → {c['new_state']} (score: {c['score']})\n"
    else:
        entry += "- Daily refresh, no state changes\n"
    
    # Prepend to changelog
    existing = ""
    if CHANGELOG_FILE.exists():
        with open(CHANGELOG_FILE) as f:
            existing = f.read()
    
    header = "# AI Tools Directory Changelog\n\nDaily updates to the directory.\n"
    if existing.startswith("# AI Tools"):
        # Remove existing header
        existing = "\n".join(existing.split("\n")[3:])
    
    with open(CHANGELOG_FILE, "w") as f:
        f.write(header + entry + existing)
    
    return len(changes)

def git_push():
    """Commit and push changes"""
    print(f"\n📤 PUBLISHER - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # Update changelog
    changes = update_changelog()
    print(f"  ✓ Updated changelog ({changes} state changes)")
    
    try:
        # Stage all changes
        subprocess.run(["git", "add", "-A"], cwd=BASE_DIR, check=True)
        
        # Commit
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"Daily update: {today}"
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        
        if "nothing to commit" in result.stdout + result.stderr:
            print("  ℹ No changes to commit")
            return True
        
        # Push
        subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
        print("  ✓ Pushed to GitHub Pages")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Git error: {e}")
        return False

if __name__ == "__main__":
    git_push()
