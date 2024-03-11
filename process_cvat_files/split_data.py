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

# Paths in script are defined from prj root directory (i.e. issp3900-handwash-annotation folder)
# Change to your input folder paths if different
# Make sure they are BOTH in the same directory and at the prj root level
input_cvat_folder = './CVAT_dataset'
output_folder = './Training_and_Validation_Data'

OUTPUT_TRAIN_FOLDER = 'TRAIN'
OUTPUT_VAL_FOLDER = 'VAL'
OUTPUT_IMG_SUBFOLDER = 'IMG'
OUTPUT_TXT_SUBFOLDER = 'TXT'


# create the training and validation directories
def create_train_split_folders(output_folder):
    subfolders = [OUTPUT_TRAIN_FOLDER, OUTPUT_VAL_FOLDER]
    subsubfolders = [OUTPUT_IMG_SUBFOLDER, OUTPUT_TXT_SUBFOLDER]

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    for subfolder in subfolders:
        if not os.path.isdir(os.path.join(output_folder, subfolder)):
            os.mkdir(os.path.join(output_folder, subfolder))

        for subsubfolder in subsubfolders:
            if not os.path.isdir(os.path.join(output_folder, subfolder, subsubfolder)):
                os.mkdir(os.path.join(output_folder, subfolder, subsubfolder))
    

def create_val_data(source_dir, dest_dir):
    cvat_file_names = os.listdir(source_dir)
    random.shuffle(cvat_file_names)
    
    # # look for all the txt files in the directory
    # txt_file = [file for file in cvat_file_names if file.endswith('.txt')]
    # val_percent = int(len(cvat_file_names)*0.2)
    

    # for cvat_file in txt_file[:val_percent]:
    #     # txt file path
    #     cvat_file_path = os.path.join(source_dir, cvat_file)
    #     # find corresponding image file
    #     file_name = os.path.splitext(cvat_file)[0]
    #     img_file = file_name + ".jpg"
        
    #     if img_file in cvat_file_names:
    #         img_file_path = os.path.join(source_dir, img_file)
            
    #         # move txt file to val directory
    #         shutil.move(cvat_file_path, txt_dest_dir)
    #         # print statements for testing
    #         # print(f"Moved {cvat_file} to {txt_dest_dir}")

    #         # move img file to val directory
    #         shutil.move(img_file_path, img_dest_dir)
    #         # print(f"Moved {img_file} to {img_dest_dir}")

    # print(f"Validation data created successfully!")


# put all the CVAT txt and img files their corresponding directories
def move_data_to_dir(txt_source_dir, txt_dest_dir, img_dest_dir):
    if not os.path.isdir(txt_source_dir):
        print(f"Error: The directory ({txt_source_dir} not found.")
        return
    
    print(f"Moving data from {txt_source_dir} to {txt_dest_dir} and {img_dest_dir}...")
    
    # get the file names in the corresponding directories
    cvat_file_names = os.listdir(txt_source_dir)
    
    # create the directories if they don't exist
    create_train_split_folders(txt_dest_dir, img_dest_dir)

    '''
    Note: If there are any duplicate files, shutil will throw an error, will need to add a try and except block to handle this
    '''
    # move the files to the new directories
    for cvat_file in cvat_file_names:
        if cvat_file.endswith('.txt'):
            cvat_txt_file_path = os.path.join(txt_source_dir, cvat_file)
            shutil.move(cvat_txt_file_path, txt_dest_dir)
            # print for testing 
            # print(f"Moved {cvat_file} to {txt_dest_dir}")
            
        if cvat_file.endswith('.jpg'):
            cvat_img_file_path = os.path.join(txt_source_dir, cvat_file)
            shutil.move(cvat_img_file_path, img_dest_dir)
            # print for testing
            # print(f"Moved {cvat_file} to {img_dest_dir}")
        
        # delete folder after all files gone
        if not os.listdir(txt_source_dir):
            os.rmdir(txt_source_dir)
            print(f"Deleting {txt_source_dir}...")

        
    print(f"Data successfully moved to {txt_dest_dir} and {img_dest_dir}")


def main():
    # Enforce paths are based on prj root dir
    while not os.path.basename(input_cvat_folder) in os.listdir(os.getcwd()):
        os.chdir('..')
    
    create_train_split_folders(output_folder)

    # Get dataset #s and process
    cvat_subfolder_list = [d for d in os.listdir(input_cvat_folder) if os.path.isdir(os.path.join(input_cvat_folder, d))]

    for num in sorted(cvat_subfolder_list):
        cvat_source_dir = os.path.join(input_cvat_folder, str(num))
        print(f"Creating validation data for {cvat_source_dir}..")
        create_val_data(cvat_source_dir, output_folder)
        
    # for i in ranges:
    #     cvat_source_dir = f"../CVAT_dataset/{i}"
    #     cvat_txt_dest_dir = f"../Training_and_Validation_Data/TRAIN/TXT" 
    #     cvat_img_dest_dir = f"../Training_and_Validation_Data/TRAIN/IMG"
    #     move_data_to_dir(cvat_source_dir, cvat_txt_dest_dir, cvat_img_dest_dir)
    
main()