import pandas as pd
import yfinance as yf
from pathlib import Path


def get_price_from_yahoo(symbol: str) -> float:
    """
    Fetch the current price of a given symbol from Yahoo Finance.
    If the symbol is not found, return 0.
    """
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")['Close'].iloc[-1]  # Get the last closing price
        return round(price, 2) if not pd.isna(price) else 0
    except Exception:
        return 0


def enrich_all_csv(input_path: Path, output_path: Path) -> None:
    """
    Read the 'all.csv' file into a DataFrame, fetch stock prices for the 'symbol' column using Yahoo Finance,
    populate the 'Purchase Price' column, and save the enriched DataFrame to a new CSV file.
    """
    # Read the all.csv file into a DataFrame
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' does not exist.")
        return
    if 'Symbol' not in df.columns:
        print("Error: The file does not contain the 'symbol' column.")
        return

    # Update the 'Purchase Price' column with prices
    df['Purchase Price'] = df['Symbol'].apply(get_price_from_yahoo)

    # Save the enriched DataFrame to the specified output file
    df.to_csv(output_path, index=False)
    print(f"Enriched CSV has been saved to '{output_path}'.")


def main() -> None:
    """
    Main function to enrich the 'all.csv' file with stock prices.
    """
    # Define input and output file paths
    current_dir = Path(__file__).parent
    input_file = current_dir / 'all.csv'
    output_file = current_dir / 'all_enriched.csv'

    # Enrich the all.csv file
    enrich_all_csv(input_file, output_file)


if __name__ == "__main__":
    main()