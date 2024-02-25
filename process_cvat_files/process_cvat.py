#!/usr/bin/env python3
import os

# Function to read the single digit number from the mod directory
def read_single_digit_number(filepath):
    with open(filepath) as file:
        single_digit_number = int(file.readline().strip())
    # Change -1 to 0
    if single_digit_number == -1:
        single_digit_number = 0
    return single_digit_number

# Process files in mod directory one by one
def process_mod_files(mod_directory, obj_directory):
    for mod_filename in os.listdir(mod_directory):
        mod_filepath = os.path.join(mod_directory, mod_filename)
        if os.path.isfile(mod_filepath):
            # Read single digit number from the mod file
            single_digit_number = read_single_digit_number(mod_filepath)
            # Find matching file in obj directory
            obj_filename = mod_filename
            obj_filepath = os.path.join(obj_directory, obj_filename)
            if os.path.isfile(obj_filepath) and obj_filename.endswith('.txt'):
                # Update data in the obj file
                update_obj_file(obj_filepath, single_digit_number)

# Function to update data in the obj file
def update_obj_file(obj_filepath, single_digit_number):
    with open(obj_filepath, 'r') as file:
        lines = file.readlines()
    with open(obj_filepath, 'w') as file:
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0 and float(parts[0]) == 0:
                parts[0] = str(single_digit_number)
            file.write(' '.join(parts) + '\n')

# Directory paths
mod_directory = 'mod'
obj_directory = 'obj'

# Process files in mod directory and update corresponding obj files
process_mod_files(mod_directory, obj_directory)
