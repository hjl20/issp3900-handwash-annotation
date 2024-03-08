#!/usr/bin/env python3
import os

# Update CVAT train folder to lowercase
def dirname_to_lowercase(cvat_dir):
    print(os.path.join(cvat_dir))
    if os.path.join(cvat_dir):
        os.rename(os.path.join(cvat_dir), os.path.join(cvat_dir).lower())

# Function to read the single digit number from the pub directory
def read_single_digit_number(filepath):
    with open(filepath) as file:
        single_digit_number = int(file.readline().strip())
    # Change -1 to 0
    if single_digit_number == -1:
        single_digit_number = 0
    return single_digit_number

# Process files in pubset directory one by one
def process_pub_files(cvat_dir, pub_dir_txt):
    for pub_filename in os.listdir(pub_dir_txt):
        if pub_filename.endswith('.txt'):
            pub_filepath = os.path.join(pub_dir_txt, pub_filename)
            if os.path.isfile(pub_filepath):
                # Read single digit number from the pubset file
                single_digit_number = read_single_digit_number(pub_filepath)
                # Find matching file in cvat directory
                cvat_filename = os.path.splitext(os.path.splitext(pub_filename)[0])[0]
                cvat_filepath = os.path.join(cvat_dir, cvat_filename + '.txt')
                if os.path.isfile(cvat_filepath):
                    # Update data in the cvat file
                    update_cvat_file(cvat_filepath, single_digit_number)
                else:
                    print('file not found')

# Function to update data in the cvat file
def update_cvat_file(cvat_filepath, single_digit_number):
    updated_lines = []
    with open(cvat_filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 0 and float(parts[0]) == 0:
            parts[0] = str(single_digit_number)
            updated_lines.append(' '.join(parts) + '\n')
    with open(cvat_filepath, 'w') as file:
        file.writelines(updated_lines)


# Process files in pub directory and update corresponding cvat files
def main():
    ranges = [1, 3, 4, 5]
    for i in ranges:

        # Directory name validation check
        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        dirname_to_lowercase(cvat_dir)

        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_train_data"
        pub_dir_txt = f"../PSKUS_dataset_preprocessed/DataSet{i}_TXT"

        process_pub_files(cvat_dir, pub_dir_txt)
        print(f"Value changes successful for set {i}!")


main()