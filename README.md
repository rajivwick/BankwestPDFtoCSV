# Bankwest PDF to CSV Converter

## Description

This project contains a Python script and Flask web application for converting Bankwest PDF files into a structured CSV format. The Python script processes transaction data from Bankwest PDFs and outputs a CSV file. The Flask application provides a simple web interface that allows users to specify input parameters for the conversion process.

## Features

- Extract text content from multiple PDF files
- Parse transaction data into a structured format
- Convert transaction data into CSV format
- Web interface for easy user interaction
- Option to customize the list of strings to ignore during processing

## Prerequisites

To run this application, you'll need:

- Python 3.7 or later
- Pip (Python package installer)
- Flask (Python web framework)
- PyMuPDF (Python library for PDF processing)
- Pandas (Python data analysis library)

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/rajivwick/BankwestPDFtoCSV.git
    ```
2. Navigate to the project directory:
    ```
    cd bankwest-pdf-to-csv-converter
    ```
3. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```
    python app.py
    ```
2. Open your web browser and navigate to `http://localhost:5000`.
3. Enter the directories for the PDF and CSV files, and the desired name of the CSV file.
4. Optionally, modify the list of strings to ignore during processing if there are items within the statement you would like avoid being added to the CSV.
5. Click `Convert` to start the conversion process.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/rajivwick/BankwestPDFtoCSV/issues) if you want to contribute.

## Contact

If you have any questions, please open an issue or submit a pull request.
