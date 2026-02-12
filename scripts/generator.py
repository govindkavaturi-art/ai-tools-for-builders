#!/usr/bin/env python3
"""
Generator - Build HTML pages from tools database
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TOOLS_FILE = DATA_DIR / "tools.json"

CATEGORIES = {
    "writing": ("✍️", "Writing & Content"),
    "image": ("🎨", "Image Generation"),
    "video": ("🎬", "Video Creation"),
    "audio": ("🎙️", "Audio & Voice"),
    "coding": ("💻", "Coding & Development"),
    "productivity": ("⚡", "Productivity"),
    "research": ("🔬", "Research & Analysis"),
    "marketing": ("📈", "Marketing"),
    "design": ("🎯", "Design"),
    "sales": ("💰", "Sales"),
    "support": ("💬", "Customer Support"),
    "data": ("📊", "Data & Analytics"),
    "hr": ("👥", "HR & Recruiting"),
    "legal": ("⚖️", "Legal"),
    "finance": ("💳", "Finance"),
    "agents": ("🤖", "AI Agents & Chatbots"),
    "automation": ("🔄", "Automation"),
    "social": ("📱", "Social Media"),
    "education": ("🎓", "Education"),
    "3d": ("🎮", "3D & Game Dev")
}

def load_tools():
    if TOOLS_FILE.exists():
        with open(TOOLS_FILE) as f:
            return json.load(f)
    return {"tools": [], "graveyard": []}

def generate_html():
    print(f"\n🎨 GENERATOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    db = load_tools()
    tools = [t for t in db.get("tools", []) if t.get("state") != "GRAVEYARD"]
    graveyard = db.get("graveyard", [])
    
    # Group by category
    by_category = {}
    for tool in tools:
        cat = tool.get("category", "other")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(tool)
    
    # Hot tools (top 10 by score)
    hot_tools = sorted(tools, key=lambda x: x.get("scores", {}).get("combined", 0), reverse=True)[:10]
    hot_html = ""
    for tool in hot_tools:
        score = tool.get("scores", {}).get("combined", 0)
        hot_html += f'''                <div class="hot-tool">
                    <a href="{tool['url']}" target="_blank">{tool['name']}</a>
                    <div class="hot-score">Score: {score:.0f}</div>
                </div>
'''
    
    # Categories HTML
    cat_html = ""
    for cat_id, (icon, cat_name) in CATEGORIES.items():
        cat_tools = by_category.get(cat_id, [])
        if not cat_tools:
            continue
        
        tools_html = ""
        for tool in sorted(cat_tools, key=lambda x: x.get("scores", {}).get("combined", 0), reverse=True):
            score = tool.get("scores", {}).get("combined", 0)
            is_hot = score >= 75
            hot_class = " tool-hot" if is_hot else ""
            
            tools_html += f'''                    <div class="tool{hot_class}">
                        <a href="{tool['url']}" target="_blank">{tool['name']}</a>
                        <div class="tool-desc">{tool.get('description', '')}</div>
                        <div class="tool-meta">
                            <span class="tool-tag">{tool.get('pricing', 'Free')}</span>
                        </div>
                        <span class="tool-score">{score:.0f}</span>
                    </div>
'''
        
        cat_html += f'''            <div class="category" data-category="{cat_id}">
                <div class="category-header">
                    <span class="category-icon">{icon}</span>
                    <h2>{cat_name}</h2>
                    <span class="category-count">{len(cat_tools)} tools</span>
                </div>
                <div class="tools-grid">
{tools_html}                </div>
            </div>
'''
    
    updated_date = datetime.now().strftime("%B %d, %Y")
    tool_count = len(tools)
    category_count = len([c for c in by_category if by_category[c]])
    graveyard_count = len(graveyard)
    
    # Build final HTML using string concatenation instead of .format()
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>200 AI Tools for Builders | The Builder Weekly</title>
    <meta name="description" content="Curated list of the hottest AI tools, updated daily. No outdated tools - only what builders are using right now.">
    <meta property="og:title" content="200 AI Tools for Builders">
    <meta property="og:description" content="Daily-updated directory of AI tools that actually work. Curated by The Builder Weekly.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: #e5e5e5; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
        header {{ padding: 60px 0 40px; text-align: center; border-bottom: 1px solid #222; }}
        header h1 {{ font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #FFF67F 0%, #FFD700 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 16px; }}
        header p {{ color: #888; font-size: 1.1rem; max-width: 600px; margin: 0 auto; }}
        .updated {{ display: inline-block; margin-top: 20px; padding: 8px 16px; background: #1a1a1a; border-radius: 20px; font-size: 0.85rem; color: #666; }}
        .live-badge {{ background: #22c55e; color: #000; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: 8px; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
        .search-box {{ padding: 30px 0; position: sticky; top: 0; background: #0a0a0a; z-index: 100; border-bottom: 1px solid #222; }}
        #search {{ width: 100%; max-width: 500px; padding: 14px 20px; font-size: 1rem; border: 1px solid #333; border-radius: 8px; background: #111; color: #fff; display: block; margin: 0 auto; }}
        #search:focus {{ outline: none; border-color: #FFF67F; }}
        .stats {{ display: flex; justify-content: center; gap: 40px; padding: 30px 0; flex-wrap: wrap; }}
        .stat {{ text-align: center; }}
        .stat-num {{ font-size: 2.5rem; font-weight: 700; color: #FFF67F; }}
        .stat-label {{ color: #666; font-size: 0.9rem; }}
        .hot-section {{ background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%); border: 1px solid #333; border-radius: 16px; padding: 24px; margin: 30px 0; }}
        .hot-section h3 {{ color: #FFF67F; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
        .hot-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }}
        .hot-tool {{ background: #222; border-radius: 8px; padding: 12px; }}
        .hot-tool a {{ color: #fff; text-decoration: none; font-weight: 500; }}
        .hot-tool a:hover {{ color: #FFF67F; }}
        .hot-score {{ font-size: 0.75rem; color: #22c55e; margin-top: 4px; }}
        .categories {{ padding: 40px 0; }}
        .category {{ margin-bottom: 50px; }}
        .category-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid #222; }}
        .category-icon {{ font-size: 1.5rem; }}
        .category h2 {{ font-size: 1.4rem; font-weight: 600; color: #fff; }}
        .category-count {{ background: #1a1a1a; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; color: #888; }}
        .tools-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }}
        .tool {{ background: #111; border: 1px solid #222; border-radius: 10px; padding: 16px; transition: all 0.2s; position: relative; }}
        .tool:hover {{ border-color: #FFF67F; transform: translateY(-2px); }}
        .tool a {{ color: #fff; text-decoration: none; font-weight: 500; }}
        .tool a:hover {{ color: #FFF67F; }}
        .tool-desc {{ color: #777; font-size: 0.85rem; margin-top: 6px; }}
        .tool-meta {{ display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }}
        .tool-tag {{ padding: 3px 8px; background: #1a1a1a; border-radius: 4px; font-size: 0.75rem; color: #555; }}
        .tool-score {{ position: absolute; top: 12px; right: 12px; font-size: 0.7rem; color: #444; }}
        .tool-hot {{ border-color: #FFF67F33; }}
        .tool-hot::before {{ content: "🔥"; position: absolute; top: -8px; right: -8px; }}
        footer {{ text-align: center; padding: 60px 0; border-top: 1px solid #222; color: #555; }}
        footer a {{ color: #FFF67F; text-decoration: none; }}
        .graveyard-link {{ margin-top: 20px; }}
        .graveyard-link a {{ color: #666; font-size: 0.9rem; }}
        .hidden {{ display: none !important; }}
        .how-we-curate {{ background: linear-gradient(135deg, #111 0%, #0a0a0a 100%); border-top: 1px solid #222; border-bottom: 1px solid #222; padding: 60px 0; margin-top: 40px; }}
        .how-we-curate h3 {{ text-align: center; color: #FFF67F; font-size: 1.5rem; margin-bottom: 40px; }}
        .curate-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; }}
        .curate-item {{ background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 24px; text-align: center; }}
        .curate-icon {{ font-size: 2rem; margin-bottom: 12px; }}
        .curate-item h4 {{ color: #fff; font-size: 1.1rem; margin-bottom: 8px; }}
        .curate-item p {{ color: #888; font-size: 0.9rem; line-height: 1.5; }}
        @media (max-width: 600px) {{ header h1 {{ font-size: 2rem; }} }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>200 AI Tools for Builders</h1>
            <p>Daily-updated directory of AI tools that actually work. Dead tools get removed. Only what builders are using right now.</p>
            <span class="updated">Updated {updated_date}<span class="live-badge">LIVE</span></span>
        </div>
    </header>
    
    <div class="search-box">
        <div class="container">
            <input type="text" id="search" placeholder="Search tools..." autocomplete="off">
        </div>
    </div>
    
    <main class="container">
        <div class="stats">
            <div class="stat"><div class="stat-num">{tool_count}</div><div class="stat-label">Active Tools</div></div>
            <div class="stat"><div class="stat-num">{category_count}</div><div class="stat-label">Categories</div></div>
            <div class="stat"><div class="stat-num">{graveyard_count}</div><div class="stat-label">In Graveyard</div></div>
        </div>
        
        <div class="hot-section">
            <h3>🔥 Hot This Week</h3>
            <div class="hot-grid">
{hot_html}
            </div>
        </div>
        
        <div class="categories">
{cat_html}
        </div>
    </main>
    
    <section class="how-we-curate">
        <div class="container">
            <h3>🔍 How We Curate This List</h3>
            <div class="curate-grid">
                <div class="curate-item">
                    <div class="curate-icon">📡</div>
                    <h4>Daily Scanning</h4>
                    <p>Every day at 6 AM, our AI agent scans GitHub trending, Hacker News, Product Hunt, and X/Twitter for AI tool activity.</p>
                </div>
                <div class="curate-item">
                    <div class="curate-icon">📊</div>
                    <h4>Activity Scoring</h4>
                    <p>Each tool gets scored on recent GitHub commits, community mentions, funding news, and real builder usage. No pay-to-play.</p>
                </div>
                <div class="curate-item">
                    <div class="curate-icon">☠️</div>
                    <h4>Graveyard Rules</h4>
                    <p>Tools with no activity for 60+ days get moved to the graveyard. No dead tools, no vaporware, no outdated recommendations.</p>
                </div>
                <div class="curate-item">
                    <div class="curate-icon">🔄</div>
                    <h4>Updated Daily</h4>
                    <p>This list refreshes every morning. What you see is what builders are actually using right now, not what was hot in 2023.</p>
                </div>
            </div>
        </div>
    </section>
    
    <footer>
        <div class="container">
            <p>Curated by <a href="https://thebuilderweekly.substack.com" target="_blank">The Builder Weekly</a></p>
            <p style="margin-top: 12px; font-size: 0.85rem;">
                <a href="https://instagram.com/thebuildrweekly" target="_blank">Instagram</a> · 
                <a href="https://x.com/thebuildrweekly" target="_blank">X</a> · 
                <a href="https://youtube.com/@thebuilderweekly" target="_blank">YouTube</a>
            </p>
            <div class="graveyard-link">
                <a href="graveyard.html">View the Graveyard</a> ({graveyard_count} tools that didn't make it)
            </div>
        </div>
    </footer>
    
    <script>
        const search = document.getElementById('search');
        const categories = document.querySelectorAll('.category');
        search.addEventListener('input', (e) => {{
            const q = e.target.value.toLowerCase();
            categories.forEach(cat => {{
                let visible = 0;
                cat.querySelectorAll('.tool').forEach(tool => {{
                    const match = tool.textContent.toLowerCase().includes(q);
                    tool.classList.toggle('hidden', !match);
                    if (match) visible++;
                }});
                cat.classList.toggle('hidden', visible === 0);
            }});
        }});
    </script>
</body>
</html>'''
    
    # Write index.html
    with open(BASE_DIR / "index.html", "w") as f:
        f.write(html)
    
    print(f"  ✓ Generated index.html with {len(tools)} tools")
    
    # Generate graveyard
    generate_graveyard(graveyard)
    
    return True

def generate_graveyard(graveyard):
    """Generate graveyard.html"""
    if not graveyard:
        graveyard_html = "<p>No tools in the graveyard yet. We remove tools that go inactive or shut down.</p>"
    else:
        graveyard_html = ""
        for tool in graveyard:
            graveyard_html += f'''<div class="graveyard-tool">
                <h4>{tool['name']}</h4>
                <p class="reason">{tool.get('reason', 'INACTIVITY')}: {tool.get('reason_detail', 'No activity detected')}</p>
                <p class="dates">Removed: {tool.get('removed_date', 'Unknown')}</p>
            </div>
'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tools Graveyard | The Builder Weekly</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: #e5e5e5; line-height: 1.6; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #666; margin-bottom: 10px; }}
        .subtitle {{ color: #444; margin-bottom: 40px; }}
        .back {{ color: #FFF67F; text-decoration: none; display: inline-block; margin-bottom: 30px; }}
        .graveyard-tool {{ background: #111; border: 1px solid #222; border-radius: 10px; padding: 20px; margin-bottom: 16px; }}
        .graveyard-tool h4 {{ color: #888; margin-bottom: 8px; }}
        .reason {{ color: #ef4444; font-size: 0.9rem; }}
        .dates {{ color: #444; font-size: 0.8rem; margin-top: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back">← Back to Active Tools</a>
        <h1>☠️ The Graveyard</h1>
        <p class="subtitle">Tools that didn't make it. Gone but not forgotten.</p>
        {graveyard_html}
    </div>
</body>
</html>'''
    
    with open(BASE_DIR / "graveyard.html", "w") as f:
        f.write(html)
    
    print(f"  ✓ Generated graveyard.html with {len(graveyard)} tools")

if __name__ == "__main__":
    generate_html()
