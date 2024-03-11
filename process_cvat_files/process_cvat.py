''' 
Create subfolders to sort frames into based on gesture value 
Will have the following structure:
    input_cvat_folder
        |-- 1    
        |-- 2
        |-- 3
        ..
        |-- 6
'''

# SCRIPT 2/2 FOR PROCESSING CVAT

import os
import shutil

# Paths in script are defined from prj root directory (i.e. issp3900-handwash-annotation folder)
# Change to your input folder paths if different
# Make sure they are BOTH in the same directory and at the prj root level
input_cvat_folder = './CVAT_dataset'
input_pub_folder = './PSKUS_dataset_preprocessed'

CVAT_SUBFOLDER_PREFIX = 'CVATDataSet'
PUB_SUBFOLDER_PREFIX = 'DataSet'
PUB_IMG_SUBFOLDER_SUFFIX = '_IMG'
PUB_TXT_SUBFOLDER_SUFFIX = '_TXT'


def get_gesture_val(file_path):
    with open(file_path) as file:
        gesture_val = int(file.readline().strip())
    # Set -1 vals to be 0 for non-washing
    if gesture_val == -1:
        gesture_val = 0
    return gesture_val


def update_cvat_file(cvat_txt_file_path, gesture_val):
    # Default: empty files are put in gesture 0 subfolder
    updated_lines = []
    gesture_subfolder = '0'

    with open(cvat_txt_file_path, 'r') as file:
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
    with open(cvat_txt_file_path, 'w') as file:
        file.writelines(updated_lines)

    return gesture_subfolder


def move_file_to_subfolder(file_path, subfolder_path):
    file_dest_path = os.path.join(subfolder_path, os.path.basename(file_path))
    shutil.move(file_path, file_dest_path)


def process_cvat_files(cvat_dir, pub_dir):
    cvat_txt_dir = os.path.join(cvat_dir, "obj_Train_data")
    pub_txt_dir = pub_dir + PUB_TXT_SUBFOLDER_SUFFIX
    pub_img_dir = pub_dir + PUB_IMG_SUBFOLDER_SUFFIX

    if not os.path.isdir(cvat_txt_dir): 
        print(f"Error: {cvat_txt_dir} not found.")
        return
    if not os.path.isdir(pub_txt_dir):
        print(f"Error: {pub_txt_dir} not found.")
        return
    if not os.path.isdir(pub_img_dir):
        print(f"Error: {pub_img_dir} not found.")
        return
    
    for pub_txt_file_name in os.listdir(pub_txt_dir):
        if not pub_txt_file_name.endswith('.txt'):
            print(f"{pub_txt_file_name} is not a txt. Continuing..")
            continue
        
        # Get img path to move with annotation later
        pub_img_file_path = os.path.join(pub_img_dir, os.path.splitext(pub_txt_file_name)[0] + '.jpg')
        pub_txt_file_path = os.path.join(pub_txt_dir, pub_txt_file_name)
        
        if not os.path.isfile(pub_txt_file_path):
            print(f"{pub_txt_file_path} not found. Continuing..")
            continue
        if not os.path.isfile(pub_img_file_path):
            print(f"{pub_img_file_path} not found. Continuing..")
            continue

        # Find matching file in cvat directory
        file_name, ext = os.path.splitext(pub_txt_file_name)
        cvat_txt_file_path = os.path.join(cvat_txt_dir, file_name + ext)
        
        if not os.path.isfile(cvat_txt_file_path):
            print(f'{cvat_txt_file_path} not found. Continuing..')

        gesture_val = str(get_gesture_val(pub_txt_file_path))
        # Get updated val to sort into subfolders. Gesture can change to 0 if label update is non-washing/empty file
        updated_gesture_val = update_cvat_file(cvat_txt_file_path, gesture_val)

        # Create subfolders to group same gesture files
        cvat_txt_dir_subpath = os.path.join(os.path.dirname(cvat_dir), updated_gesture_val)
        if not os.path.isdir(cvat_txt_dir_subpath):
            os.mkdir(cvat_txt_dir_subpath)

        # We will move it to a subfolder based on gesture val
        move_file_to_subfolder(cvat_txt_file_path, cvat_txt_dir_subpath)
        move_file_to_subfolder(pub_img_file_path, cvat_txt_dir_subpath)

    print(f"Modified gesture values successfully for {os.path.dirname(cvat_txt_dir)}!")


# Process files in pub directory and update corresponding cvat files
def main():
    # Enforce paths are based on prj root dir
    count = 0
    while not os.path.basename(input_cvat_folder) in os.listdir(os.getcwd()):
        os.chdir('..')
        count += 1
        if count > 5:
            print(f"Error: {os.path.basename(input_cvat_folder)} not found.")
            return
        
    # Get dataset #s and process
    cvat_subfolder_list = [d for d in os.listdir(input_cvat_folder) if os.path.isdir(os.path.join(input_cvat_folder, d))]
    set_numbers = [int(folder.removeprefix(CVAT_SUBFOLDER_PREFIX)) for folder in cvat_subfolder_list]
    for num in sorted(set_numbers):
        cvat_txt_dir = os.path.join(input_cvat_folder, CVAT_SUBFOLDER_PREFIX + str(num))
        pub_img_dir = os.path.join(input_pub_folder, PUB_SUBFOLDER_PREFIX + str(num))

        print(f"Modifying annotation set {num}..")
        process_cvat_files(cvat_txt_dir, pub_img_dir)
    
    # Delete unneeded folders from previous steps
    print("Cleaning up processed dataset folders..")
    for num in set_numbers:
        cvat_processed_dir = os.path.join(input_cvat_folder, CVAT_SUBFOLDER_PREFIX + str(num))
        if os.path.isdir(cvat_processed_dir):
            shutil.rmtree(cvat_processed_dir)
            
    cvat_discard_dir = os.path.join(input_cvat_folder, '0')
    if os.path.isdir(cvat_discard_dir):
        shutil.rmtree(cvat_discard_dir)
    if os.path.isdir(input_pub_folder):
        shutil.rmtree(input_pub_folder)
    print("Clean up completed!")


main()