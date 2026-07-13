# Daily Market Brief

Emails you a short audio briefing (+ text) covering price movement and news
for a list of stock tickers, once a day, automatically. Built entirely with
free tools:

| Step              | Tool                              | Cost |
|-------------------|------------------------------------|------|
| Price data        | `yfinance`                        | Free |
| News headlines     | Google News RSS                    | Free |
| Summarization      | Google Gemini API (`gemini-1.5-flash`) | Free tier |
| Text-to-speech     | `edge-tts`                         | Free |
| Email delivery      | Gmail SMTP                         | Free |
| Scheduling          | GitHub Actions                     | Free (public/private repo, within free minutes) |

## 1. Get a free Gemini API key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with a Google account and click "Create API key."
3. Copy the key — you'll add it as a GitHub secret below.

## 2. Create a Gmail "app password"
Gmail won't let scripts log in with your normal password. Use an app password instead:
1. Turn on 2-Step Verification on your Google account (required for app passwords): https://myaccount.google.com/security
2. Go to https://myaccount.google.com/apppasswords
3. Create a new app password (name it anything, e.g. "market-brief"), copy the 16-character password.

## 3. Put this project in a GitHub repo
1. Create a new repo (can be private) and push these files to it.
2. It's fine to keep it private — GitHub Actions free minutes still apply.

## 4. Add your secrets to the repo
In your repo: **Settings → Secrets and variables → Actions**

Add these **Repository secrets**:
- `GEMINI_API_KEY` — from step 1
- `GMAIL_ADDRESS` — the Gmail address you're sending from
- `GMAIL_APP_PASSWORD` — from step 2
- `RECIPIENT_EMAIL` — where you want the brief sent (can be the same Gmail address)

Add this **Repository variable** (same page, "Variables" tab):
- `TICKERS` — comma-separated list, e.g. `AAPL,MSFT,NVDA`
  (or just edit `tickers.txt` directly in the repo instead — either works; the env var takes priority if both are set)

## 5. Test it
Go to the **Actions** tab in your repo → "Daily Market Brief" → **Run workflow**
button. This triggers it manually so you don't have to wait for the schedule.
Check your email a minute or two later.

## 6. Adjust the schedule
The workflow is set to run weekdays at 9:00 PM UTC (1:00 PM PT / 4:00 PM ET) —
right after US markets close. Edit the `cron` line in
`.github/workflows/daily_brief.yml` to change the time. Cron times are always
in UTC.

## Running locally (optional, for testing)
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="..."
export GMAIL_ADDRESS="..."
export GMAIL_APP_PASSWORD="..."
export RECIPIENT_EMAIL="..."
python main.py
```

## Notes & limitations
- `yfinance` and Google News RSS are free but unofficial — fine for personal
  use, but could occasionally hiccup if the underlying site changes something.
- Gemini's free tier (as of writing) allows generous daily usage — far more
  than one request/day needs, so you won't hit limits with this workflow.
- To change the narrator voice, edit `VOICE` in `tts.py` — a few options are
  listed in comments there.
- To change which tickers are covered, edit `tickers.txt` or the `TICKERS`
  repo variable.
