#!/usr/bin/env python3
"""
Scanner - Fetch fresh data from sources
Product Hunt, GitHub Trending, HackerNews, X/Twitter
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SOURCES_DIR = DATA_DIR / "sources"

def fetch_github_trending():
    """Fetch GitHub trending repos for AI/ML"""
    print("📡 Fetching GitHub trending...")
    
    # Use gh CLI to search for trending AI repos
    try:
        result = subprocess.run([
            "gh", "api", "search/repositories",
            "-X", "GET",
            "-f", "q=topic:ai topic:machine-learning stars:>1000 pushed:>2026-01-01",
            "-f", "sort=stars",
            "-f", "order=desc",
            "-f", "per_page=100"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            repos = []
            for item in data.get("items", [])[:100]:
                repos.append({
                    "name": item["name"],
                    "full_name": item["full_name"],
                    "url": item["html_url"],
                    "description": item.get("description", ""),
                    "stars": item["stargazers_count"],
                    "forks": item["forks_count"],
                    "updated_at": item["updated_at"],
                    "topics": item.get("topics", [])
                })
            
            with open(SOURCES_DIR / "github.json", "w") as f:
                json.dump({"fetched_at": datetime.now().isoformat(), "repos": repos}, f, indent=2)
            
            print(f"  ✓ Found {len(repos)} trending repos")
            return repos
    except Exception as e:
        print(f"  ✗ GitHub fetch failed: {e}")
    
    return []

def fetch_hackernews():
    """Fetch HN front page and search for AI tools"""
    print("📡 Fetching HackerNews...")
    
    try:
        import urllib.request
        
        # Get top stories
        with urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json") as resp:
            top_ids = json.loads(resp.read().decode())[:50]
        
        stories = []
        ai_keywords = ['ai', 'gpt', 'llm', 'claude', 'openai', 'anthropic', 'chatgpt', 'copilot', 'agent', 'model']
        
        for story_id in top_ids[:30]:
            try:
                with urllib.request.urlopen(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json") as resp:
                    story = json.loads(resp.read().decode())
                    title = story.get("title", "").lower()
                    if any(kw in title for kw in ai_keywords):
                        stories.append({
                            "id": story_id,
                            "title": story.get("title"),
                            "url": story.get("url"),
                            "score": story.get("score", 0),
                            "time": story.get("time")
                        })
            except:
                continue
        
        with open(SOURCES_DIR / "hackernews.json", "w") as f:
            json.dump({"fetched_at": datetime.now().isoformat(), "stories": stories}, f, indent=2)
        
        print(f"  ✓ Found {len(stories)} AI-related stories")
        return stories
    except Exception as e:
        print(f"  ✗ HN fetch failed: {e}")
    
    return []

def fetch_producthunt():
    """Fetch recent Product Hunt AI launches"""
    print("📡 Fetching Product Hunt...")
    
    # For now, we'll use web scraping via the existing web_fetch capability
    # In production, would use PH API with proper auth
    
    try:
        # Placeholder - would need PH API key for real implementation
        # For now, return empty and rely on manual additions
        print("  ⚠ Product Hunt API not configured - using cached data")
        
        # Check if we have cached data
        ph_file = SOURCES_DIR / "producthunt.json"
        if ph_file.exists():
            with open(ph_file) as f:
                return json.load(f).get("products", [])
    except Exception as e:
        print(f"  ✗ PH fetch failed: {e}")
    
    return []

def fetch_twitter_mentions():
    """Fetch AI tool mentions from builder accounts"""
    print("📡 Fetching X/Twitter mentions...")
    
    # This would use the existing X API credentials
    # For now, placeholder
    try:
        print("  ⚠ Using cached Twitter data")
        tw_file = SOURCES_DIR / "twitter.json"
        if tw_file.exists():
            with open(tw_file) as f:
                return json.load(f).get("mentions", [])
    except Exception as e:
        print(f"  ✗ Twitter fetch failed: {e}")
    
    return []

def run_scan():
    """Run full scan of all sources"""
    print(f"\n🔍 SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # Ensure directories exist
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "github": fetch_github_trending(),
        "hackernews": fetch_hackernews(),
        "producthunt": fetch_producthunt(),
        "twitter": fetch_twitter_mentions()
    }
    
    # Save combined results
    with open(SOURCES_DIR / "latest_scan.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Scan complete")
    return results

if __name__ == "__main__":
    run_scan()
