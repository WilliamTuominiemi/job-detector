# Job Detector

An automated scraper that monitors tech career pages for new job openings and sends alerts via Telegram.

## Workflow

1. **Scrape** - Uses Playwright to fetch job listings.
2. **Parse** - Sends raw page text to Gemini (`gemini-3.5-flash-lite`) to extract structured `title|company|location` lines.
3. **Deduplicate** - Compares parsed jobs against a PostgreSQL `seen_jobs` table using fuzzy string matching (`difflib.SequenceMatcher` > 0.9 similarity).
4. **Store & Notify** - Saves unseen jobs to PostgreSQL and sends a summary message to Telegram.

## Automation

Runs daily at **16:00 UTC** (or manually) via GitHub Actions (`.github/workflows/daily.yml`).

### Required Environment Variables / Secrets

- `GEMINI_API_KEY` — Google GenAI API key
- `DATABASE_URL` — PostgreSQL connection string
- `TELEGRAM_BOT_TOKEN` — Telegram bot token
- `TELEGRAM_CHAT_ID` — Target Telegram chat ID
