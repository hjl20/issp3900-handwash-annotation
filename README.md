# issp3900-handwash-annotation
This repo contains scripts to split PSKUS videos into frames and save the frame's gesture value with the image.

## How to use w/ bash script
Comment in/out the datasets you want to download, unzip, and process. We will be using datasets 1, 3, 4, and 5.
1. Install the dependencies by running ```pip install -r requirements.txt```.
2. Run ```./get-and-process-dataset.sh``` in terminal and the rest will be done for you.
3. Download your CVAT data sets and move it to the same directory as the PSKUS_dataset and PSKUS_dataset_preprocessed. Rename it as 'CVAT_dataset'.
4. Go in the CVAT_dataset folder. Rename each dataset folder to this format: 'CVATDataSet#' (eg. CVATDataSet1).
5. Go in the process_cvat_files directory where you will find three scripts: filter_not_washing.py, process_cvat.py, and rename_txt_files.py
### IMPORTANT: The scripts in step7 need to be executed in the correct sequence. Follow the steps below
6. Run ```./rename_txt_files.py```
7. Run ```./process_cvat.py```
8. Run ```./filter_not_washing.py```

## How to use w/o bash script
1. Download PSKUS datasets and extract them into a folder called PSKUS_dataset in the same directory as the scripts and README.
2. With the extracted datasets in the folder (eg. ./PSKUS_dataset/DataSet4), run ```python separate-frames.py``` to process the videos.
3. Download your CVAT data sets and move it to the same directory as the PSKUS_dataset and PSKUS_dataset_preprocessed. Rename it as 'CVAT_dataset'.
4. Go in the CVAT_dataset folder. Rename each dataset folder to this format: 'CVATDataSet#' (eg. CVATDataSet1).
5. Go in the process_cvat_files directory where you will find three scripts: filter_not_washing.py, process_cvat.py, and rename_txt_files.py
### IMPORTANT: The scripts in step5 need to be executed in the correct sequence. Follow the steps below
6. Run ```python rename_txt_files.py```
7. Run ```python process_cvat.py```
8. Run ```python filter_not_washing.py```


## Credits and References
Scripts are based from
https://github.com/edi-riga/handwash/tree/master

Used to run on PSKUS datasets to split videos into frames and pairing with their gesture value
https://zenodo.org/record/4537209

