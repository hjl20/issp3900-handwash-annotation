''' 
Create a new folder called "Training_and_Validation_Data" in the same directory as the PSKUS_dataset_preprocessed and CVAT_dataset folders
Will have the following structure:
    Training_and_Validation_Data
        |-- IMG
        |-- TXT
        |-- VAL
            |-- IMG
            |-- TXT
'''

import os 
import shutil
import random



# create the training and validation directories
def create_training_dirs(txt_dest_dir, img_dest_dir):
    if not os.path.isdir(txt_dest_dir) or not os.path.isdir(img_dest_dir):
        # setting exist_ok to True to avoid FileExistsError
        os.makedirs(txt_dest_dir, exist_ok=True)
        os.makedirs(img_dest_dir, exist_ok=True)
        print("Training_and_Validation_Data directories created successfully!")
        return
    
    
# put all the CVAT txt files and PSKUS_dataset_preprocessed img files in the same directory
def move_data_to_dir(cvat_source_dir, cvat_dest_dir, pub_source_dir, pub_dest_dir):
    if not os.path.isdir(cvat_source_dir) or not os.path.isdir(pub_source_dir):
        print(f"Error: One or both of the directories ({cvat_source_dir} and {pub_source_dir}) not found.")
        return
    cvat_file_names = os.listdir(cvat_source_dir)
    pub_file_names = os.listdir(pub_source_dir)
    
    # create the directories
    create_training_dirs(cvat_dest_dir, pub_dest_dir)
    
    # move the files to the new directories
    for cvat_file in cvat_file_names:
        cvat_file_path = os.path.join(cvat_source_dir, cvat_file)
        shutil.move(cvat_file_path, cvat_dest_dir)
        # remove later 
        print(f"Moved {cvat_file} to {cvat_dest_dir}")
        # delete folder after all files gone
        if not os.listdir(cvat_source_dir):
            parent_cvat_dir = os.path.dirname(cvat_source_dir)
            # have to use shutil.rmtree to dir since obj_train is inside
            shutil.rmtree(parent_cvat_dir)
            print(f"Deleting {parent_cvat_dir}...")


    for pub_file in pub_file_names:
        pub_file_path = os.path.join(pub_source_dir, pub_file)
        shutil.move(pub_file_path, pub_dest_dir)
        # remove later
        print(f"Moved {pub_file} to {pub_dest_dir}")
        # delete folder after all files gone
        if not os.listdir(pub_source_dir):
            os.rmdir(pub_source_dir)
            print(f"Deleting {pub_source_dir}...")

        




def main():
    ranges = [1, 3, 4, 5]
    for i in ranges:
        cvat_source_dir = f"../CVAT_dataset/CVATDataSet{i}/obj_train_data"
        cvat_dest_dir = f"../Training_and_Validation_Data/TXT"
        pub_source_dir = f"../PSKUS_dataset_preprocessed/DataSet{i}_IMG"
        pub_dest_dir = f"../Training_and_Validation_Data/IMG"

        move_data_to_dir(cvat_source_dir, cvat_dest_dir, pub_source_dir, pub_dest_dir)
    print("Data directories created and moved successfully!")
    
    
main()