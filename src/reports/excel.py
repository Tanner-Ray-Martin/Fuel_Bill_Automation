"""
data_summary.py

A module to process a list of pandas DataFrames and generate summary tables,
grouped data, and other useful summaries for end users.
"""

import pandas as pd


class DataFrameSummarizer:
    def __init__(self, dataframes, names=None):
        """
        Initialize the DataFrameSummarizer with a list of pandas DataFrames.

        :param dataframes: List of pandas DataFrames.
        :param names: (Optional) List of names for the DataFrames.
        """
        self.dataframes = dataframes
        if names is None:
            self.names = [f"DataFrame_{i}" for i in range(len(dataframes))]
        else:
            self.names = names

    def describe(self):
        """
        Generate descriptive statistics for each DataFrame.

        :return: Dictionary with DataFrame names as keys and their descriptive statistics as values.
        """
        descriptions = {}
        for name, df in zip(self.names, self.dataframes):
            descriptions[name] = df.describe(include="all")
        return descriptions

    def group_by(self, group_columns, agg_funcs):
        """
        Group each DataFrame by the specified columns and aggregate using the provided functions.

        :param group_columns: List of column names to group by.
        :param agg_funcs: Dictionary of aggregation functions, e.g., {'column1': 'mean', 'column2': 'sum'}
        :return: Dictionary with DataFrame names as keys and their grouped DataFrames as values.
        """
        grouped_data = {}
        for name, df in zip(self.names, self.dataframes):
            grouped = df.groupby(group_columns).agg(agg_funcs).reset_index()
            grouped_data[name] = grouped
        return grouped_data

    def value_counts(self, columns):
        """
        Get counts of unique values in specified columns for each DataFrame.

        :param columns: List of column names.
        :return: Nested dictionary with DataFrame names and their value counts per specified column.
        """
        counts = {}
        for name, df in zip(self.names, self.dataframes):
            counts[name] = {}
            for col in columns:
                counts[name][col] = df[col].value_counts()
        return counts

    def correlation_matrix(self):
        """
        Compute the correlation matrix for each DataFrame.

        :return: Dictionary with DataFrame names as keys and their correlation matrices as values.
        """
        correlations = {}
        for name, df in zip(self.names, self.dataframes):
            correlations[name] = df.corr()
        return correlations

    def missing_values_table(self):
        """
        Summarize missing values in each DataFrame.

        :return: Dictionary with DataFrame names as keys and their missing values summary as values.
        """
        missing_values = {}
        for name, df in zip(self.names, self.dataframes):
            total = df.isnull().sum()
            percent = (df.isnull().sum() / len(df)) * 100
            missing = pd.concat([total, percent], axis=1, keys=["Total", "Percent"])
            missing_values[name] = missing
        return missing_values

    def pivot_table(self, index, columns, values, aggfunc="mean"):
        """
        Create pivot tables for each DataFrame.

        :param index: Column(s) to use as the index.
        :param columns: Column(s) to use as the columns.
        :param values: Column(s) to aggregate.
        :param aggfunc: Aggregation function to use (default is 'mean').
        :return: Dictionary with DataFrame names as keys and their pivot tables as values.
        """
        pivot_tables = {}
        for name, df in zip(self.names, self.dataframes):
            pivot = pd.pivot_table(
                df, index=index, columns=columns, values=values, aggfunc=aggfunc
            )
            pivot_tables[name] = pivot
        return pivot_tables
