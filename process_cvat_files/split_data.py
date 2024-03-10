''' 
Create a new folder called "Training_and_Validation_Data" in the same directory as the PSKUS_dataset_preprocessed and CVAT_dataset folders
Will have the following structure:
    Training_and_Validation_Data
        |-- TRAIN    
            |-- IMG
            |-- TXT
        |-- VAL
            |-- IMG
            |-- TXT
'''

import os 
import shutil
import random
import math


# create the training and validation directories
def create_dirs(txt_dest_dir, img_dest_dir):
    if not os.path.isdir(txt_dest_dir) or not os.path.isdir(img_dest_dir):
        os.makedirs(txt_dest_dir, exist_ok=False)
        os.makedirs(img_dest_dir, exist_ok=False)
        print(f"{txt_dest_dir} and {img_dest_dir} created successfully")
        return
    
    
# put all the CVAT txt files and PSKUS_dataset_preprocessed img files in the same directory
def move_data_to_dir(txt_source_dir, txt_dest_dir, img_source_dir, img_dest_dir):
    if not os.path.isdir(txt_source_dir) or not os.path.isdir(img_source_dir):
        print(f"Error: One or both of the directories ({txt_source_dir} and {img_source_dir}) not found.")
        return
    print(f"Moving data from {txt_source_dir} and {img_source_dir} to {txt_dest_dir} and {img_dest_dir}...")
    # get the file names in the corresponding directories
    cvat_file_names = os.listdir(txt_source_dir)
    pub_file_names = os.listdir(img_source_dir)
    
    # create the directories if they don't exist
    create_dirs(txt_dest_dir, img_dest_dir)
    
    # move the files to the new directories
    for cvat_file in cvat_file_names:
        cvat_file_path = os.path.join(txt_source_dir, cvat_file)
        shutil.move(cvat_file_path, txt_dest_dir)
        # remove later 
        # print(f"Moved {cvat_file} to {txt_dest_dir}")
        
        # delete folder after all files gone
        if not os.listdir(txt_source_dir):
            parent_cvat_dir = os.path.dirname(txt_source_dir)
            # have to use shutil.rmtree to remove dir since obj_train is inside
            shutil.rmtree(parent_cvat_dir)
            print(f"Deleting {parent_cvat_dir}...")

    for pub_file in pub_file_names:
        pub_file_path = os.path.join(img_source_dir, pub_file)
        shutil.move(pub_file_path, img_dest_dir)
        # remove later
        # print(f"Moved {pub_file} to {img_dest_dir}")
        
        # delete folder after all files gone
        if not os.listdir(img_source_dir):
            os.rmdir(img_source_dir)
            print(f"Deleting {img_source_dir}...")
        
    print(f"Data successfully moved to {txt_dest_dir} and {img_dest_dir}")

        

def create_val_data(txt_source_dir, txt_dest_dir, img_source_dir, img_dest_dir):
    create_dirs(txt_dest_dir, img_dest_dir)
    cvat_file_names = os.listdir(txt_source_dir)
    pub_file_names = os.listdir(img_source_dir)
    random.shuffle(cvat_file_names)
    
    val_percent = int(math.ceil(len(cvat_file_names)*0.2))
    
    for cvat_file in cvat_file_names[:val_percent]:
        cvat_file_path = os.path.join(txt_source_dir, cvat_file)
        shutil.move(cvat_file_path, txt_dest_dir)
        # remove later
        print(f"Moved {cvat_file} to {txt_dest_dir}")

        # split the file name to get the corresponding img
        file_name = os.path.splitext(cvat_file)[0]
        #print(file_name)
        pub_file = file_name + ".jpg"
        if pub_file in pub_file_names:
            pub_file_path = os.path.join(img_source_dir, pub_file)
            shutil.move(pub_file_path, img_dest_dir)
            print(f"Moved {pub_file} to {img_dest_dir}")

    print(f"Validation data created successfully!")


def main():
    ranges = [1, 3, 4, 5]
    for i in ranges:
        cvat_source_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_train_data"
        cvat_dest_dir = f"../Training_and_Validation_Data/TRAIN/TXT"
        pub_source_dir = f"../PSKUS_dataset_preprocessed/DataSet{i}_IMG"
        pub_dest_dir = f"../Training_and_Validation_Data/TRAIN/IMG"
        val_img_dest_dir = f"../Training_and_Validation_Data/VAL/IMG"
        val_txt_dest_dir = f"../Training_and_Validation_Data/VAL/TXT"


        move_data_to_dir(cvat_source_dir, cvat_dest_dir, pub_source_dir, pub_dest_dir)
    
    print(f"Creating validation data...")
    create_val_data(cvat_dest_dir, val_txt_dest_dir, pub_dest_dir, val_img_dest_dir)

    
    
main()