#!/usr/bin/env python3

# SCRIPT 1/2 FOR PROCESSING CVAT

import os


def dirname_to_lowercase(dir):
    if os.path.isdir(dir):
        folder_name = os.path.basename(dir)
        new_folder_name = folder_name.lower()
        new_folder_path = os.path.join(os.path.dirname(dir), new_folder_name)
        os.rename(dir, new_folder_path)


def get_sorted_txt_files(dir):
    return sorted([entry.name for entry in os.scandir(dir) if entry.is_file() and entry.name.endswith('.txt')])


# Function to custom sort PUB files based on timestamp and frame number
def sort_by_timestamp_frame(file_list):
    return sorted(file_list, key=lambda x: (x.split('_frame_')[0], int(x.split('_frame_')[-1].split('.')[0])))


def rename_txt_files(cvat_dir_txt, pub_dir_txt):
    # Check if directories exist
    if not os.path.isdir(cvat_dir_txt): 
        print(f"Error: {cvat_dir_txt} not found.")
        return
    if not os.path.isdir(pub_dir_txt):
        print(f"Error: {pub_dir_txt} not found.")
        return

    # Get sorted lists of txt files for CVAT and PUB directory
    cvat_files = get_sorted_txt_files(cvat_dir_txt)
    pub_files = sort_by_timestamp_frame(get_sorted_txt_files(pub_dir_txt))

    # Validation count of frames 
    if len(cvat_files) != len(pub_files):
        print(f"Error: number of frames is not equal between directories (CVAT: {len(cvat_files)} vs PUB: {len(pub_files)})")
        return

    for i in range(len(cvat_files)):
        cvat_file = cvat_files[i]
        pub_file = pub_files[i]

        # Create new file name with the same extension as the PUB file
        pub_file_parts = pub_file.split('.')
        extension = pub_file_parts[-1]
        new_cvat_file_name = os.path.join(cvat_dir_txt, pub_file_parts[0] + '.' + extension)

        # Rename the file
        curr_cvat_file_path = os.path.join(cvat_dir_txt, cvat_file)
        os.rename(curr_cvat_file_path, new_cvat_file_name)

    print(f"Renamed files successfully for {os.path.dirname(cvat_dir_txt)}!")


def main():
    ranges = [1, 3, 4, 5]

    for i in ranges:
        # Set dirname based on cwd (default: root dir of prj)
        cvat_dir_txt = f"CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        if os.path.basename(os.getcwd()) == "process_cvat_files":
            cvat_dir_txt = f"../CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        dirname_to_lowercase(cvat_dir_txt)
        print(os.path.dirname(cvat_dir_txt))

        # cvat_dir_txt = f"../CVAT_dataset/CVATDataSet{i}/obj_train_data"
        # pub_dir_txt = f"../PSKUS_dataset_preprocessed/DataSet{i}_TXT"
        # rename_txt_files(cvat_dir_txt, pub_dir_txt)


main()