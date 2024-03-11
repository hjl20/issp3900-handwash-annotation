﻿# issp3900-handwash-annotation
This repo contains scripts to split PSKUS videos into frames and save the frame's gesture value with the image.

#### IMPORTANT: Bash scripts are likely to throw errors because of Windows line endings being different from Linux.

## Part 1a. How to use w/ bash script
Comment in/out the datasets you want to download, unzip, and process. We will be using datasets 1, 3, 4, and 5.
1. Install the dependencies by running ```pip install -r requirements.txt```.
2. Run ```sed -i -e 's/\r$//' <scriptname>``` in terminal. Replace <scriptname> with the scripts in this repo. This would include ```separate-frames.py```, ```rename_txt_files.py```, ```process_cvat.py```, and ```split_data.py```.
3. Run ```./get-and-preprocess-dataset.sh``` in terminal and the rest will be done for you.

## Part 1b. How to use w/o bash script
1. Install the dependencies by running ```pip install -r requirements.txt```.
2. Download PSKUS datasets and extract them into a folder called PSKUS_dataset in the same directory as the scripts and README.
3. With the extracted datasets in the folder (eg. ./PSKUS_dataset/DataSet4), run ```python separate-frames.py``` to process the videos.

## Part 2. Modifying frame annotation values
4. Create a directory called 'CVAT_dataset' in the main directory of the project (i.e. next to PSKUS_dataset and PSKUS_dataset_preprocessed)
5. Download and extract your CVAT datasets into their own folders within CVAT_dataset.
6. Rename each folder to this format: 'CVATDataSet#' (eg. CVATDataSet1).
7. Go in the process_cvat_files directory where you will find two scripts: rename_txt_files.py and process_cvat.py
#### NOTE: To ensure the scripts work, please make sure the CVAT and pub datasets have equal number of img/txt files after separate-frames.py before further processing.
#### IMPORTANT: The scripts in step5 need to be executed in the correct sequence. Follow the steps below
8. Run ```python rename_txt_files.py```
9. Run ```python process_cvat.py```

## Part 3. Splitting dataset into training and validation data
10. Run ```split_data.py```


## Final Output / Desired Data
The processed images and annotations used for training the machine learning model will be stored within the following folders (# being the number of the set processed) 
1. ./Training_and_Validation_Data/TRAIN (annotations and images in subfolders) 
2. ./Training_and_Validation_Data/VAL (annotations and images in subfolders) 


## Credits and References
Scripts are based from
https://github.com/edi-riga/handwash/tree/master

Used to run on PSKUS datasets to split videos into frames and pairing with their gesture value
https://zenodo.org/record/4537209

