#!/usr/bin/env python3

import os
import csv

# Function to read each text file in a directory
def read_text_files(directory):
    # List to store data from text files
    data = []
    
    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.read().strip()  # Read content and remove leading/trailing whitespace
                content = (max(0, int(content)))

                # Adjust filename format
                file_number = int(filename.split("_")[-1].split(".")[0])  # Extract the number from the filename
                new_filename = "frame_{:06d}".format(file_number)  # Format the new filename with 6 digits

                data.append((new_filename, content))  # Append filename and content to the list
    return data

# Function to write data to a CSV file
def write_to_csv(data, output_file):
    # Define headers for CSV file
    headers = ['Filename', 'Content']
    
    # Write data to CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(data)  # Write data rows

# Main function
def main():
    # Directory containing text files
    directory = './DataSet1'
    
    # Output CSV file
    output_file = 'output.csv'
    
    # Read data from text files
    data = read_text_files(directory)
    
    # Write data to CSV file
    write_to_csv(data, output_file)
    
    print("CSV file generated successfully.")

if __name__ == "__main__":
    main()
