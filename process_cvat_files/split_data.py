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
def move_data_to_dir(txt_source_dir, txt_dest_dir, img_dest_dir):
    if not os.path.isdir(txt_source_dir):
        print(f"Error: The directory ({txt_source_dir} not found.")
        return
    print(f"Moving data from {txt_source_dir} to {txt_dest_dir} and {img_dest_dir}...")
    # get the file names in the corresponding directories
    cvat_file_names = os.listdir(txt_source_dir)

    
    # create the directories if they don't exist
    create_dirs(txt_dest_dir, img_dest_dir)


    # move the files to the new directories
    '''
    Note: If there are any duplicate files, shutil will throw an error, will need to add a try and except block to handle this
    '''
    for cvat_file in cvat_file_names:
        if cvat_file.endswith('.txt'):
            cvat_txt_file_path = os.path.join(txt_source_dir, cvat_file)
            shutil.move(cvat_txt_file_path, txt_dest_dir)
            # remove later 
            print(f"Moved {cvat_file} to {txt_dest_dir}")
            
        if cvat_file.endswith('.jpg'):
            cvat_img_file_path = os.path.join(txt_source_dir, cvat_file)
            shutil.move(cvat_img_file_path, img_dest_dir)
            # remove later
            print(f"Moved {cvat_file} to {img_dest_dir}")
        
        # delete folder after all files gone
        if not os.listdir(txt_source_dir):
            os.rmdir(txt_source_dir)
            print(f"Deleting {txt_source_dir}...")

        
    print(f"Data successfully moved to {txt_dest_dir} and {img_dest_dir}")

        

def create_val_data(source_dir, txt_dest_dir, img_dest_dir):
    create_dirs(txt_dest_dir, img_dest_dir)
    cvat_file_names = os.listdir(source_dir)
    random.shuffle(cvat_file_names)
    
    # look for all the txt files in the directory
    txt_file = [file for file in cvat_file_names if file.endswith('.txt')]
    val_percent = int(len(cvat_file_names)*0.2)
    
    # getting randomly 20% of data in directory
    for cvat_file in txt_file[:val_percent]:

        cvat_file_path = os.path.join(source_dir, cvat_file)

        # find corresponding image file
        file_name = os.path.splitext(cvat_file)[0]
        #print(file_name)
        img_file = file_name + ".jpg"
        if img_file in cvat_file_names:
            img_file_path = os.path.join(source_dir, img_file)
            
            # move txt file to val directory
            shutil.move(cvat_file_path, txt_dest_dir)
            # can remove print statements
            print(f"Moved {cvat_file} to {txt_dest_dir}")

            # move img file to val directory
            shutil.move(img_file_path, img_dest_dir)
            print(f"Moved {img_file} to {img_dest_dir}")

    print(f"Validation data created successfully!")


def main():
    ranges = range(1, 8)
    for i in ranges:
        cvat_source_dir = f"../CVAT_dataset/{i}"
        val_img_dest_dir = f"../Training_and_Validation_Data/VAL/IMG"
        val_txt_dest_dir = f"../Training_and_Validation_Data/VAL/TXT" 
        cvat_txt_dest_dir = f"../Training_and_Validation_Data/TRAIN/TXT" 
        cvat_img_dest_dir = f"../Training_and_Validation_Data/TRAIN/IMG"

        print(f"Creating validation data for {cvat_source_dir}...")
        create_val_data(cvat_source_dir, val_txt_dest_dir, val_img_dest_dir)
        
    for i in ranges:
        cvat_source_dir = f"../CVAT_dataset/{i}"
        cvat_txt_dest_dir = f"../Training_and_Validation_Data/TRAIN/TXT" 
        cvat_img_dest_dir = f"../Training_and_Validation_Data/TRAIN/IMG"
        move_data_to_dir(cvat_source_dir, cvat_txt_dest_dir, cvat_img_dest_dir)

    
    
main()