"""Turn raw price + news data into a spoken-style daily market brief using Gemini."""

import os
from google import genai
from google.genai import errors as genai_errors

# Tried in order — Google renames/retires Gemini model IDs somewhat often,
# so if the first one 404s, we fall back to the next rather than failing outright.
MODEL_CANDIDATES = [
    "gemini-3-flash-preview",
    "gemini-flash-latest",
    "gemini-2.5-flash",
]


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

    client = genai.Client(api_key=api_key)
    prompt = _build_prompt(price_data, news_data)

    last_error = None
    for model_name in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            return response.text.strip()
        except genai_errors.ClientError as e:
            # 404 = model not found/available for this project; try the next candidate.
            # Any other error (bad key, quota, etc.) should surface immediately.
            if getattr(e, "code", None) == 404 or "NOT_FOUND" in str(e):
                last_error = e
                continue
            raise

    raise RuntimeError(
        f"None of the candidate Gemini models worked: {MODEL_CANDIDATES}. "
        f"Last error: {last_error}"
    )


if __name__ == "__main__":
    from fetch_prices import get_all_prices
    from fetch_news import get_all_news

    tickers = ["AAPL", "MSFT"]
    prices = get_all_prices(tickers)
    news = get_all_news(tickers)
    print(summarize(prices, news))
