#!/usr/bin/env python3

# SCRIPT 2/3 FOR PROCESSING CVAT

import os
import shutil

def get_gesture_val(filepath):
    with open(filepath) as file:
        gesture_val = int(file.readline().strip())
    # Set -1 vals to be 0 for non-washing
    if gesture_val == -1:
        gesture_val = 0
    return gesture_val


def update_cvat_file(cvat_file_path, gesture_val):
    updated_lines = []
    gesture_subfolder = '0'

    with open(cvat_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        label_line = line.strip().split()
        # Only keep washing vals and convert to gesture val
        if len(label_line) > 0 and float(label_line[0]) == 0:
            label_line[0] = str(gesture_val)
            gesture_subfolder = str(gesture_val)
            updated_lines.append(' '.join(label_line) + '\n')

    # Overwrite file with updated lines
    # Will be appropriate gesture val (is-washing), empty file (non-washing), or 0 (unknown gesture)
    with open(cvat_file_path, 'w') as file:
        file.writelines(updated_lines)

    return gesture_subfolder


def move_file_to_subfolder(file_path, subfolder_path):
    file_name = file_path.split('\\')[-1]
    file_dest_path = os.path.join(subfolder_path, file_name)
    shutil.move(file_path, file_dest_path)


def process_cvat_files(cvat_dir, pub_dir):
    pub_dir_txt = pub_dir + "_TXT"
    pub_dir_img = pub_dir + "_IMG"

    if not os.path.isdir(cvat_dir): 
        print(f"Error: directory {cvat_dir} not found.")
        return
    if not os.path.isdir(pub_dir_txt):
        print(f"Error: directory {pub_dir_txt} not found.")
        return
    if not os.path.isdir(pub_dir_img):
        print(f"Error: directory {pub_dir_img} not found.")
        return
    
    for pub_txt_file_name in os.listdir(pub_dir_txt):
        if not pub_txt_file_name.endswith('.txt'):
            print(f"{pub_txt_file_name} is not a txt. Continuing..")
            continue
        
        # Get img path to move with annotation later
        pub_img_file_name = pub_txt_file_name.split('.')[0] + '.jpg'

        pub_txt_file_path = os.path.join(pub_dir_txt, pub_txt_file_name)
        pub_img_file_path = os.path.join(pub_dir_img, pub_img_file_name)
        
        if not os.path.isfile(pub_txt_file_path):
            print(f"{pub_txt_file_path} does not exist. Continuing..")
            continue
        if not os.path.isfile(pub_img_file_path):
            print(f"{pub_img_file_path} does not exist. Continuing..")
            continue

        gesture_val = str(get_gesture_val(pub_txt_file_path))

        # Find matching file in cvat directory
        cvat_file_name = os.path.splitext(os.path.splitext(pub_txt_file_name)[0])[0]
        cvat_file_path = os.path.join(cvat_dir, cvat_file_name + '.txt')
        
        if os.path.isfile(cvat_file_path):
            updated_gesture_val = update_cvat_file(cvat_file_path, gesture_val)

            # Create subfolders to group same gesture files
            cvat_dir_subpath = cvat_dir.split('/')
            cvat_dir_subpath = os.path.join(cvat_dir_subpath[0], cvat_dir_subpath[1], updated_gesture_val)
            if not os.path.isdir(cvat_dir_subpath):
                os.mkdir(cvat_dir_subpath)

            # We will move it to a subfolder based on gesture val
            move_file_to_subfolder(cvat_file_path, cvat_dir_subpath)
            move_file_to_subfolder(pub_img_file_path, cvat_dir_subpath)
        else:
            print(f'file {cvat_file_path} not found. Continuing..')
    print(f"Value changes successful for {cvat_dir}!")


# Process files in pub directory and update corresponding cvat files
def main():
    ranges = [1, 3, 4, 5]

    for i in ranges:
        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_train_data"
        pub_dir = f"../PSKUS_dataset_preprocessed/DataSet{i}"

        process_cvat_files(cvat_dir, pub_dir)


main()