import pandas as pd


def filter_by_month(
    df: pd.DataFrame, date_column: str, month: int, year: int
) -> pd.DataFrame:
    """
    Filter the DataFrame by the given month and year.

    :param df: The input DataFrame
    :param date_column: Name of the column containing the date or datetime
    :param month: The month to filter by
    :param year: The year to filter by
    :return: Filtered DataFrame
    """
    df[date_column] = pd.to_datetime(
        df[date_column]
    )  # Ensure the date column is in datetime format
    filtered_df = df[
        (df[date_column].dt.month == month) & (df[date_column].dt.year == year)
    ]
    return filtered_df


def check_job_number(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    employee_column: str,
    date_column: str,
    job_number_column: str,
):
    """
    Checks that rows with the same employee name and the same date have the same job number.
    Returns a good DataFrame where job numbers match and a bad DataFrame where they do not.

    :param df1: First DataFrame
    :param df2: Second DataFrame (optional)
    :param employee_column: Column name for the employee
    :param date_column: Column name for the date or datetime
    :param job_number_column: Column name for the job number
    :return: Tuple of (good_dataframe, bad_dataframe)
    """
    # Merge both DataFrames on employee name and date
    merged_df = pd.merge(
        df1, df2, on=[employee_column, date_column], suffixes=("_df1", "_df2")
    )

    # Create a boolean mask where job numbers match
    job_number_match = (
        merged_df[job_number_column + "_df1"] == merged_df[job_number_column + "_df2"]
    )

    # Separate good and bad DataFrames
    good_df = merged_df[job_number_match]
    bad_df = merged_df[~job_number_match]

    return good_df, bad_df


def process_dataframes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    date_column: str,
    employee_column: str,
    job_number_column: str,
    month: int,
    year: int,
):
    """
    Process the DataFrames, filtering by month, then checking job numbers.

    :param df1: First DataFrame
    :param df2: Second DataFrame
    :param date_column: Column name for the date or datetime
    :param employee_column: Column name for the employee
    :param job_number_column: Column name for the job number
    :param month: Month to filter by
    :param year: Year to filter by
    :return: Tuple of (good_dataframe, bad_dataframe)
    """
    # Filter both DataFrames by the specific month and year
    df1_filtered = filter_by_month(df1, date_column, month, year)
    df2_filtered = filter_by_month(df2, date_column, month, year)

    # Check job number consistency
    good_df, bad_df = check_job_number(
        df1_filtered, df2_filtered, employee_column, date_column, job_number_column
    )

    return good_df, bad_df


# Example usage
if __name__ == "__main__":
    # Example DataFrames for testing
    data1 = {
        "Employee": ["John Doe", "Jane Smith", "John Doe"],
        "Date": ["2024-09-01", "2024-09-02", "2024-09-03"],
        "JobNumber": ["123", "456", "789"],
    }

    data2 = {
        "Employee": ["John Doe", "Jane Smith", "John Doe"],
        "Date": ["2024-09-01", "2024-09-02", "2024-09-03"],
        "JobNumber": ["123", "456", "000"],
    }

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    # Process the DataFrames
    good_df, bad_df = process_dataframes(
        df1, df2, "Date", "Employee", "JobNumber", 9, 2024
    )

    print("Good DataFrame:")
    print(good_df)

    print("\nBad DataFrame:")
    print(bad_df)
