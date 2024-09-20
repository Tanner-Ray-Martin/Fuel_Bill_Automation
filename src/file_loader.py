import os
import pandas as pd
import tabula
import PyPDF2


def load_file_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Load a file (pdf, xlsx, xlsm, csv) into a pandas DataFrame.

    :param file_path: Path to the file to load
    :return: A pandas DataFrame containing the data
    :raises ValueError: If the file format is not supported
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Load CSV file
    if file_extension == ".csv":
        return pd.read_csv(file_path)

    # Load Excel file (supports .xlsx and .xlsm)
    elif file_extension in [".xlsx", ".xlsm"]:
        return pd.read_excel(file_path, engine="openpyxl")

    # Load PDF file
    elif file_extension == ".pdf":
        # Use tabula-py to extract tables from PDF into DataFrame
        dfs = tabula.read_pdf(file_path, pages="all", multiple_tables=True)
        if dfs:
            # Concatenate all extracted tables into a single DataFrame
            return pd.concat(dfs, ignore_index=True)
        else:
            # Use PyPDF2 to extract text-based data
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text_data = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text_data += page.extract_text()

            # If no tables are found, return text data in DataFrame
            return pd.DataFrame({"Extracted_Text": [text_data]})

    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


# Example usage
if __name__ == "__main__":
    file_path = input("Enter the file path: ")

    try:
        df = load_file_to_dataframe(file_path)
        print("Data loaded successfully!")
        print(df.head())  # Display the first 5 rows of the DataFrame
    except Exception as e:
        print(f"Error: {str(e)}")
