#!/usr/bin/env python3

# SCRIPT 1/3 FOR PROCESSING CVAT

import os

def dirname_to_lowercase(cvat_dir):
    if os.path.isdir(cvat_dir):
        # Get the current folder name
        folder_name = os.path.basename(cvat_dir)

        # Create the new lowercase folder name
        new_folder_name = folder_name.lower()

        # Construct the new folder path
        new_folder_path = os.path.join(os.path.dirname(cvat_dir), new_folder_name)

        # Rename the folder
        os.rename(cvat_dir, new_folder_path)

def get_sorted_files(directory, ext=None):
    if ext:
        files = [entry.name for entry in os.scandir(directory) if entry.is_file() and entry.name.endswith(ext)]
    else:
        files = [entry.name for entry in os.scandir(directory) if entry.is_file()]
    return sorted(files)


# Function to custom sort PUB files based on timestamp and frame number
def sort_by_frame_timestamp(pub_file_list):
    return sorted(pub_file_list, key=lambda x: (x.split('_frame_')[0], int(x.split('_frame_')[-1].split('.')[0])))


def rename_txt_files(cvat_dir, pub_dir_txt):
    # Check if directories exist
    if not os.path.isdir(cvat_dir) or not os.path.isdir(pub_dir_txt):
        print(f"Error: One or both of the directories ({cvat_dir} and {pub_dir_txt}) not found.")
        return

    # Get sorted lists of txt files for CVAT and PUB directory
    cvat_files = get_sorted_files(cvat_dir, '.txt')
    pub_files = sort_by_frame_timestamp(get_sorted_files(pub_dir_txt, '.txt'))

    # Iterate as many files as are in both sets
    for i in range(min(len(cvat_files), len(pub_files))):
        cvat_file = cvat_files[i]
        pub_file = pub_files[i]

        # Create new file name with the same extension as the PUB file
        pub_file_parts = pub_file.split('.')
        extension = pub_file_parts[-1]
        new_cvat_file_name = os.path.join(cvat_dir, pub_file_parts[0] + '.' + extension)

        # Rename the file
        curr_cvat_file_path = os.path.join(cvat_dir, cvat_file)
        os.rename(curr_cvat_file_path, new_cvat_file_name)

    print(f"Renamed files successfully for set {cvat_dir}!")


def main():
    ranges = [1, 3, 4, 5]

    for i in ranges:
        # Directory name validation check
        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        dirname_to_lowercase(cvat_dir)

        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_train_data"
        pub_dir_txt = f"../PSKUS_dataset_preprocessed/DataSet{i}_TXT"
        rename_txt_files(cvat_dir, pub_dir_txt)


main()