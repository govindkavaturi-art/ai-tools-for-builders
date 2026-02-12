# AI Tools Directory Curator - System Design

## Overview

A sub-agent (`curator`) that maintains a living directory of 200 AI tools, updated daily based on real activity signals. Tools that go inactive are moved to a "graveyard" list with reasons.

---

## Data Sources (Freshness Signals)

| Source | Signal | Weight | API/Method |
|--------|--------|--------|------------|
| Product Hunt | Featured launch (30 days) | +50 | PH API |
| Product Hunt | 500+ upvotes | +30 | PH API |
| GitHub | Commits in last 30 days | +25 | GitHub API |
| GitHub | Stars gained (30 days) | +20 | GitHub API |
| GitHub | Trending repos | +40 | GitHub trending |
| X/Twitter | Mentions by builders (1K+ followers) | +15/mention | Search API |
| Hacker News | Front page mention | +35 | HN API |
| Google Trends | Rising search interest | +20 | SerpAPI/Trends |
| Funding | New round announced | +30 | Crunchbase/news |
| Shutdown | Company closed/acquired badly | -100 | News/manual |
| Inactivity | No signals in 60 days | -50 | Calculated |

---

## Scoring System

### Activity Score (0-100)
```
base_score = 50

Recent signals (last 30 days):
  + product_hunt_feature * 50
  + product_hunt_upvotes / 20 (max 30)
  + github_commits > 10 ? 25 : github_commits * 2.5
  + github_stars_gained / 100 (max 20)
  + twitter_mentions * 15 (max 45)
  + hn_frontpage * 35
  + funding_round * 30

Decay:
  - days_since_last_signal > 60 ? 50 : 0
  - days_since_last_signal > 30 ? 25 : 0

Final = clamp(base_score + signals - decay, 0, 100)
```

### Relevance Score (0-100)
```
- Builder utility (manual tag): 0-30
- Solo-friendly pricing: 0-20
- Active development: 0-25
- Community buzz: 0-25
```

### Combined Score
```
total_score = (activity_score * 0.6) + (relevance_score * 0.4)
```

---

## Tool Lifecycle

### States
1. **ACTIVE** - Score >= 40, in top 200
2. **WATCHLIST** - Score 25-39, at risk
3. **GRAVEYARD** - Score < 25 for 14 days, or confirmed shutdown

### Transitions
```
New tool discovered (score >= 50) → ACTIVE
ACTIVE tool drops below 40 → WATCHLIST (7 day grace)
WATCHLIST tool recovers above 45 → ACTIVE
WATCHLIST tool stays < 40 for 14 days → GRAVEYARD
GRAVEYARD tool surges above 60 → ACTIVE (comeback)
```

---

## Daily Cron Process

### Schedule: 6:00 AM PST

### Steps:

1. **SCAN** (30 min)
   - Fetch Product Hunt launches (last 24h)
   - Fetch GitHub trending (AI/ML tags)
   - Search X for tool mentions by builders
   - Check HN front page for AI tools
   - Check RSS feeds for AI news

2. **SCORE** (10 min)
   - Recalculate activity score for all tools
   - Apply decay for inactive tools
   - Flag tools crossing state thresholds

3. **RANK** (5 min)
   - Sort by combined score
   - Top 200 = ACTIVE list
   - 201-250 = WATCHLIST
   - Below threshold = GRAVEYARD candidates

4. **DISCOVER** (15 min)
   - New tools from PH/GitHub/X not in database
   - Quick evaluation: real product? active? useful?
   - Add promising tools to WATCHLIST for observation

5. **UPDATE** (5 min)
   - Generate new index.html with current top 200
   - Update graveyard.html with removed tools + reasons
   - Update changelog.md with today's changes

6. **PUBLISH** (2 min)
   - Git commit changes
   - Push to GitHub Pages
   - Log results

---

## Directory Structure

```
ai-tools-directory/
├── index.html              # Live directory (auto-generated)
├── graveyard.html          # Inactive/dead tools
├── changelog.md            # Daily changes log
├── data/
│   ├── tools.json          # Master tool database
│   ├── scores.json         # Current scores
│   ├── history/            # Daily snapshots
│   │   └── 2026-02-12.json
│   └── sources/            # Raw data from APIs
│       ├── producthunt.json
│       ├── github.json
│       └── twitter.json
├── scripts/
│   ├── scanner.py          # Fetch data from sources
│   ├── scorer.py           # Calculate scores
│   ├── generator.py        # Build HTML
│   └── publisher.py        # Git push
└── CURATOR-PLAN.md         # This file
```

---

## Tool Database Schema

```json
{
  "id": "cursor",
  "name": "Cursor",
  "url": "https://cursor.sh",
  "category": "coding",
  "description": "AI-first code editor",
  "pricing": "Free tier",
  "added_date": "2026-01-15",
  "last_signal_date": "2026-02-11",
  "state": "ACTIVE",
  "scores": {
    "activity": 85,
    "relevance": 90,
    "combined": 87
  },
  "signals": {
    "github_stars": 45000,
    "github_commits_30d": 156,
    "twitter_mentions_30d": 234,
    "ph_upvotes": 3200,
    "hn_mentions_30d": 12
  },
  "tags": ["coding", "editor", "free-tier", "hot"],
  "graveyard_reason": null
}
```

---

## Graveyard Entry Schema

```json
{
  "id": "copy-ai",
  "name": "Copy.ai",
  "url": "https://copy.ai",
  "category": "writing",
  "removed_date": "2026-02-12",
  "reason": "INACTIVITY",
  "reason_detail": "No significant updates or community mentions in 90+ days. Superseded by Claude, ChatGPT, and Jasper.",
  "last_score": 18,
  "peak_score": 72,
  "peak_date": "2024-06-15",
  "days_active": 487
}
```

### Graveyard Reasons
- `INACTIVITY` - No signals for 60+ days
- `SHUTDOWN` - Company closed
- `ACQUIRED` - Acquired and deprecated
- `SUPERSEDED` - Better alternatives emerged
- `PIVOTED` - No longer AI-focused
- `VAPORWARE` - Never delivered on promises

---

## Categories (20)

1. **Writing & Content** - Long-form, copywriting, editing
2. **Image Generation** - Art, photos, design assets
3. **Video Creation** - Generation, editing, avatars
4. **Audio & Voice** - TTS, music, voice cloning
5. **Coding & Dev Tools** - Copilots, editors, agents
6. **Productivity** - Notes, tasks, meetings
7. **Research & Analysis** - Search, papers, data
8. **Marketing** - Ads, campaigns, personalization
9. **Design** - UI/UX, logos, graphics
10. **Sales** - Outreach, intelligence, CRM
11. **Customer Support** - Chatbots, tickets, help
12. **Data & Analytics** - BI, visualization, ML
13. **HR & Recruiting** - Hiring, talent, HR ops
14. **Legal** - Contracts, compliance, research
15. **Finance** - Accounting, expenses, FP&A
16. **AI Agents & Chatbots** - Assistants, personas
17. **Automation** - Workflows, scraping, integration
18. **Social Media** - Scheduling, content, growth
19. **Education** - Learning, tutoring, courses
20. **3D & Game Dev** - Models, assets, engines

---

## Sub-Agent Configuration

### Agent: `curator`

**Identity:**
- Name: Curator
- Role: AI Tools Directory maintainer
- Runs: Daily at 6 AM PST (cron)

**Capabilities:**
- Web search (Brave)
- Web fetch (for APIs)
- File read/write
- Git operations
- GitHub API access

**Session:** Isolated (not main)

**Cron Job:**
```json
{
  "name": "AI Tools Curator - Daily Update",
  "schedule": { "kind": "cron", "expr": "0 6 * * *", "tz": "America/Los_Angeles" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the daily AI tools directory update. Follow CURATOR-PLAN.md steps: SCAN sources, SCORE tools, RANK by combined score, DISCOVER new tools, UPDATE HTML files, PUBLISH to GitHub. Log all changes to changelog.md and memory."
  }
}
```

---

## Manual Overrides

Curator can be instructed to:
- Force-add a tool (bypasses scoring for 7 days)
- Force-remove a tool (immediate graveyard)
- Adjust category
- Update description/pricing
- Flag for human review

Commands via main session:
```
"Curator: add [tool-url] to coding category"
"Curator: remove [tool-name], reason: shutdown"
"Curator: review [tool-name] - seems inactive"
```

---

## Success Metrics

Weekly review:
- Tools added this week
- Tools moved to graveyard
- Score changes > 20 points
- New discoveries from each source
- API rate limit usage

Monthly review:
- Category distribution health
- Graveyard growth rate
- Source effectiveness (which finds best tools)
- User feedback (if collecting)

---

## Phase 1 Implementation (Today)

1. ✅ Create directory structure
2. ✅ Seed tools.json with curated 200 (manual research)
3. ✅ Build scanner.py (Product Hunt + GitHub + basic X)
4. ✅ Build scorer.py
5. ✅ Build generator.py (HTML output)
6. ✅ Build publisher.py (git push)
7. ✅ Create curator agent
8. ✅ Set up daily cron job
9. ✅ Test full pipeline

## Phase 2 (Week 2)
- Add graveyard.html with styling
- Add HN API integration
- Add changelog.md auto-generation
- Improve Twitter search (builder accounts list)

## Phase 3 (Week 3)
- Add submission form (Google Form → webhook)
- Add "Hot This Week" section
- Add tool comparison feature
- Email digest option

---

## API Keys Needed

- GitHub: ✅ (gh auth)
- Product Hunt: Need to register app
- Twitter/X: ✅ (existing credentials)
- HackerNews: No auth needed
- Google Trends: SerpAPI or pytrends (no auth)

---

## Notes

- Start conservative: better to have 150 solid tools than 200 with filler
- Graveyard is valuable content too - "what died and why"
- Consider "Rising" section for tools 180-220 that are climbing
- Weekly "What's New" summary for social content
