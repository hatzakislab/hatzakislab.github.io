#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 09:30:53 2019

@author: sorensnielsen

"""

import glob
import os

import matplotlib  as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import scipy
import scipy.ndimage as ndimage
import trackpy_OLD as tp
from pims import ImageSequence
from pims import TiffStack
from scipy import ndimage
from scipy.stats.stats import pearsonr
from skimage import feature
from skimage import feature
from skimage import io
from skimage import measure
from skimage.color import rgb2gray
from skimage.feature import blob_log
from skimage.feature import blob_log
from skimage.feature import peak_local_max


def image_loader_video(video):
    images_1 = TiffStack(video)
    return images_1


mean_multiplier = 5.75
sep = 8

# Tracking parameters
memory = 1  # frame
search_range = 7  # pixels
Object_size = 15

# tester video for initial thresholding
file_path = os.getcwd()
tif_file_loc = sorted(glob.glob(file_path + "/vid/*.tif"))
vid_name = tif_file_loc[0]

video = image_loader_video(vid_name)

# exp_type_folders=   ['vid_folder']
# exp_types=          ['3']
# save_path =         'save_folder'

exp_type_folders = ['/Users/superman/Desktop/script/vid/']
exp_types = ['3']
save_path = '/Users/superman/Desktop/script/results/'

# actual data paths and save_path
# exp_type_folders    = ['/Volumes/Soeren/Lipase/treat_2/Native/',
#                        '/Volumes/Soeren/Lipase/treat_2/Native_product/',
#                        '/Volumes/Soeren/Lipase/treat_2/Inactive/',
#                        '/Volumes/Soeren/Lipase/treat_2/L2/',
#                        '/Volumes/Soeren/Lipase/treat_2/L3/']
# exp_types           = ['Native','Native_product','Inactive','L2','L3']
# save_path = '/Volumes/Soeren/Lipase/Treats_190115/new_before_fixed_dist/'

view_frame = 199

cont = 0
while cont < 1:
    mean = np.mean(video[view_frame])

    f = tp.locate(video[view_frame], Object_size, invert=False, minmass=mean * mean_multiplier, separation=sep)
    plt.figure()  # make a new figure
    tp.annotate(f, video[view_frame])
    plt.ion()
    print(str("Found: " + str(len(f))) + ' particles')
    print("Threshold: ", mean_multiplier, "\nSeperation: ", sep)
    raw = input("Change sep or threshold?: Enter -no- if good\n")
    if raw == "no":
        cont += 5
    else:
        print("Threshold: ", mean_multiplier, "\nSeperation: ", sep)
        mean_multiplier = input("Enter threshold:\n")
        mean_multiplier = float(mean_multiplier)
        sep = input("Enter seperation in pixels:\n")
        sep = int(sep)


def step_tracker(df):
    microns_per_pixel = 0.160
    steps = []
    msd = []
    lag = []
    df = df.sort_values(by=['particle', 'frame'])
    df['x'] = df['x'] * microns_per_pixel
    df['y'] = df['y'] * microns_per_pixel
    group_all = df.groupby('particle')
    x_step = []
    y_step = []

    # easiest: compute step in x, step in y and then steps
    for name, group in group_all:
        x_list = group.x.tolist()
        x_tmp = [y - x for x, y in zip(x_list, x_list[1:])]
        x_tmp.insert(0, 0.)

        y_list = group.y.tolist()
        y_tmp = [y - x for x, y in zip(y_list, y_list[1:])]
        y_tmp.insert(0, 0.)
        y_step.extend(y_tmp)
        x_step.extend(x_tmp)
        step_tmp = [np.sqrt(y ** 2 + x ** 2) for y, x in zip(y_tmp, x_tmp)]

        steps.extend(step_tmp)

    df['x_step'] = x_step
    df['y_step'] = y_step
    df['steplength'] = steps

    return df


def tracker(video, mean_multiplier, sep):
    import collections
    # full = tp.batch(video, 15,invert=False, minmass =mean*mean_multiplier,separation= sep);
    full = tp.batch(video, Object_size, invert=False, minmass=mean * mean_multiplier, separation=sep)
    # check for subpixel accuracy
    tp.subpx_bias(full)
    plt.show()

    full_tracked = tp.link_df(full, search_range, memory=memory)  # 5 pixel search range, memory =2
    full_tracked = tp.filter_stubs(full_tracked, 1)  # filter aour short stuff

    full_tracked = step_tracker(full_tracked)
    full_tracked['particle'] = full_tracked['particle'].transform(int)
    # full_tracked['particle'] = full_tracked['particle'].transform(str)
    full_tracked['duration'] = full_tracked.groupby('particle')['particle'].transform(len)

    def msd_df(df):
        max_lagtime = max(df['duration'])
        microns_per_pixel = 0.160
        frame_per_sec = float(1000 / 81.)
        df_msd = tp.imsd(df, microns_per_pixel, frame_per_sec, max_lagtime=max_lagtime)
        return df_msd

    msd_df = msd_df(full_tracked)
    msd_df = msd_df.stack().reset_index()
    msd_df.columns = ['time', 'particle', 'msd']
    return full_tracked, msd_df


def runner_tracker(video_location, experiment_type, save_path, replicate):
    video = image_loader_video(video_location)
    full_tracked, msd_df = tracker(video, mean_multiplier, sep)

    msd_df['experiment_type'] = str(experiment_type)
    msd_df['replicate'] = str(replicate)

    full_tracked['experiment_type'] = str(experiment_type)
    full_tracked['replicate'] = str(replicate)
    full_tracked['unique_particle_id'] = str(
        str(replicate) + '_' + str(full_tracked['particle']) + '_' + str(experiment_type))

    # vid_name_lst = sorted(os.listdir(file_path))
    vid_name_lst = sorted(os.listdir(os.getcwd() + "/vid/"))
    try:
        vid_name_lst.remove('.DS_Store')
    except:
        pass
    vid_name = vid_name_lst[experiment_type][:-4]

    full_tracked.to_csv(
        str(save_path + vid_name + '__full_tracked_thres' + str(mean_multiplier) + '_sep' + str(sep) + '.csv'),
        header=True, index=None, sep=',', mode='w')
    # msd_df.to_csv(str(save_path+'__'+experiment_type+'__'+str(replicate)+'__MSD_.csv'), header=True, index=None, sep=',', mode='w')


def create_big_df(save_path):
    from glob import glob
    files = glob(str(save_path + '*.csv'))

    tracks_csv = []
    msd_csv = []
    df_new_full = pd.DataFrame()
    df_new_msd = pd.DataFrame()
    for filepath in files:
        if filepath.find('MSD') != -1:
            msd_csv.append(filepath)
        elif filepath.find('full_tracked_') != -1:
            tracks_csv.append(filepath)

    for path in tracks_csv:
        df = pd.read_csv(str(path), low_memory=False, sep=',')
        df_new_full = df_new_full.append(df, ignore_index=True)

    for path in msd_csv:
        df = pd.read_csv(str(path), low_memory=False, sep=',')
        df_new_msd = df_new_msd.append(df, ignore_index=True)

    df_new_full.to_csv(str(save_path + 'all_tracked.csv'), header=True, index=None, sep=',', mode='w')
    df_new_msd.to_csv(str(save_path + 'all_msd.csv'), header=True, index=None, sep=',', mode='w')


def create_list_of_vids(path, exp):
    from glob import glob
    files = glob(str(path + '*.tif'))
    relica_list = np.arange(len(files))
    type_list = [str(exp)] * len(files)
    return files, relica_list, type_list


# list_of_vids = []
# type_list = []
# replica_list = []
#
# for main_folder in range(len(exp_type_folders)):
#     file_paths,relica_number,exp_type = create_list_of_vids(exp_type_folders[main_folder],exp_types[main_folder])
#     list_of_vids.extend(file_paths)
#     type_list.extend(exp_type)
#     replica_list.extend(relica_number)

list_of_vids = tif_file_loc
type_list = np.arange(len(list_of_vids))
replica_list = np.arange(len(list_of_vids))

for i in range(len(list_of_vids)):
    save_path1 = save_path
    path = list_of_vids[i]
    lipase = type_list[i]
    replica = replica_list[i]
    runner_tracker(path, lipase, save_path1, replica)
    print()
    print('#########')
    print(str(1 + i), ' Round Done')
    print('#########')
    print()

create_big_df(save_path)
