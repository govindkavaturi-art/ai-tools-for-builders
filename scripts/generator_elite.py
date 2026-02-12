#!/usr/bin/env python3
"""
Elite Generator - Premium "Insider" design for AI Tools Directory
Bento grid, 3D tilt, animated backgrounds, luxury aesthetics
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TOOLS_FILE = DATA_DIR / "tools.json"

CATEGORIES = {
    "coding": ("💻", "Code & Ship"),
    "agents": ("🤖", "AI Agents"),
    "image": ("🎨", "Visual Creation"),
    "video": ("🎬", "Video & Motion"),
    "audio": ("🎙️", "Audio & Voice"),
    "productivity": ("⚡", "Productivity"),
    "research": ("🔬", "Research"),
    "automation": ("🔄", "Automation"),
    "design": ("🎯", "Design"),
    "writing": ("✍️", "Writing"),
    "data": ("📊", "Data"),
    "sales": ("💰", "Sales"),
    "support": ("💬", "Support"),
    "marketing": ("📈", "Marketing"),
    "social": ("📱", "Social"),
    "finance": ("💳", "Finance"),
    "legal": ("⚖️", "Legal"),
    "hr": ("👥", "HR"),
    "education": ("🎓", "Education"),
    "3d": ("🎮", "3D & Gaming")
}

def load_tools():
    if TOOLS_FILE.exists():
        with open(TOOLS_FILE) as f:
            return json.load(f)
    return {"tools": [], "graveyard": []}

def generate_elite_html():
    print(f"\n✨ ELITE GENERATOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    db = load_tools()
    tools = [t for t in db.get("tools", []) if t.get("state") != "GRAVEYARD"]
    graveyard = db.get("graveyard", [])
    
    # Sort by score
    tools_sorted = sorted(tools, key=lambda x: x.get("scores", {}).get("combined", 0), reverse=True)
    
    # Top 6 for hero bento
    hero_tools = tools_sorted[:6]
    
    # Rest grouped by category
    by_category = {}
    for tool in tools_sorted[6:]:
        cat = tool.get("category", "other")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(tool)
    
    # Build hero bento HTML
    hero_html = ""
    for i, tool in enumerate(hero_tools):
        score = tool.get("scores", {}).get("combined", 0)
        size_class = "bento-large" if i < 2 else "bento-medium" if i < 4 else "bento-small"
        hero_html += f'''
            <a href="{tool['url']}" target="_blank" class="bento-card {size_class}" data-tilt>
                <div class="card-glow"></div>
                <div class="card-content">
                    <div class="card-rank">#{i+1}</div>
                    <h3>{tool['name']}</h3>
                    <p>{tool.get('description', '')}</p>
                    <div class="card-meta">
                        <span class="card-score">{score:.0f}</span>
                        <span class="card-tag">{tool.get('pricing', 'Free')}</span>
                    </div>
                </div>
                <div class="activity-pulse"></div>
            </a>'''
    
    # Build category sections
    cat_html = ""
    for cat_id, (icon, cat_name) in CATEGORIES.items():
        cat_tools = by_category.get(cat_id, [])
        if not cat_tools:
            continue
        
        tools_html = ""
        for tool in cat_tools[:12]:  # Max 12 per category
            score = tool.get("scores", {}).get("combined", 0)
            hot_class = " is-hot" if score >= 85 else ""
            tools_html += f'''
                    <a href="{tool['url']}" target="_blank" class="tool-card{hot_class}" data-tilt data-tilt-scale="1.02">
                        <div class="tool-name">{tool['name']}</div>
                        <div class="tool-desc">{tool.get('description', '')[:60]}...</div>
                        <div class="tool-footer">
                            <span class="tool-score">{score:.0f}</span>
                            <span class="tool-price">{tool.get('pricing', '')}</span>
                        </div>
                    </a>'''
        
        cat_html += f'''
            <section class="category-section" data-category="{cat_id}">
                <div class="category-header">
                    <span class="category-icon">{icon}</span>
                    <h2>{cat_name}</h2>
                    <span class="category-count">{len(cat_tools)}</span>
                </div>
                <div class="tools-row">
                    {tools_html}
                </div>
            </section>'''
    
    # Graveyard preview
    graveyard_html = ""
    for tool in graveyard[:4]:
        graveyard_html += f'''
                <div class="grave-card">
                    <div class="grave-name">{tool['name']}</div>
                    <div class="grave-reason">{tool.get('reason', 'INACTIVE')}</div>
                </div>'''
    
    updated_date = datetime.now().strftime("%B %d, %Y")
    tool_count = len(tools)
    graveyard_count = len(graveyard)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Insider's AI Stack | The Builder Weekly</title>
    <meta name="description" content="{tool_count} tools. Zero filler. The AI stack for builders who ship.">
    <meta property="og:title" content="The Insider's AI Stack">
    <meta property="og:description" content="{tool_count} curated AI tools. Updated daily. No pay-to-play.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --yellow: #FFF67F;
            --yellow-dim: #FFF67F22;
            --bg: #050505;
            --bg-card: #0a0a0a;
            --bg-elevated: #111;
            --text: #e5e5e5;
            --text-dim: #666;
            --border: #1a1a1a;
            --glow: rgba(255, 246, 127, 0.15);
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        html {{ scroll-behavior: smooth; }}
        
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        
        /* Animated gradient background */
        .bg-gradient {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(255, 246, 127, 0.03) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(255, 246, 127, 0.02) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(100, 100, 255, 0.01) 0%, transparent 70%);
            animation: gradientShift 20s ease-in-out infinite;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.8; transform: scale(1.1); }}
        }}
        
        /* Neural network dots */
        .neural-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.3;
            background-image: radial-gradient(circle at center, var(--yellow-dim) 1px, transparent 1px);
            background-size: 60px 60px;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; padding: 0 40px; }}
        
        /* Header */
        header {{
            padding: 50px 0 40px;
            text-align: center;
            position: relative;
        }}
        
        .eyebrow {{
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--yellow);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 16px;
        }}
        
        h1 {{
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            letter-spacing: -1px;
            line-height: 1.2;
            margin-bottom: 16px;
        }}
        
        h1 span {{
            background: linear-gradient(135deg, var(--yellow) 0%, #FFD700 50%, var(--yellow) 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 3s ease-in-out infinite;
        }}
        
        @keyframes shimmer {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .subtitle {{
            font-size: 1.25rem;
            color: var(--text-dim);
            max-width: 600px;
            margin: 0 auto 30px;
        }}
        
        .stats-row {{
            display: flex;
            justify-content: center;
            gap: 50px;
            flex-wrap: wrap;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--yellow);
        }}
        
        .stat-label {{
            font-size: 0.8rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Search */
        .search-wrap {{
            max-width: 400px;
            margin: 30px auto 0;
            position: relative;
        }}
        
        #search {{
            width: 100%;
            padding: 12px 18px;
            font-size: 0.9rem;
            font-family: inherit;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--bg-card);
            color: var(--text);
            transition: all 0.3s ease;
        }}
        
        #search:focus {{
            outline: none;
            border-color: var(--yellow);
            box-shadow: 0 0 30px var(--glow);
        }}
        
        #search::placeholder {{ color: var(--text-dim); }}
        
        /* Bento Grid */
        .bento-section {{
            padding: 30px 0;
        }}
        
        .section-label {{
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 16px;
        }}
        
        .bento-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
        }}
        
        .bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            text-decoration: none;
            color: var(--text);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            transition: all 0.3s ease;
            transform-style: preserve-3d;
            min-height: 120px;
        }}
        
        .bento-large {{
            grid-column: span 2;
        }}
        
        .bento-medium {{
            grid-column: span 2;
        }}
        
        .bento-small {{
            grid-column: span 1;
        }}
        
        .bento-card:hover {{
            border-color: var(--yellow);
            transform: translateY(-5px);
        }}
        
        .bento-card .card-glow {{
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, var(--glow) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.4s ease;
            pointer-events: none;
        }}
        
        .bento-card:hover .card-glow {{
            opacity: 1;
        }}
        
        .card-content {{
            position: relative;
            z-index: 1;
        }}
        
        .card-rank {{
            font-size: 0.65rem;
            font-weight: 600;
            color: var(--yellow);
            margin-bottom: 6px;
        }}
        
        .bento-card h3 {{
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        
        .bento-large h3 {{ font-size: 1.1rem; }}
        
        .bento-card p {{
            font-size: 0.75rem;
            color: var(--text-dim);
            margin-bottom: 8px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .card-meta {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}
        
        .card-score {{
            font-weight: 600;
            font-size: 0.8rem;
            color: var(--yellow);
        }}
        
        .card-tag {{
            font-size: 0.75rem;
            padding: 4px 10px;
            background: var(--bg-elevated);
            border-radius: 6px;
            color: var(--text-dim);
        }}
        
        .activity-pulse {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.5); opacity: 0.5; }}
        }}
        
        /* Category sections */
        .categories-wrap {{
            padding: 20px 0 40px;
        }}
        
        .category-section {{
            margin-bottom: 35px;
        }}
        
        .category-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
        }}
        
        .category-icon {{
            font-size: 1rem;
        }}
        
        .category-header h2 {{
            font-size: 0.95rem;
            font-weight: 600;
        }}
        
        .category-count {{
            font-size: 0.65rem;
            padding: 3px 8px;
            background: var(--bg-elevated);
            border-radius: 20px;
            color: var(--text-dim);
        }}
        
        .tools-row {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 10px;
        }}
        
        .tool-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px;
            text-decoration: none;
            color: var(--text);
            transition: all 0.2s ease;
            display: block;
        }}
        
        .tool-card:hover {{
            border-color: var(--yellow);
            transform: translateY(-3px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        
        .tool-card.is-hot {{
            border-color: var(--yellow-dim);
        }}
        
        .tool-name {{
            font-weight: 600;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }}
        
        .tool-desc {{
            font-size: 0.7rem;
            color: var(--text-dim);
            margin-bottom: 8px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .tool-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .tool-score {{
            font-weight: 600;
            font-size: 0.75rem;
            color: var(--yellow);
        }}
        
        .tool-price {{
            font-size: 0.65rem;
            color: var(--text-dim);
        }}
        
        /* Graveyard section */
        .graveyard-section {{
            padding: 30px 0;
            border-top: 1px solid var(--border);
        }}
        
        .graveyard-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        
        .graveyard-header h2 {{
            font-size: 0.95rem;
            color: var(--text-dim);
        }}
        
        .graveyard-link {{
            font-size: 0.85rem;
            color: var(--text-dim);
            text-decoration: none;
        }}
        
        .graveyard-link:hover {{ color: var(--yellow); }}
        
        .graveyard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 10px;
        }}
        
        .grave-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
            opacity: 0.6;
        }}
        
        .grave-name {{
            font-weight: 500;
            font-size: 0.85rem;
            text-decoration: line-through;
            margin-bottom: 4px;
        }}
        
        .grave-reason {{
            font-size: 0.7rem;
            color: #ef4444;
        }}
        
        /* How we curate */
        .curate-section {{
            padding: 40px 0;
            border-top: 1px solid var(--border);
            background: linear-gradient(180deg, transparent 0%, var(--bg-card) 100%);
        }}
        
        .curate-section h2 {{
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .curate-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}
        
        .curate-card {{
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        
        .curate-icon {{
            font-size: 1.5rem;
            margin-bottom: 10px;
        }}
        
        .curate-card h3 {{
            font-size: 0.85rem;
            margin-bottom: 8px;
        }}
        
        .curate-card p {{
            font-size: 0.75rem;
            color: var(--text-dim);
            line-height: 1.5;
        }}
        
        /* Footer */
        footer {{
            text-align: center;
            padding: 40px 0;
            border-top: 1px solid var(--border);
        }}
        
        .footer-brand {{
            font-size: 0.85rem;
            color: var(--text-dim);
            margin-bottom: 12px;
        }}
        
        .footer-brand a {{ color: var(--yellow); text-decoration: none; }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 24px;
        }}
        
        .footer-links a {{
            font-size: 0.85rem;
            color: var(--text-dim);
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .footer-links a:hover {{ color: var(--yellow); }}
        
        .hidden {{ display: none !important; }}
        
        @media (max-width: 1200px) {{
            .bento-grid {{
                grid-template-columns: repeat(4, 1fr);
            }}
            .curate-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (max-width: 900px) {{
            .bento-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
            .bento-large, .bento-medium, .bento-small {{
                grid-column: span 1;
            }}
            .tools-row {{
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }}
        }}
        
        @media (max-width: 600px) {{
            .container {{ padding: 0 16px; }}
            .bento-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .stats-row {{ gap: 20px; }}
            .curate-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <div class="neural-bg"></div>
    
    <header>
        <div class="container">
            <div class="eyebrow">The Builder Weekly Presents</div>
            <h1><span>The Insider's AI Stack</span></h1>
            <p class="subtitle">{tool_count} tools. Zero filler. Scored by real activity, not ads. Updated daily.</p>
            
            <div class="stats-row">
                <div class="stat">
                    <div class="stat-value">{tool_count}</div>
                    <div class="stat-label">Active Tools</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{graveyard_count}</div>
                    <div class="stat-label">In Graveyard</div>
                </div>
                <div class="stat">
                    <div class="stat-value">6AM</div>
                    <div class="stat-label">Daily Refresh</div>
                </div>
            </div>
            
            <div class="search-wrap">
                <input type="text" id="search" placeholder="Search the stack...">
            </div>
        </div>
    </header>
    
    <main>
        <section class="bento-section">
            <div class="container">
                <div class="section-label">🔥 Top Performers This Week</div>
                <div class="bento-grid">
                    {hero_html}
                </div>
            </div>
        </section>
        
        <section class="categories-wrap">
            <div class="container">
                <div class="section-label">📦 The Full Stack</div>
                {cat_html}
            </div>
        </section>
        
        <section class="graveyard-section">
            <div class="container">
                <div class="graveyard-header">
                    <h2>☠️ The Graveyard</h2>
                    <a href="graveyard.html" class="graveyard-link">View all {graveyard_count} →</a>
                </div>
                <div class="graveyard-grid">
                    {graveyard_html}
                </div>
            </div>
        </section>
        
        <section class="curate-section">
            <div class="container">
                <h2>How We Curate</h2>
                <div class="curate-grid">
                    <div class="curate-card">
                        <div class="curate-icon">📡</div>
                        <h3>Daily Scanning</h3>
                        <p>Every morning at 6 AM, we scan GitHub, HackerNews, Product Hunt, and X for real activity signals.</p>
                    </div>
                    <div class="curate-card">
                        <div class="curate-icon">📊</div>
                        <h3>Activity Scoring</h3>
                        <p>Tools are scored on commits, mentions, and buzz. No pay-to-play. No sponsored placements.</p>
                    </div>
                    <div class="curate-card">
                        <div class="curate-icon">☠️</div>
                        <h3>Brutal Curation</h3>
                        <p>60 days of silence = graveyard. We don't keep dead tools around to pad the numbers.</p>
                    </div>
                    <div class="curate-card">
                        <div class="curate-icon">🎯</div>
                        <h3>Builder-First</h3>
                        <p>Every tool here is used by people shipping real products. Not enterprise demos. Not vaporware.</p>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p class="footer-brand">Curated by <a href="https://thebuilderweekly.substack.com" target="_blank">The Builder Weekly</a></p>
            <div class="footer-links">
                <a href="https://instagram.com/thebuildrweekly" target="_blank">Instagram</a>
                <a href="https://x.com/thebuildrweekly" target="_blank">X</a>
                <a href="https://youtube.com/@thebuilderweekly" target="_blank">YouTube</a>
            </div>
        </div>
    </footer>
    
    <script>
        // Search functionality
        const search = document.getElementById('search');
        const categories = document.querySelectorAll('.category-section');
        const bentoCards = document.querySelectorAll('.bento-card');
        
        search.addEventListener('input', (e) => {{
            const q = e.target.value.toLowerCase();
            
            // Filter bento cards
            bentoCards.forEach(card => {{
                const match = card.textContent.toLowerCase().includes(q);
                card.style.display = match ? '' : 'none';
            }});
            
            // Filter category cards
            categories.forEach(cat => {{
                let visible = 0;
                cat.querySelectorAll('.tool-card').forEach(tool => {{
                    const match = tool.textContent.toLowerCase().includes(q);
                    tool.style.display = match ? '' : 'none';
                    if (match) visible++;
                }});
                cat.style.display = visible === 0 && q ? 'none' : '';
            }});
        }});
        
        // Simple tilt effect
        document.querySelectorAll('[data-tilt]').forEach(card => {{
            card.addEventListener('mousemove', (e) => {{
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;
                card.style.transform = `perspective(1000px) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) translateY(-5px)`;
            }});
            
            card.addEventListener('mouseleave', () => {{
                card.style.transform = '';
            }});
        }});
    </script>
</body>
</html>'''
    
    # Write elite index
    with open(BASE_DIR / "index.html", "w") as f:
        f.write(html)
    
    print(f"  ✓ Generated elite index.html with {len(tools)} tools")
    print(f"  ✓ Hero section: {len(hero_tools)} top tools")
    print(f"  ✓ Categories: {len([c for c in by_category if by_category[c]])} active")
    
    return True

if __name__ == "__main__":
    generate_elite_html()
