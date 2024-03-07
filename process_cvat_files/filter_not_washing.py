#!/usr/bin/env python3
import os

data_txt_folder = "./CVATDataSet1"
data_jpg_folder = "./DataSet1"

# Step 1: Check every single txt file in the data_txt folder
for txt_file in os.listdir(data_txt_folder):
    if txt_file.endswith(".txt"):
        txt_file_path = os.path.join(data_txt_folder, txt_file)
        
        # Step 2: Check if the file meets the specified criteria
        with open(txt_file_path, 'r') as file:
            first_line = file.readline().strip()
            
            if not first_line or first_line.startswith('0') or float(first_line.split()[0]) < 0:
                # Step 3: Remove the file from data_txt and data_jpg directories
                jpg_file = os.path.splitext(txt_file)[0] + ".jpg"
                jpg_file_path = os.path.join(data_jpg_folder, jpg_file)
                
                os.remove(txt_file_path)
                os.remove(jpg_file_path)
                
                #print(f"Removed {txt_file} and {jpg_file}.")

print("Script execution completed.")
