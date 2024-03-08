#!/usr/bin/env python3
import os

def filter_not_washing(cvat_dir, pub_dir_img):
        # Step 1: Check every single txt file in the data_txt folder
        if cvat_dir is None or pub_dir_img is None:
            print(f"{cvat_dir} or {pub_dir_img} folder not found. Exiting..")
            return

        for txt_file in os.listdir(cvat_dir):
            if not txt_file.endswith(".txt"):
                return 
            txt_file_path = os.path.join(cvat_dir, txt_file)
            
            # Step 2: Check if the file meets the specified criteria
            with open(txt_file_path, 'r') as file:
                first_line = file.readline().strip()
                
                if not first_line or first_line.startswith('0') or float(first_line.split()[0]) < 0:
                    # Step 3: Remove the file from data_txt and data_jpg directories
                    jpg_file = os.path.splitext(txt_file)[0] + ".jpg"
                    jpg_file_path = os.path.join(pub_dir_img, jpg_file)
                    
                    os.remove(txt_file_path)
                    os.remove(jpg_file_path)
                    

def main():
    ranges = [1, 3, 4, 5]

    for i in ranges:
        cvat_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_Train_data"
        pub_dir_img = f"../PSKUS_dataset_preprocessed/DataSet{i}_IMG"
        filter_not_washing(cvat_dir, pub_dir_img)
        print(f"Filtering non-washing successful for set {i}!")


main()
