import argparse
from pathlib import Path
import pandas as pd
import yfinance as yf

SYMBOL = "MSTY"

def fetch_price(symbol: str) -> float | None:
    """Fetch the latest closing price for the given symbol."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        price = hist['Close'].iloc[-1]
        if pd.isna(price):
            return None
        return float(price)
    except Exception:
        return None

def fetch_history(symbol: str, period: str = "1mo") -> pd.DataFrame | None:
    """Fetch historical OHLC data for the given symbol."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        return hist[['Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        return None

def cmd_price(args: argparse.Namespace) -> None:
    price = fetch_price(SYMBOL)
    if price is not None:
        print(f"{SYMBOL} current price: {price:.2f}")
    else:
        print(f"Unable to fetch price for {SYMBOL}.")

def cmd_history(args: argparse.Namespace) -> None:
    hist = fetch_history(SYMBOL, args.period)
    if hist is None or hist.empty:
        print(f"Unable to fetch history for {SYMBOL}.")
        return
    print(hist)
    if args.save:
        hist.to_csv(args.save)
        print(f"History saved to {args.save}")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track MSTY stock information")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_price = subparsers.add_parser("price", help="Show current price")
    parser_price.set_defaults(func=cmd_price)

    parser_hist = subparsers.add_parser("history", help="Show historical data")
    parser_hist.add_argument("--period", default="1mo",
                             help="Data period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max")
    parser_hist.add_argument("--save", type=Path,
                             help="Optional CSV file to save history")
    parser_hist.set_defaults(func=cmd_history)

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
