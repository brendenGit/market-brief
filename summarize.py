"""Turn raw price + news data into a spoken-style daily market brief using Gemini."""

import os
import google.generativeai as genai

MODEL_NAME = "gemini-1.5-flash"  # fast + generous free tier


def _build_prompt(price_data: list[dict], news_data: dict[str, list[dict]]) -> str:
    lines = [
        "You are writing a short, spoken-word daily stock market brief that will be "
        "converted directly to audio and emailed to one person. Write it as natural "
        "spoken narration (no markdown, no bullet points, no headers) — like a friendly "
        "radio host giving a 2-3 minute market update. Open with a one-line date/overview, "
        "then cover each ticker below, then close with a brief one-sentence sign-off. "
        "Keep it factual and grounded only in the data provided — do not invent numbers.\n\n"
    ]

    for row in price_data:
        ticker = row["ticker"]
        if "error" in row:
            lines.append(f"Ticker {ticker}: data unavailable ({row['error']}).\n")
            continue

        lines.append(
            f"Ticker {ticker}: closed at ${row['close']}, "
            f"{'up' if row['change'] >= 0 else 'down'} {abs(row['pct_change'])}% "
            f"({'+' if row['change'] >= 0 else ''}{row['change']}), "
            f"day range ${row['day_low']}-${row['day_high']}, volume {row['volume']:,}."
        )

        headlines = news_data.get(ticker, [])
        if headlines:
            lines.append(f"Recent headlines for {ticker}:")
            for h in headlines:
                if h["title"]:
                    lines.append(f"  - {h['title']} ({h['source']})")
        lines.append("")

    return "\n".join(lines)


def summarize(price_data: list[dict], news_data: dict[str, list[dict]]) -> str:
    """Call Gemini to generate the spoken-style script. Returns plain text."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = _build_prompt(price_data, news_data)
    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    from fetch_prices import get_all_prices
    from fetch_news import get_all_news

    tickers = ["AAPL", "MSFT"]
    prices = get_all_prices(tickers)
    news = get_all_news(tickers)
    print(summarize(prices, news))
