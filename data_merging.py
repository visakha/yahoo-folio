import os
import pandas as pd
from pathlib import Path
from typing import List, Dict


def get_csv_files(folder_path: Path) -> List[Path]:
    """
    Get a list of all CSV files in a given folder.
    """
    return [file for file in folder_path.iterdir() if file.suffix == ".csv"]


def read_and_prepare_dataframe(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file into a Pandas DataFrame and add a 'folio' column
    containing the stripped file name (without 'portfolio-' prefix).
    """
    # Get the file name without the extension
    stripped_name = file_path.stem.replace("portfolio-", "")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Add the 'folio' column
    df["folio"] = stripped_name

    return df


def merge_dataframes(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge a list of Pandas DataFrames into a single DataFrame, ignoring indices.
    """
    return pd.concat(dataframes, ignore_index=True)


def write_dataframe_to_csv(df: pd.DataFrame, output_path: Path) -> None:
    """
    Write a Pandas DataFrame to a CSV file.
    """
    df.to_csv(output_path, index=False)


def main() -> None:
    """
    Main function to read all CSV files from a folder, add a 'folio' column to each,
    merge them, and write the result to 'all.csv'.
    """
    # Define the folder and output paths
    current_dir = Path(__file__).parent
    folder_path = current_dir / "resources/yahoo-folio-dwnld"
    output_file = current_dir / "all.csv"

    # Ensure the folder exists
    if not folder_path.exists():
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Get list of CSV files
    csv_files = get_csv_files(folder_path)
    if not csv_files:
        print(f"No CSV files found in the folder '{folder_path}'.")
        return

    # Process each file into a DataFrame
    dataframes = [read_and_prepare_dataframe(file) for file in csv_files]

    # Merge the DataFrames
    merged_df = merge_dataframes(dataframes)

    # Write the merged DataFrame to a CSV file
    write_dataframe_to_csv(merged_df, output_file)

    print(f"Merged CSV has been written to '{output_file}'.")


if __name__ == "__main__":
    main()