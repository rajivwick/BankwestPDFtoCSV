import os
from flask import Flask, request, render_template
from BankwestPDFtoCSV import process_directory  # assuming your_script.py is the name of your Python script


app = Flask(__name__)

# Initialize global variable
ignore_list = ['Credit Interest Rates',
                'OPENING BALANCE',
                 'CARRIED FORWARD',
                 'BROUGHT FORWARD',
                 'DEBIT INTEREST',
                 'BSB Number',
                 'CLOSING BALANCE',
                 'Debit Interest Rates 01',
                 'Page 1 of'
                 ]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ignore_list=ignore_list)  # Pass ignore_list to template

@app.route('/convert', methods=['POST'])
def convert():

    
    pdf_directory = request.form.get('pdf_directory')
    csv_directory = request.form.get('csv_directory')
    csv_name = request.form.get('csv_name')
    additional_ignore_list = request.form.get('additional_ignore_list')
    
    remove_ignore_list = request.form.get('remove_ignore_list')
    
    csv_name = csv_name + '.csv'
    global ignore_list
    
    # Add additional ignore values to global ignore_list
    if additional_ignore_list:
        additional_ignore_list = additional_ignore_list.split(",")
        ignore_list += additional_ignore_list  # Assuming comma-separated values
    
    if remove_ignore_list:
        items_to_remove = remove_ignore_list.split(',')
        for item in items_to_remove:
            item = item.strip()  # Remove leading/trailing white spaces
            if item in ignore_list:
                ignore_list.remove(item)

    

    # Construct the full CSV path by joining the directory and name
    csv_path = os.path.join(csv_directory, csv_name)

    # Call the process_directory function with the user's input
    process_directory(pdf_directory, csv_path, ignore_list)

    return "Conversion complete!"

if __name__ == "__main__":
    app.run(debug=True)