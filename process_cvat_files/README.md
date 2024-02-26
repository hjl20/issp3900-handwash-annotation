# Please read this file before running the scripts

## This folder contains the following files
1. check_gestures.py
2. rename_files.py
3. process_cvat.py

## IMPORTANT NOTES
1. These files are ran in Linux environment
2. Make sure you have ran herman's script get-and-preprocess-dataset.sh
3. If step 2 was successful, you should have a folder that has 'DataSet1' and inside that folder is a bunch of jpg and text files
4. **Note that this script only processes one video**. This script still needs to be modified so that it can run multiple dataset.
5. If you want to try to run this script yourself, make sure you follow the file structure below. If not, make sure you edit the scripts that will point to your directories
6. Run the files in the order mentioned in the Instructions


### Recommended File structure
PSKUS_dataset Folder
- DataSet1
- Videos 
    - ** should only contain 1 video**
    - you dont have to delete your videos, just change the name of the current folder and make a separate folder that contains only 1 video for processing

*After running get-and-preprocess-dataset.sh

PSKUS_dataset_preprocessed
- DataSet1
    - bunch of jpg and txt files
- Cvat 'obj_train_data'
    - this folder is included when you export the annotations from cvat. it should be called obj_train_data
    - this folder contains png and txt files. you don't have to modify this folder in any way. but you can remove the png files if you want. DO NOT REMOVE THE TXT FILES.
- check_gestures.py
- rename_files.py
- process_cvat.py


### (OPTIONAL) Run check_gestures.py
This file will create a csv file that shows you the pubset frames being renamed (which matches with cvat filename format) and the gesture value inside.
Please note that the pubset files are not being revised in any way when you run this script. This is only a sanity check to see the gesture value and filenames.

### Run rename_files.py
This file will rename the pubset frames to the same format as the cvat txt files

### Run process_cvat_files.py
The cvat txt files have bounding boxes classes and coordinates inside. What this script will do is find the classes '0' (washing) and replace it with the gesture number found inside the pubset txt files. The python file itself has some comments if you want to know how the script operates.