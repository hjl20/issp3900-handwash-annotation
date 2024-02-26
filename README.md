# issp3900-handwash-annotation
This repo contains scripts to split PSKUS videos into frames and save the frame's gesture value with the image.

## How to use w/ bash script
Comment in/out the datasets you want to download, unzip, and process. We will be using datasets 1, 3, 4, and 5.
1. Get the required dependencies with ```pip install -r requirements.txt```
2. Run ```./get-and-process-dataset.sh``` in terminal and the rest will be done for you.

## How to use w/o bash script
1. Download PSKUS datasets and extract them into a folder called PSKUS_dataset in the same directory as the scripts and README.
2. With the extracted datasets in the folder (eg. ./PSKUS_dataset/DataSet4), run ```python separate-frames.py``` to process the videos.


## Credits and References
Scripts are based from
https://github.com/edi-riga/handwash/tree/master

Used to run on PSKUS datasets to split videos into frames and pairing with their gesture value
https://zenodo.org/record/4537209

