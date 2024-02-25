#!/usr/bin/env python3

#
# This script takes input folders with video files and annotations
# and converts them to output folders.

import cv2
import os
import json
# print("Current working directory:", os.getcwd())
# Change these directories to your own locations
input_folder = './PSKUS_dataset'
output_folder = './PSKUS_dataset_preprocessed'

# the movement codes are from 0 to 7
TOTAL_MOVEMENTS = 8

# the Annotator directories go from Annotator1 to Annotator8
TOTAL_ANNOTATORS = 8

FULL_PROCESSING = True


def majority_vote(lst):
    """Returns the element present in majority of the list, or -1 otherwise
    """
    counts = [0] * TOTAL_MOVEMENTS
    for el in lst:
        counts[int(el)] += 1
    best = 0
    for i in range(1, TOTAL_MOVEMENTS):
        if counts[best] < counts[i]:
            best = i
    majority = (len(lst) + 2) // 2
    # TODO: figure out what to do if no majority vote
    if counts[best] < majority:
        return -1
    return best


def find_frame_labels(fullpath):
    """Returns movement codes for each frame
    """
    filename = os.path.basename(fullpath)
    annotators_dir = os.path.join(os.path.dirname(os.path.dirname(fullpath)), "Annotations")

    annotations = []

    for a in range(1, TOTAL_ANNOTATORS + 1):
        annotator_dir = os.path.join(annotators_dir, "Annotator" + str(a))
        json_filename = os.path.join(annotator_dir, filename.split(".")[0] + ".json")

        # Get annotations from file
        if os.access(json_filename, os.R_OK):
            with open(json_filename, "r") as f:
                try:
                  data = json.load(f)
                except:
                  print("failed to load {}".format(json_filename))
                  continue
                a_annotations = [data['labels'][i]['code'] for i in range(len(data['labels']))]
                annotations.append(a_annotations)

    num_annotators = len(annotations)
    num_frames = len(annotations[0])
    codes = []
    for frame_num in range(num_frames):
        frame_annotations = [annotations[a][frame_num] for a in range(num_annotators)]
        frame_codes = [frame_annotations[a] for a in range(num_annotators)]
        # treat movement 7 as movement 0
        frame_codes = [0 if code == 7 else code for code in frame_codes]

        # Get code num recorded by majority of annotators for each frame
        codes.append(majority_vote(frame_codes))
    return codes


def get_frames(folder):
    print('Processing folder: ' + folder + ' ...')

    for subdir, dirs, files in os.walk(os.path.join(input_folder, folder)):
        for videofile in files:

            # exit early if not desired file format
            if not videofile.endswith(".mp4"):
                continue
                
            if not FULL_PROCESSING:
                continue

            print('Video name: ' + os.path.splitext(videofile)[0])
            
            # get gesture code of current video
            fullpath = os.path.join(subdir, videofile)
            codes = find_frame_labels(fullpath)

            # video splitting process
            vidcap = cv2.VideoCapture(fullpath)
            is_success, image = vidcap.read()
            frame_number = 0

            while is_success:
                code = codes[frame_number]

                assert code == codes[frame_number]

                # name frame based on video
                video_name = os.path.splitext(videofile)[0]
                filename = '{}_frame_{}.jpg'.format(video_name, frame_number)
                save_path_and_name = os.path.join(output_folder, folder, filename)
                
                # save frame as image + gesture code as txt
                cv2.imwrite(save_path_and_name, image)
                with open(f'{save_path_and_name}.txt', 'w') as f:
                    f.write(str(code))

                # check next (i think)
                is_success, image = vidcap.read()
                frame_number += 1


def main():
    # Gets folders of datasets to process
    list_of_folders = [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]
    for folder in sorted(list_of_folders):
        # Create output folders
        if not os.path.isdir(os.path.join(output_folder)):
            os.mkdir(output_folder)
        if not os.path.isdir(os.path.join(output_folder, folder)):
            os.mkdir(os.path.join(output_folder, folder))
        get_frames(folder)

# ----------------------------------------------
if __name__ == "__main__":

    main()
