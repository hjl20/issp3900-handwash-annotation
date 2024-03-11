# SCRIPT 1/2 FOR PROCESSING CVAT

import os

# Paths in script are defined from prj root directory (i.e. issp3900-handwash-annotation folder)
# Change to your input folder paths if different
# Make sure they are BOTH in the same directory and at the prj root level
input_cvat_folder = './CVAT_dataset'
input_pub_folder = './PSKUS_dataset_preprocessed'

CVAT_SUBFOLDER_PREFIX = 'CVATDataSet'
PUB_SUBFOLDER_PREFIX = 'DataSet'
PUB_SUBFOLDER_SUFFIX = '_TXT'


def dirname_to_lowercase(dir):
    if os.path.isdir(dir):
        folder_name = os.path.basename(dir)
        new_folder_name = folder_name.lower()
        new_folder_path = os.path.join(os.path.dirname(dir), new_folder_name)
        os.rename(dir, new_folder_path)
        return new_folder_path
    else:
        return dir


def get_sorted_txt_files(dir):
    return sorted([entry.name for entry in os.scandir(dir) if entry.is_file() and entry.name.endswith('.txt')])


# Function to custom sort PUB files based on timestamp and frame number
def sort_by_timestamp_frame(file_list):
    return sorted(file_list, key=lambda x: (x.split('_frame_')[0], int(x.split('_frame_')[-1].split('.')[0])))


def rename_annotation_files(cvat_txt_dir, pub_txt_dir):
    if not os.path.isdir(cvat_txt_dir): 
        print(f"Error: {cvat_txt_dir} not found.")
        return
    if not os.path.isdir(pub_txt_dir):
        print(f"Error: {pub_txt_dir} not found.")
        return

    # Sort to enforce proper ordering of frames
    cvat_files = get_sorted_txt_files(cvat_txt_dir)
    pub_files = sort_by_timestamp_frame(get_sorted_txt_files(pub_txt_dir))

    # Validation count of frames 
    if len(cvat_files) != len(pub_files):
        print(f"Error: number of frames is not equal between directories (CVAT: {len(cvat_files)} vs PUB: {len(pub_files)})")
        return

    for i in range(len(cvat_files)):
        cvat_file = cvat_files[i]
        pub_file = pub_files[i]

        # Create new file name with the same extension as the PUB file
        file_name, ext = os.path.splitext(pub_file)
        new_cvat_file_name = os.path.join(cvat_txt_dir, file_name + ext)

        # Rename the file
        curr_cvat_file_path = os.path.join(cvat_txt_dir, cvat_file)
        os.rename(curr_cvat_file_path, new_cvat_file_name)

    print(f"Renamed files successfully for {os.path.dirname(cvat_txt_dir)}!")


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
        cvat_txt_dir = os.path.join(input_cvat_folder, CVAT_SUBFOLDER_PREFIX + str(num), "obj_Train_data")
        pub_txt_dir = os.path.join(input_pub_folder, PUB_SUBFOLDER_PREFIX + str(num) + PUB_SUBFOLDER_SUFFIX)

        # Context: folders vary from obj_Train_data and obj_train_data, so lower to prevent errors 
        cvat_txt_dir = dirname_to_lowercase(cvat_txt_dir)
        
        print(f"Renaming set {num}..")
        rename_annotation_files(cvat_txt_dir, pub_txt_dir)


main()