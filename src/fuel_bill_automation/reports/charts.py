"""
chart_generator.py

A module to generate various types of charts from a pandas DataFrame and save them as images.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ChartGenerator:
    def __init__(self, dataframe):
        """
        Initialize the ChartGenerator with a pandas DataFrame.

        :param dataframe: pandas DataFrame containing the data.
        """
        self.df = dataframe

    def line_chart(self, x_col, y_col, filename, title=None, xlabel=None, ylabel=None):
        """
        Generate a line chart and save it as an image.

        :param x_col: Column name for the x-axis data.
        :param y_col: Column name for the y-axis data.
        :param filename: File path to save the image.
        :param title: (Optional) Title of the chart.
        :param xlabel: (Optional) Label for the x-axis.
        :param ylabel: (Optional) Label for the y-axis.
        """
        plt.figure()
        sns.lineplot(data=self.df, x=x_col, y=y_col)
        plt.title(title or "")
        plt.xlabel(xlabel or x_col)
        plt.ylabel(ylabel or y_col)
        plt.savefig(filename)
        plt.close()

    def bar_chart(self, x_col, y_col, filename, title=None, xlabel=None, ylabel=None):
        """
        Generate a bar chart and save it as an image.

        :param x_col: Column name for the x-axis categories.
        :param y_col: Column name for the y-axis values.
        :param filename: File path to save the image.
        :param title: (Optional) Title of the chart.
        :param xlabel: (Optional) Label for the x-axis.
        :param ylabel: (Optional) Label for the y-axis.
        """
        plt.figure()
        sns.barplot(data=self.df, x=x_col, y=y_col)
        plt.title(title or "")
        plt.xlabel(xlabel or x_col)
        plt.ylabel(ylabel or y_col)
        plt.savefig(filename)
        plt.close()

    def scatter_plot(
        self, x_col, y_col, filename, title=None, xlabel=None, ylabel=None, hue=None
    ):
        """
        Generate a scatter plot and save it as an image.

        :param x_col: Column name for the x-axis data.
        :param y_col: Column name for the y-axis data.
        :param filename: File path to save the image.
        :param title: (Optional) Title of the chart.
        :param xlabel: (Optional) Label for the x-axis.
        :param ylabel: (Optional) Label for the y-axis.
        :param hue: (Optional) Column name for color encoding.
        """
        plt.figure()
        sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=hue)
        plt.title(title or "")
        plt.xlabel(xlabel or x_col)
        plt.ylabel(ylabel or y_col)
        plt.savefig(filename)
        plt.close()

    def histogram(
        self, col, filename, bins=10, title=None, xlabel=None, ylabel="Frequency"
    ):
        """
        Generate a histogram and save it as an image.

        :param col: Column name for the data.
        :param filename: File path to save the image.
        :param bins: (Optional) Number of histogram bins.
        :param title: (Optional) Title of the chart.
        :param xlabel: (Optional) Label for the x-axis.
        :param ylabel: (Optional) Label for the y-axis.
        """
        plt.figure()
        sns.histplot(data=self.df, x=col, bins=bins)
        plt.title(title or "")
        plt.xlabel(xlabel or col)
        plt.ylabel(ylabel)
        plt.savefig(filename)
        plt.close()

    def box_plot(self, x_col, y_col, filename, title=None, xlabel=None, ylabel=None):
        """
        Generate a box plot and save it as an image.

        :param x_col: Column name for the categories.
        :param y_col: Column name for the data.
        :param filename: File path to save the image.
        :param title: (Optional) Title of the chart.
        :param xlabel: (Optional) Label for the x-axis.
        :param ylabel: (Optional) Label for the y-axis.
        """
        plt.figure()
        sns.boxplot(data=self.df, x=x_col, y=y_col)
        plt.title(title or "")
        plt.xlabel(xlabel or x_col)
        plt.ylabel(ylabel or y_col)
        plt.savefig(filename)
        plt.close()

    def heatmap(self, filename, title=None, cmap="viridis"):
        """
        Generate a heatmap of the correlation matrix and save it as an image.

        :param filename: File path to save the image.
        :param title: (Optional) Title of the chart.
        :param cmap: (Optional) Color map to use.
        """
        plt.figure(figsize=(10, 8))
        corr = self.df.corr()
        sns.heatmap(corr, annot=True, cmap=cmap)
        plt.title(title or "Correlation Heatmap")
        plt.savefig(filename)
        plt.close()
