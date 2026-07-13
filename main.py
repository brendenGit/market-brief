"""Daily Market Brief
Fetches price + news data for a list of tickers, summarizes it into a spoken
script with Gemini, converts it to audio, and emails it to you.

Run manually:   python main.py
Run on a schedule: see .github/workflows/daily_brief.yml
"""

import os
from datetime import date

from fetch_prices import get_all_prices
from fetch_news import get_all_news
from summarize import summarize
from tts import generate_audio
from send_email import send_email


def load_tickers(path: str = "tickers.txt") -> list[str]:
    # Allow overriding via env var (comma-separated), useful for GitHub Actions
    env_tickers = os.environ.get("TICKERS")
    if env_tickers:
        return [t.strip().upper() for t in env_tickers.split(",") if t.strip()]

    with open(path) as f:
        return [
            line.strip().upper()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def main():
    tickers = load_tickers()
    print(f"Tickers: {tickers}")

    print("Fetching price data...")
    prices = get_all_prices(tickers)

    print("Fetching news...")
    news = get_all_news(tickers)

    print("Summarizing with Gemini...")
    script_text = summarize(prices, news)

    print("Generating audio...")
    audio_path = generate_audio(script_text, output_path="market_brief.mp3")

    print("Sending email...")
    subject = f"Market Brief - {date.today().isoformat()}"
    send_email(subject, script_text, audio_path)

    print("Done.")


if __name__ == "__main__":
    main()
