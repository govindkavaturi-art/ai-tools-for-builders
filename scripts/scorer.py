#!/usr/bin/env python3
"""
Scorer - Calculate activity and relevance scores for tools
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TOOLS_FILE = DATA_DIR / "tools.json"
SCORES_FILE = DATA_DIR / "scores.json"
SOURCES_DIR = DATA_DIR / "sources"

def load_tools():
    """Load tools database"""
    if TOOLS_FILE.exists():
        with open(TOOLS_FILE) as f:
            return json.load(f)
    return {"tools": [], "graveyard": []}

def load_sources():
    """Load latest scan data"""
    sources = {}
    for src in ["github", "hackernews", "producthunt", "twitter"]:
        src_file = SOURCES_DIR / f"{src}.json"
        if src_file.exists():
            with open(src_file) as f:
                sources[src] = json.load(f)
    return sources

def calculate_activity_score(tool, sources):
    """Calculate activity score based on signals"""
    score = 50  # Base score
    
    tool_name = tool.get("name", "").lower()
    tool_url = tool.get("url", "").lower()
    
    # GitHub signals
    github_data = sources.get("github", {}).get("repos", [])
    for repo in github_data:
        repo_name = repo.get("name", "").lower()
        if tool_name in repo_name or repo_name in tool_name:
            # Found matching repo
            stars = repo.get("stars", 0)
            score += min(stars / 1000, 25)  # Max 25 points from stars
            
            # Recent activity bonus
            updated = repo.get("updated_at", "")
            if updated:
                try:
                    updated_date = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    days_ago = (datetime.now(updated_date.tzinfo) - updated_date).days
                    if days_ago < 7:
                        score += 20
                    elif days_ago < 30:
                        score += 10
                except:
                    pass
            break
    
    # HackerNews signals
    hn_data = sources.get("hackernews", {}).get("stories", [])
    for story in hn_data:
        title = story.get("title", "").lower()
        url = story.get("url", "") or ""
        if tool_name in title or tool_url in url.lower():
            hn_score = story.get("score", 0)
            score += min(hn_score / 10, 35)  # Max 35 points
            break
    
    # Check for inactivity
    last_signal = tool.get("last_signal_date")
    if last_signal:
        try:
            last_date = datetime.fromisoformat(last_signal)
            days_inactive = (datetime.now() - last_date).days
            if days_inactive > 60:
                score -= 50
            elif days_inactive > 30:
                score -= 25
        except:
            pass
    
    return max(0, min(100, score))

def calculate_relevance_score(tool):
    """Calculate relevance score based on builder utility"""
    score = 0
    
    # Builder utility (based on category and tags)
    high_value_categories = ["coding", "automation", "agents", "productivity"]
    if tool.get("category") in high_value_categories:
        score += 25
    else:
        score += 15
    
    # Solo-friendly pricing
    pricing = tool.get("pricing", "").lower()
    if "free" in pricing:
        score += 20
    elif any(x in pricing for x in ["$10", "$15", "$20", "$25", "$29", "$30"]):
        score += 15
    elif "enterprise" in pricing:
        score += 5
    else:
        score += 10
    
    # Tags bonus
    hot_tags = ["hot", "trending", "new", "ai-native"]
    for tag in tool.get("tags", []):
        if tag in hot_tags:
            score += 10
            break
    
    # Has working product (not waitlist)
    if tool.get("state") == "ACTIVE":
        score += 25
    elif "waitlist" not in tool.get("description", "").lower():
        score += 20
    
    return max(0, min(100, score))

def score_all_tools():
    """Score all tools and update database"""
    print(f"\n📊 SCORER - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    db = load_tools()
    sources = load_sources()
    
    scores = []
    state_changes = []
    
    for tool in db.get("tools", []):
        activity = calculate_activity_score(tool, sources)
        relevance = calculate_relevance_score(tool)
        combined = (activity * 0.6) + (relevance * 0.4)
        
        old_state = tool.get("state", "ACTIVE")
        
        # Determine new state
        if combined >= 40:
            new_state = "ACTIVE"
        elif combined >= 25:
            new_state = "WATCHLIST"
        else:
            new_state = "GRAVEYARD"
        
        # Update tool
        tool["scores"] = {
            "activity": round(activity, 1),
            "relevance": round(relevance, 1),
            "combined": round(combined, 1)
        }
        
        if new_state != old_state:
            state_changes.append({
                "name": tool["name"],
                "old_state": old_state,
                "new_state": new_state,
                "score": round(combined, 1)
            })
            tool["state"] = new_state
        
        scores.append({
            "id": tool["id"],
            "name": tool["name"],
            "combined": round(combined, 1)
        })
    
    # Sort by combined score
    db["tools"].sort(key=lambda x: x.get("scores", {}).get("combined", 0), reverse=True)
    
    # Save updated database
    with open(TOOLS_FILE, "w") as f:
        json.dump(db, f, indent=2)
    
    # Save scores summary
    with open(SCORES_FILE, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "scores": sorted(scores, key=lambda x: x["combined"], reverse=True),
            "state_changes": state_changes
        }, f, indent=2)
    
    print(f"  ✓ Scored {len(db['tools'])} tools")
    if state_changes:
        print(f"  ⚠ {len(state_changes)} state changes:")
        for change in state_changes:
            print(f"    - {change['name']}: {change['old_state']} → {change['new_state']}")
    
    return db

if __name__ == "__main__":
    score_all_tools()
