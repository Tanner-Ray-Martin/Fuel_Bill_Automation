import os
from datetime import datetime, timedelta
from typing import List, Optional

import pandas as pd
import pdfplumber
from pdfplumber.page import Page

from fuel_bill_automation.configs.constants import (
    LABOR_REPORT_DIRECTORY,
    BEST_PASS_FINANCIAL_SUMMARY_PDF,
    # Include other constants as needed
)


def find_xlsx_files_by_modified_date(
    folder_path: str, year: int, month: int
) -> List[str]:
    """
    Scans a folder for .xlsx files and returns a list of file paths that were modified
    within the given month, including one week prior and one week after the month.
    """
    result = []

    # Calculate the date range (start of the previous week to end of the following week)
    first_day_of_month = datetime(year, month, 1)
    if month == 12:
        last_day_of_month = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day_of_month = datetime(year, month + 1, 1) - timedelta(days=1)

    start_range = first_day_of_month - timedelta(days=7)
    end_range = last_day_of_month + timedelta(days=7)

    # Iterate through files in the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                # Check if the file's modified date is within the target range
                if start_range <= modified_time <= end_range:
                    result.append(file_path)

    return result


def load_and_concatenate_xlsx(
    file_paths: List[str], max_columns: Optional[int] = None
) -> pd.DataFrame:
    """
    Takes a list of .xlsx file paths, loads the first sheet in each file as a DataFrame,
    sets the first row as the column names if the column names are not all strings,
    and returns a DataFrame of all the data combined after removing duplicates.
    """
    dataframes = []

    for file_path in file_paths:
        # Load the first sheet of the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=0)
        if max_columns is not None:
            df = df.iloc[:, :max_columns]

        # Check if the column names are not all strings
        if not all(isinstance(col, str) for col in df.columns) or any(
            "Unnamed" in str(col) for col in df.columns
        ):
            # Set the first row as the column names
            df.columns = df.iloc[0]
            df = df[1:]

        # Append the DataFrame to the list
        dataframes.append(df)

    # Concatenate all the DataFrames into one and remove duplicates
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True).drop_duplicates()
    else:
        combined_df = pd.DataFrame()

    return combined_df


def clean_column_name(column: str) -> str:
    """Cleans a DataFrame column name by replacing newline characters with spaces."""
    return column.replace("\n", " ")


def extract_tables_from_pdf(file_path: str) -> pd.DataFrame:
    """
    Extracts tables from a PDF file and returns them as a DataFrame.
    """
    all_tables = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = extract_tables_from_page(page)
            for table in tables:
                processed_df = process_table(table)
                if not processed_df.empty:
                    all_tables.append(processed_df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    else:
        return pd.DataFrame()


def extract_tables_from_page(page: Page) -> List[List[List[str | None]]]:
    """Extracts tables from a single PDF page."""
    return page.extract_tables()


def process_table(table: List[List[str | None]]) -> pd.DataFrame:
    """Processes a single table extracted from the PDF."""
    if not table:
        return pd.DataFrame()

    df = pd.DataFrame(table[1:], columns=table[0])
    df.columns = [clean_column_name(col) for col in df.columns]
    df.replace("", None, inplace=True)
    if "DEPARTMENT" in df.columns:
        return process_departments(df)
    else:
        return pd.DataFrame()


def process_departments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the 'DEPARTMENT' column, splitting it into multiple departments
    and extracting corresponding data.
    """
    # Remove rows where 'DESCRIPTION' is 'YTD' or 'PERIOD'
    df = df[~df["DESCRIPTION"].isin(["YTD", "PERIOD"])]

    # Split departments and process each separately
    departments = df["DEPARTMENT"].iloc[0].split("\n")
    all_department_dfs = []

    for idx, department in enumerate(departments):
        if department == "ACCOUNTS RECEIVABLE":
            continue
        department_df = extract_department_data(df, idx)
        if not department_df.empty:
            department_df["DEPARTMENT"] = department
            # Reorder columns to match original DataFrame
            for col in df.columns[1:].tolist():
                if col not in department_df.columns:
                    department_df[col] = None
            department_df = department_df[df.columns.tolist()]
            all_department_dfs.append(department_df)

    if all_department_dfs:
        return pd.concat(all_department_dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def extract_department_data(df: pd.DataFrame, department_idx: int) -> pd.DataFrame:
    """
    Extracts data for a single department based on the department index.
    """
    department_df = pd.DataFrame()
    for col in df.columns[1:]:  # Skip 'DEPARTMENT' column
        column_values = extract_column_values(df, col, department_idx)
        try:
            department_df[col] = column_values
        except ValueError:
            department_df[col] = None
    department_df.replace("", None, inplace=True)
    department_df.dropna(how="all", inplace=True)
    return department_df


def extract_column_values(
    df: pd.DataFrame, col: str, department_idx: int
) -> List[Optional[str]]:
    """
    Extracts column values for a specific department.
    """
    try:
        column_data = df[col].iloc[department_idx]
        if isinstance(column_data, str):
            return column_data.split("\n")
        else:
            return [column_data]
    except (IndexError, AttributeError):
        # Handle cases where data is missing or not in the expected format
        return [None] * len(df)


def save_dataframe_to_csv(df: pd.DataFrame, file_name: str) -> None:
    """
    Saves a DataFrame to a CSV file and opens it.
    """
    df.to_csv(file_name, index=False)
    os.startfile(file_name)


def main():
    # Example usage
    folder_path = LABOR_REPORT_DIRECTORY
    year = 2024
    month = 8  # August

    # Process PDF file
    financial_summary_df = extract_tables_from_pdf(BEST_PASS_FINANCIAL_SUMMARY_PDF)

    # Save results to CSV
    save_dataframe_to_csv(financial_summary_df, "best_pass_financial_summary.csv")


if __name__ == "__main__":
    main()
