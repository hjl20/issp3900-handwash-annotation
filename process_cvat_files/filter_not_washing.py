#!/usr/bin/env python3

# SCRIPT 3/3 FOR PROCESSING CVAT

import os


def filter_not_washing(cvat_dir, pub_dir_img):
    if not os.path.isdir(cvat_dir) or not os.path.isdir(pub_dir_img):
        print(f"Error: One or both of the directories ({cvat_dir} and {pub_dir_img}) not found.")
        return
    
    # Step 1: Check txt file in the data_txt folder
    for txt_file in os.listdir(cvat_dir):
        if not txt_file.endswith(".txt"):
            return 
        
        txt_file_path = os.path.join(cvat_dir, txt_file)
        
        with open(txt_file_path, 'r') as file:
            # Files should only have 1 line after being processed with process_cvat.py
            first_line = file.readline().strip()
            
            # Step 2: Check if not a valid gesture value (i.e. unknown gesture or non-washing)
            if not first_line or first_line.startswith('0') or float(first_line.split()[0]) < 0:
                # Step 3: Remove the file from data_txt and data_jpg directories
                jpg_file = os.path.splitext(txt_file)[0] + ".jpg"
                jpg_file_path = os.path.join(pub_dir_img, jpg_file)
                
                os.remove(txt_file_path)
                os.remove(jpg_file_path)

    print(f"Filtering complete for set {cvat_dir}!")          
    

def main():
    ranges = [1, 3, 4, 5]
    for i in ranges:
        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        pub_dir_img = f"../PSKUS_dataset_preprocessed/DataSet{i}_IMG"
        filter_not_washing(cvat_dir, pub_dir_img)


main()
