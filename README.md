# issp3900-handwash-annotation
This repo contains scripts to split PSKUS videos into frames.
Within the ```process_cvat_files folder``` contains scripts to save the frame's gesture value and split the frame images and labels into training and validation sets.

#### IMPORTANT NOTES: 
- Make copies of your datasets in case of irreversible changes from the scripts.
- Make sure to run the scripts in the order of instructions listed below
- Make sure the CVAT and pub datasets have equal number of img/txt files after Part 2. ```separate_frames.py``` before further processing.
- Bash scripts are likely to throw errors because of Windows line endings being different from Linux.


## Quick Start Instructions (work in project root directory)
1. Download PSKUS and CVAT 1, 3, 4, & 5 datasets
2. Extract to ```./PSKUS_dataset/DataSet#``` and ```./CVAT_dataset/CVATDataSet#```
3. Run ```python separate_frames.py```
4. Run ```python process_cvat_files/rename_txt_files.py```
5. Run ```python process_cvat_files/process_cvat.py```
6. Run ```python process_cvat_files/split_data.py```


## Part 1. Dependencies
1. Install with ```pip install -r requirements.txt```

## Part 2. Separating Frames 
### a. Using get_and_preprocess_dataset.sh 
Comment in/out the datasets you want to download, unzip, and process. We will be using datasets 1, 3, 4, and 5.
1. Run ```sed -i -e 's/\r$//' <scriptname>``` in terminal to change line endings to Unix format. Replace <scriptname> with the following while in their folder:
- ```get_and_preprocess_dataset.sh```
- ```separate_frames.py```
- ```rename_txt_files.py```
- ```process_cvat.py```
- ```split_data.py```
2. Run ```./get_and_preprocess_dataset.sh``` in terminal and the rest will be done for you.

### b. Without using bash
1. Create a directory called ```PSKUS_dataset``` in the project root directory (i.e. ```issp3900-handwash-annotation```).
2. Download PSKUS datasets 1, 3, 4, and 5 and extract them into ```./PSKUS_dataset```
3. Rename each folder to this format: ``DataSet4#`` (eg. ```./PSKUS_dataset/DataSet4```).
4. Run ```python separate_frames.py``` to process all of the extracted datasets (eg. ```./PSKUS_dataset/DataSet4```).

## Part 3. Modifying frame annotation values
1. Create a directory called ```CVAT_dataset``` in the project root directory (i.e. ```issp3900-handwash-annotation```).
2. Download CVAT datasets 1, 3, 4, and 5 and extract them into ```./CVAT_dataset```.
3. Rename each folder to this format: ``CVATDataSet#`` (eg. ```./CVAT_dataset/CVATDataSet4```).
4. Run ```python rename_txt_files.py``` or ```python process_cvat_files/rename_txt_files.py``` while in the project root directory.
5. Run ```python process_cvat.py``` or ```python process_cvat_files/process_cvat.py``` while in the project root directory.

## Part 4. Splitting dataset into training and validation data
1. Run ```split_data.py``` or ```python process_cvat_files/split_data.py``` while in the project root directory.


## Final Output / Desired Data
The processed images and annotations used for training the machine learning model will be stored within the following folders (# being the number of the set processed) 
- ```./train_val_dataset/train``` (annotations and images in subfolders) 
- ```./train_val_dataset/val``` (annotations and images in subfolders) 


## Credits and References
Scripts are based from
https://github.com/edi-riga/handwash/tree/master

Used to run on PSKUS datasets to split videos into frames and pairing with their gesture value
https://zenodo.org/record/4537209

