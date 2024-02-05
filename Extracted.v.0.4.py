import re
import pandas as pd
from datetime import datetime
import os

def extract_sha256_and_ips(input_file_path):
    # Define the regular expression patterns for SHA256 and modified IP addresses
    sha256_pattern = re.compile(r'\b[A-Fa-f0-9]{64}\b')
    ip_pattern = re.compile(r'\b(?:\d{1,3}\[.\]\d{1,3}\[.\]\d{1,3}\[.\]\d{1,3}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')

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

        # Get the user's home directory
        home_directory = os.path.expanduser("~")

        # Create the output file path in the user's home directory
        output_file_path = os.path.join(home_directory, 'output.xlsx')

        # Write the DataFrame to an Excel file
        df.to_excel(output_file_path, index=False)

        # Print the output file path
        print(f"Values extracted from '{input_file_path}' and written to '{output_file_path}'.")

    return output_file_path

def remove_matching_rows(output_excel_path, user_excel_path):
    # Read the output Excel sheet
    output_df = pd.read_excel(output_excel_path)

    # Read the user-provided Excel sheet
    user_df = pd.read_excel(user_excel_path)

    # Convert the 'Values' column in user_df to a set for faster lookups
    user_values_set = set(user_df['Values'])

    # Use the 'isin' method to create a boolean mask for matching values
    mask = output_df['Values'].isin(user_values_set)

    # Remove rows in the output sheet where the values are present in the user-provided sheet
    final_output_df = output_df[~mask]

    # Get the user's home directory
    home_directory = os.path.expanduser("~")

    # Create the final output Excel sheet path in the user's home directory
    final_output_path = os.path.join(home_directory, 'final_output.xlsx')

    # Write the final output DataFrame to an Excel file
    final_output_df.to_excel(final_output_path, index=False)

    # Print the final output file path
    print(f"Final output written to '{final_output_path}'.")

if __name__ == "__main__":
    # Replace 'input.txt' and 'user_provided.xlsx' with the actual file paths
    input_file_path = 'input.txt'
    user_excel_path = 'user_provided.xlsx'

    # Call the function to extract SHA256 values and write them to the Excel file
    output_excel_path = extract_sha256_and_ips(input_file_path)

    # Call the function to remove matching rows and get the final output Excel sheet
    remove_matching_rows(output_excel_path, user_excel_path)
