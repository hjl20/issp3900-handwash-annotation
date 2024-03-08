#!/usr/bin/env python3
import os

def rename_txt_files(cvat_dir, pub_dir_txt):
        # Check if directories exist
        if not os.path.isdir(cvat_dir) or not os.path.isdir(pub_dir_txt):
            print(f"Error: One or both of the directories ({cvat_dir} and {pub_dir_txt}) not found.")
            exit(1)

        # Function to get a list of txt files in a directory and sort them
        def get_sorted_txt_files(directory):
            txt_files = [entry.name for entry in os.scandir(directory) if entry.is_file() and entry.name.endswith('.txt')]
            return sorted(txt_files)

        # Function to custom sort PUB files based on timestamp and frame number
        def custom_sort_pub_files(file_list):
            return sorted(file_list, key=lambda x: (x.split('_frame_')[0], int(x.split('_frame_')[-1].split('.')[0])))

        # Get sorted lists of txt files for CVAT and all files (regardless of type) for PUB directory
        cvat_files = get_sorted_txt_files(cvat_dir)
        pub_files = custom_sort_pub_files([entry.name for entry in os.scandir(pub_dir_txt) if entry.is_file()])

        # Determine the number of files to process (minimum of CVAT and PUB file counts)
        num_files_to_process = min(len(cvat_files), len(pub_files))

        # Iterate through the selected number of files and rename them
        for i in range(num_files_to_process):
            cvat_file = cvat_files[i]
            pub_file = pub_files[i]

            # Create new file name with the same extension as the PUB file
            pub_file_parts = pub_file.split('.')
            extension = pub_file_parts[-1]
            new_cvat_file_name = os.path.join(cvat_dir, pub_file_parts[0] + '.' + extension)

            # Rename the file
            cvat_file_path = os.path.join(cvat_dir, cvat_file)
            os.rename(cvat_file_path, new_cvat_file_name)


def main():
    ranges = [1, 3, 4, 5]

    for i in ranges:
        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        pub_dir_txt = f"../PSKUS_dataset_preprocessed/DataSet{i}_TXT"
        rename_txt_files(cvat_dir, pub_dir_txt)
        print(f"Renamed files successfully for set {i}!")

main()