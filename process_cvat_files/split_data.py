''' 
Create a new folder called "train_val_dataset" in the same directory as the PSKUS_dataset_preprocessed and CVAT_dataset folders
Will have the following structure:
    train_val_dataset
        |-- train    
            |-- images
            |-- labels
        |-- val
            |-- images
            |-- labels
'''

import os 
import shutil
import random
from alive_progress import alive_bar

# Paths in script are defined from prj root directory (i.e. issp3900-handwash-annotation folder)
# Change to your input folder paths if different
# Make sure they are BOTH in the same directory and at the prj root level
input_cvat_folder = './CVAT_dataset'
output_folder = './train_val_dataset'

OUTPUT_TRAIN_FOLDER = 'train'
OUTPUT_VAL_FOLDER = 'val'
OUTPUT_IMG_SUBFOLDER = 'images'
OUTPUT_TXT_SUBFOLDER = 'labels'
VAL_SPLIT_RATIO = 0.2


# Create the training and validation directories
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
    

def move_frame_pairs(pair, src_dir, dest_dir):
        txt_src_path = os.path.join(src_dir, pair[0])
        img_src_path = os.path.join(src_dir, pair[1])
        txt_dest_path = os.path.join(dest_dir, OUTPUT_TXT_SUBFOLDER, pair[0])
        img_dest_path = os.path.join(dest_dir, OUTPUT_IMG_SUBFOLDER, pair[1])

        shutil.move(txt_src_path, txt_dest_path)
        shutil.move(img_src_path, img_dest_path)


def split_to_train_val(src_dir, dest_dir):
    '''
    Note: If there are any duplicate files, shutil will throw an error.
            TODO: add a try and except block to handle this
    '''
    dest_val_dir = os.path.join(dest_dir, OUTPUT_VAL_FOLDER)
    dest_train_dir = os.path.join(dest_dir, OUTPUT_TRAIN_FOLDER)
    
    cvat_file_names = os.listdir(src_dir)
    
    # Only get % of frame pairs (dir has both img and txt of frame, so only get % of one type eg. txt)
    txt_files = [os.path.splitext(file)[0] for file in cvat_file_names]
    frame_pairs = [(frame_name + '.txt', frame_name + '.jpg') for frame_name in set(txt_files)]
    val_percent = int(len(frame_pairs) * VAL_SPLIT_RATIO)

    # Random sample for validation set
    random.shuffle(frame_pairs)

    # Move sampled pairs into val folders
    with alive_bar(len(frame_pairs[:val_percent]), title="Validation Set") as bar:
        for pair in frame_pairs[:val_percent]:
            if not pair[0] in cvat_file_names:
                print(f'{pair[0]} not found. Continuing..')
                continue
            if not pair[1] in cvat_file_names:
                print(f'{pair[1]} not found. Continuing..')
                continue

            move_frame_pairs(pair, src_dir, dest_val_dir)

            # Remove to updated pair list to move later
            frame_pairs.remove(pair)
            bar()

    # Move remaining pairs into train folders
    with alive_bar(len(frame_pairs), title="Training   Set") as bar:
        for pair in frame_pairs:
            if not pair[0] in cvat_file_names:
                print(f'{pair[0]} not found. Continuing..')
                continue
            if not pair[1] in cvat_file_names:
                print(f'{pair[1]} not found. Continuing..')
                continue

            move_frame_pairs(pair, src_dir, dest_train_dir)
            bar()

    print(f"Train/Val split successfully for {src_dir}!")


def main():
    # Enforce paths are based on prj root dir
    count = 0
    while not os.path.basename(input_cvat_folder) in os.listdir(os.getcwd()):
        os.chdir('..')
        count += 1
        if count > 5:
            print(f"Error: {os.path.basename(input_cvat_folder)} not found.")
            return
    
    create_train_split_folders(output_folder)

    # Get dataset #s and process
    cvat_subfolder_list = [d for d in os.listdir(input_cvat_folder) if os.path.isdir(os.path.join(input_cvat_folder, d))]
    for num in sorted(cvat_subfolder_list):
        cvat_src_dir = os.path.join(input_cvat_folder, str(num))

        print(f"Splitting set {num}..")
        split_to_train_val(cvat_src_dir, output_folder)
    
    # Delete unneeded folders from previous steps
    print("Cleaning up processed dataset folders..")
    if os.path.isdir(input_cvat_folder):
        shutil.rmtree(input_cvat_folder)
    print("Clean up completed!")


main()