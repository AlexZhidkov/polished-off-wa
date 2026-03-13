---
name: industry-news-monitor
description: Monitor and summarize industry news for concrete polishing and epoxy flooring businesses. Search web for latest news, categorize by geography (International, Australian, WA), and compile structured summaries. Use when setting up automated news monitoring, manually checking industry updates, or configuring news alerts for the concrete polishing/epoxy flooring industry.
---

# Industry News Monitor

Monitor concrete polishing and epoxy flooring industry news and compile structured summaries.

## Use Cases

1. **Automated weekly reports** — Set up cron job for regular news digests
2. **Manual news check** — On-demand industry update
3. **Configure monitoring** — Adjust search terms, frequency, or output format

## Output Format

Standard email/report structure:

```
Subject: Weekly Industry News - Concrete Polishing & Epoxy - [Date]

========================================
INTERNATIONAL NEWS
========================================
• [Brief summary 1-2 sentences] — [Link]

========================================
AUSTRALIAN NEWS
========================================
• [Brief summary 1-2 sentences] — [Link]

========================================
WA NEWS
========================================
• [Brief summary 1-2 sentences] — [Link]
```

## Search Strategy

### Geographic Tiers

| Tier | Search Terms | Focus |
|------|--------------|-------|
| **International** | Global industry sources | Technology, trends, major players |
| **Australian** | National news, industry bodies | National regulations, projects, pricing |
| **WA** | Western Australia specific | Local competitors, projects, regulations |

### Key Topics to Capture

- Pricing trends and market shifts
- New technologies and equipment
- Industry regulations and standards
- Major commercial/residential projects
- Competitor activity (new services, expansions)
- Environmental/sustainability developments

## Workflow

### Automated Setup (Cron)

See [references/cron-setup.md](references/cron-setup.md) for cron job configuration.

### Manual Execution

1. Search web for news from past week
2. Categorize by geographic tier
3. Summarize each item (1-2 sentences)
4. Compile into formatted email
5. Send to configured recipient

## Configuration

Edit [references/config.md](references/config.md) to customize:
- Recipient email
- Search queries
- Frequency
- Categories

## Scripts

- `scripts/news_check.py` — Main news gathering and compilation script
