#!/usr/bin/env python3
import os


def dirname_to_lowercase(cvat_dir):
    if os.path.isdir(cvat_dir):
        os.rename(os.path.join(cvat_dir), os.path.join(cvat_dir).lower())


def get_gesture_val(filepath):
    with open(filepath) as file:
        gesture_val = int(file.readline().strip())
    # Set -1 vals to be non-washing
    if gesture_val == -1:
        gesture_val = 0
    return gesture_val


def update_cvat_file(cvat_filepath, gesture_val):
    updated_lines = []
    with open(cvat_filepath, 'r') as file:
        lines = file.readlines()

    for line in lines:
        label_line = line.strip().split()
        # Only keep washing vals and convert to gesture val
        if len(label_line) > 0 and float(label_line[0]) == 0:
            label_line[0] = str(gesture_val)
            updated_lines.append(' '.join(label_line) + '\n')

    # Overwrite file with updated lines
    with open(cvat_filepath, 'w') as file:
        file.writelines(updated_lines)


def process_cvat_files(cvat_dir, pub_dir_txt):
    if not os.path.isdir(cvat_dir) or not os.path.isdir(pub_dir_txt):
        print(f"Error: One or both of the directories ({cvat_dir} and {pub_dir_txt}) not found.")
        return
    
    for pub_filename in os.listdir(pub_dir_txt):
        if not pub_filename.endswith('.txt'):
            print(f"{pub_filename} is not a txt. Continuing..")
            continue

        pub_filepath = os.path.join(pub_dir_txt, pub_filename)
        
        if not os.path.isfile(pub_filepath):
            print(f"{pub_filepath} does not exist. Continuing..")
            continue

        gesture_val = get_gesture_val(pub_filepath)

        # Find matching file in cvat directory
        cvat_filename = os.path.splitext(os.path.splitext(pub_filename)[0])[0]
        cvat_filepath = os.path.join(cvat_dir, cvat_filename + '.txt')

        if os.path.isfile(cvat_filepath):
            update_cvat_file(cvat_filepath, gesture_val)
        else:
            print(f'{cvat_filepath} not found.')
    print(f"Value changes successful for {cvat_dir}!")


# Process files in pub directory and update corresponding cvat files
def main():
    ranges = [1, 3, 4, 5]
    for i in ranges:

        # Directory name validation check
        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        dirname_to_lowercase(cvat_dir)

        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_train_data"
        pub_dir_txt = f"../PSKUS_dataset_preprocessed/DataSet{i}_TXT"

        process_cvat_files(cvat_dir, pub_dir_txt)


main()