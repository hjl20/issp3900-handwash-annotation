#!/bin/bash



echo "Renaming all the .txt files in the PublicDataset folder..."
# Rename all the .txt files in the PublicDataset folder 
./rename_txt_files.py

echo "Changing the gesture values on the CVAT Dataset..."
# Changes the gesture values on the CVAT Dataset
./process_cvat.py

echo "Filtering out all the non washing gestures..."
# Filter out the not washing and delete the files from CVATDataset and Dataset_IMG
./filter_not_washing.py
