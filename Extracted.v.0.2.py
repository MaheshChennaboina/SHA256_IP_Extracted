import re
import pandas as pd
from datetime import datetime
import os

def extract_sha256_and_ips(input_file_path):
    # Define the regular expression patterns for SHA256 and modified IP addresses
    sha256_pattern = re.compile(r'\b[A-Fa-f0-9]{64}\b')
    ip_pattern = re.compile(r'\b(?:\d{1,3}\[.\]\d{1,3}\[.\]\d{1,3}\[.\]\d{1,3}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')

    # Create the output file path
    output_file_path = 'output.xlsx'

    # Open the input file for reading with explicit encoding
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        # Read the content of the input file
        input_content = input_file.read()

        # Find all SHA256 values and IP addresses in the input content using regex patterns
        sha256_values = sha256_pattern.findall(input_content)
        ip_values = ip_pattern.findall(input_content)

        # Combine SHA256 and IP values along with their corresponding categories (SHA256 or IP)
        all_values = sha256_values + ip_values
        categories = ['SHA256'] * len(sha256_values) + ['IP'] * len(ip_values)

        # Create a DataFrame using pandas
        df = pd.DataFrame({'Date': [datetime.now().date()] * len(all_values),
                           'Values': all_values,
                           'Category': categories})

        # Write the DataFrame to an Excel file
        df.to_excel(output_file_path, index=False)

        print(f"Values extracted from '{input_file_path}' and written to '{output_file_path}'.")

if __name__ == "__main__":
    # Replace 'input.txt' with the path to your input text file
    input_file_path = 'input.txt'

    # Call the function to extract SHA256 values, IP addresses, and write them to the Excel file
    extract_sha256_and_ips(input_file_path)
