#!/usr/bin/env python3
import os

def rename_files(directory):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    mod_directory = os.path.join(script_directory, 'mod')

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    # Create 'mod' directory if it doesn't exist
    os.makedirs(mod_directory, exist_ok=True)

    # List all files in the directory
    files = os.listdir(directory)

    # Filter out only the .txt files
    txt_files = [file for file in files if file.endswith('.txt')]

    # Rename each txt file
    for old_name in txt_files:
        # Extract the frame number
        frame_number = old_name.split('_')[-1].split('.')[0]

        # Generate the new name with leading zeros
        new_name = f"frame_{frame_number.zfill(6)}.txt"

        # Build the full path for old and new names
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(mod_directory, new_name)

        # Rename the file
        os.rename(old_path, new_path)
        #print(f"Renamed '{old_name}' to '{new_name}'")

# Specify the directory containing the txt files
directory = './DataSet1'

# Call the function to rename the files
rename_files(directory)
