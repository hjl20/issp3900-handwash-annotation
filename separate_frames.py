#!/usr/bin/env python3

# This script takes input folders with video files and annotations
# and converts them to output folders.

import cv2
import os
import json
from alive_progress import alive_bar


input_folder = './PSKUS_dataset'
output_folder = './PSKUS_dataset_preprocessed'

IMG_FOLDER_EXT = '_IMG'
TXT_FOLDER_EXT = '_TXT'

# the movement codes are from 0 to 7
TOTAL_MOVEMENTS = 8
TOTAL_ANNOTATORS = 8


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
    if counts[best] < majority:
        return -1
    return best


def find_frame_labels(video_path):
    """Returns movement codes for each frame
    """
    file_name = os.path.basename(video_path)
    annotators_dir = os.path.join(os.path.dirname(os.path.dirname(video_path)), "Annotations")

    annotations = []

    for a in range(1, TOTAL_ANNOTATORS + 1):
        annotator_dir = os.path.join(annotators_dir, "Annotator" + str(a))
        json_file_name = os.path.join(annotator_dir, file_name.split(".")[0] + ".json")

        # Get annotations from file
        if os.access(json_file_name, os.R_OK):
            with open(json_file_name, "r") as f:
                try:
                  data = json.load(f)
                except:
                  print("failed to load {}".format(json_file_name))
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
    print('Processing folder: ' + folder + ' ..')

    for subdir in os.listdir(os.path.join(input_folder, folder)):
        if not os.path.basename(subdir) == 'Videos':
            continue

        videos_list = os.listdir(os.path.join(input_folder, folder, subdir))

        with alive_bar(len(videos_list), title='Videos processed') as bar:
            for video_name in videos_list:
                if not video_name.endswith(".mp4"):
                    continue
                
                # get gesture code of current video
                video_path = os.path.join(subdir, video_name)
                codes = find_frame_labels(video_path)

                # video splitting process
                vidcap = cv2.VideoCapture(video_path)
                is_success, image = vidcap.read()
                frame_number = 0

                while is_success:
                    code = codes[frame_number]

                    assert code == codes[frame_number]

                    # name frame based on video
                    video_name = os.path.splitext(video_name)[0]
                    file_name = '{}_frame_{}'.format(video_name, frame_number)
                    save_path_img = os.path.join(output_folder, folder + IMG_FOLDER_EXT, file_name)
                    save_path_txt = os.path.join(output_folder, folder + TXT_FOLDER_EXT, file_name)
                    
                    # save frame as image + gesture code as txt
                    cv2.imwrite(save_path_img + '.jpg', image)
                    with open(f'{save_path_txt}.txt', 'w') as f:
                        f.write(str(code))

                    # check next
                    is_success, image = vidcap.read()
                    frame_number += 1
                bar()


def main():
    # Gets folders of datasets to process
    list_of_folders = [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]
    for folder in sorted(list_of_folders):
        # Create output folders
        if not os.path.isdir(os.path.join(output_folder)):
            os.mkdir(output_folder)
        if not os.path.isdir(os.path.join(output_folder, folder + IMG_FOLDER_EXT)):
            os.mkdir(os.path.join(output_folder, folder + IMG_FOLDER_EXT))
        if not os.path.isdir(os.path.join(output_folder, folder + TXT_FOLDER_EXT)):
            os.mkdir(os.path.join(output_folder, folder + TXT_FOLDER_EXT))
        get_frames(folder)

# ----------------------------------------------
if __name__ == "__main__":
    main()
