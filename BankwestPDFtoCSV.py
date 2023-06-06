import fitz  # PyMuPDF
import pandas as pd
import re  # regular expressions
import csv
import os
import datetime

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def parse_transactions(text):
    # Break into lines
    lines = text.split('\n')

    # Prepare a list to hold transactions
    transactions = []

    # Find the line with 'TRANSACTION'
    transaction_start = 0
    for i, line in enumerate(lines):
        if 'TRANSACTION' in line:
            transaction_start = i + 1
            break

    print(f"Transaction start line: {transaction_start}")

    # Go through each line after 'TRANSACTION' and accumulate transactions
    transaction = {}
    last_balance = 0.0
    for line in lines[transaction_start:]:
        if re.match(r'\d{2} \w{3} \d{2}', line):  # e.g., '16 APR 20'
            # If we encounter a new date and we've already started a transaction,
            # append the current transaction to the list and start a new one
            if transaction:
                transaction['Balance'] = transaction.pop('TempBalance', 0)
                difference = transaction['Balance'] - last_balance
                if difference > 0:
                    transaction['Credit'] = difference
                elif difference < 0:
                    transaction['Debit'] = -difference
                last_balance = transaction['Balance']
                transactions.append(transaction)
                transaction = {}
            transaction['Date'] = line
            transaction['Debit'] = ''  # Initialize 'Debit' field
            transaction['Credit'] = ''  # Initialize 'Credit' field
        elif re.match(r'\$.*', line):  # e.g., '$2.46'
            clean_line = re.sub(r'[^0-9.]', '', line)
            try:
                print(line)
                current_balance = float(clean_line)
                print(current_balance)
                transaction['TempBalance'] = current_balance
            except ValueError:
                # skip lines that cannot be converted to float
                continue
        else:  # Assume it's the transaction description
            if 'Particulars' in transaction:
                transaction['Particulars'] += ' ' + line  # concatenate additional description lines
            else:
                transaction['Particulars'] = line

    # Don't forget to append the last transaction
    if transaction:
        transaction['Balance'] = transaction.pop('TempBalance', 0)
        difference = transaction['Balance'] - last_balance
        if difference > 0:
            transaction['Credit'] = difference
        elif difference < 0:
            transaction['Debit'] = -difference
        transactions.append(transaction)

    
    return transactions



def append_transactions_to_csv(transactions, csv_file_path, ignore_list):
    # Specify the column order
    column_order = ['Date', 'Particulars', 'Credit', 'Debit', 'Balance']

    # Check if the file exists. If it doesn't, write the header
    file_exists = os.path.isfile(csv_file_path)

 
    # Append transactions to CSV
    with open(csv_file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=column_order)
        if not file_exists:
            writer.writeheader()
        for transaction in transactions:
            if not any(ignore_str in transaction['Particulars'] for ignore_str in ignore_list):
                writer.writerow(transaction)
    print(ignore_list)

def process_multiple_pdfs(pdf_file_paths, csv_file_path, ignore_list):
    # First, we'll clear out the old CSV file if it exists
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    # Then we'll process each PDF file in turn
    for pdf_file_path in pdf_file_paths:
        text = extract_text_from_pdf(pdf_file_path)
        transactions = parse_transactions(text)
        append_transactions_to_csv(transactions, csv_file_path, ignore_list)

def process_directory(pdf_directory, csv_file_path,ignore_list):
    # List all files in the directory
    files = os.listdir(pdf_directory)

    # Filter for PDF files
    pdf_file_paths = [os.path.join(pdf_directory, file) for file in files if file.endswith('.pdf')]

    # Process the PDF files
    process_multiple_pdfs(pdf_file_paths, csv_file_path, ignore_list)




