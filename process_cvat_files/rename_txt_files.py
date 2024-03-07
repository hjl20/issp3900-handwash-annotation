#!/usr/bin/env python3
import os

CVAT_DIR = "./CVATDataSet1"
PUB_DIR = "./DataSet1_txt"

# Check if directories exist
if not os.path.isdir(CVAT_DIR) or not os.path.isdir(PUB_DIR):
    print(f"Error: One or both of the directories ({CVAT_DIR} and {PUB_DIR}) not found.")
    exit(1)

# Function to get a list of txt files in a directory and sort them
def get_sorted_txt_files(directory):
    txt_files = [entry.name for entry in os.scandir(directory) if entry.is_file() and entry.name.endswith('.txt')]
    return sorted(txt_files)

# Function to custom sort PUB files based on timestamp and frame number
def custom_sort_pub_files(file_list):
    return sorted(file_list, key=lambda x: (x.split('_frame_')[0], int(x.split('_frame_')[-1].split('.')[0])))

# Get sorted lists of txt files for CVAT and all files (regardless of type) for PUB directory
cvat_files = get_sorted_txt_files(CVAT_DIR)
pub_files = custom_sort_pub_files([entry.name for entry in os.scandir(PUB_DIR) if entry.is_file()])

# Determine the number of files to process (minimum of CVAT and PUB file counts)
num_files_to_process = min(len(cvat_files), len(pub_files))

# Display the first 15 elements in the sorted lists
#print("First 15 elements in sorted cvat_files:", cvat_files[:15])
#print("First 15 elements in sorted pub_files:", pub_files[:15])

# Iterate through the selected number of files and rename them
for i in range(num_files_to_process):
    cvat_file = cvat_files[i]
    pub_file = pub_files[i]

    # Create new file name with the same extension as the PUB file
    pub_file_parts = pub_file.split('.')
    extension = pub_file_parts[-1]
    new_cvat_file_name = os.path.join(CVAT_DIR, pub_file_parts[0] + '.' + extension)

    # Rename the file
    cvat_file_path = os.path.join(CVAT_DIR, cvat_file)
    os.rename(cvat_file_path, new_cvat_file_name)

print("Script executed successfully!")
