"""Fetch price, movement, and volume data for a ticker using yfinance."""

import yfinance as yf


def get_price_data(ticker: str) -> dict:
    """Return a dict of key price/movement stats for a single ticker.

    Falls back gracefully with an 'error' key if data can't be fetched
    (e.g. bad ticker, temporary Yahoo hiccup) so one bad ticker doesn't
    crash the whole run.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")

        if hist.empty or len(hist) < 2:
            return {"ticker": ticker, "error": "No price history available"}

        latest = hist.iloc[-1]
        previous = hist.iloc[-2]

        close = float(latest["Close"])
        prev_close = float(previous["Close"])
        change = close - prev_close
        pct_change = (change / prev_close) * 100 if prev_close else 0.0

        return {
            "ticker": ticker,
            "close": round(close, 2),
            "change": round(change, 2),
            "pct_change": round(pct_change, 2),
            "volume": int(latest["Volume"]),
            "day_high": round(float(latest["High"]), 2),
            "day_low": round(float(latest["Low"]), 2),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def get_all_prices(tickers: list[str]) -> list[dict]:
    return [get_price_data(t) for t in tickers]


if __name__ == "__main__":
    # Quick manual test
    for row in get_all_prices(["AAPL", "MSFT"]):
        print(row)
