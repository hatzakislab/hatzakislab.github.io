#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 17:10:36 2018

@author: sorensnielsen
"""


from __futures__ import print
from pims import ImageSequence
import numpy as np
import pandas as pd
import trackpy as tp
import matplotlib as mpl
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from scipy import ndimage
from skimage.feature import blob_log
from skimage import feature
from scipy.stats.stats import pearsonr
import os
import scipy
import scipy.ndimage as ndimage
from skimage import measure
from skimage.color import rgb2gray
import matplotlib.patches as mpatches


def extract_mask_from_raw(raw, mask_bool, mask_inverse_bool):
    full_val = sum((raw[mask_bool]))
    pixels = np.sum(mask_bool)
    val_per_pixel = float(full_val) / float(pixels)

    BG = sum((raw[mask_inverse_bool]))
    pixels_BG = np.sum(mask_inverse_bool)
    val_per_pixel_BG = float(BG) / float(pixels_BG)

    raw_bg_correct = raw - val_per_pixel_BG

    return (
        raw_bg_correct,
        val_per_pixel,
        pixels,
    )  # return bg corrected image and average pixel value of membraneand area in pixels


def image_routine(raw_image):
    image = ndimage.gaussian_filter(raw_image, sigma=(5, 1), order=0)  # blurr a little
    median = np.median(image)  # get the mean
    mask = np.ma.masked_where(image < median * 1.5, image)  # return cell walls
    mask_inv = np.ma.masked_where(
        image > median * 1.5, image
    )  # return inverse of this cell walls, boolean could be used for bg correct
    array = np.zeros(image.shape)
    img_contour = np.array(array + mask, dtype=np.float)
    img_contour_inv = np.array(array + mask_inv, dtype=np.float)

    mask_bool = img_contour > 0
    mask_inverse_bool = img_contour_inv > 0

    return mask_bool, mask_inverse_bool


def number_of_cells(raw_image):
    from skimage import measure
    from skimage.segmentation import clear_border

    image = ndimage.gaussian_filter(raw_image, sigma=(0.5, 0.5), order=0)
    median = np.median(image)
    # mask =np.ma.masked_where(image<median*2.,image) # return cell walls
    mask_inv = np.ma.masked_where(image > median * 1.5, image)  # was 5
    array = np.zeros(image.shape)
    img_contour_inv = np.array(array + mask_inv, dtype=np.float)
    mask_inverse_bool = img_contour_inv > 0
    mask_inverse_bool_no_edge = clear_border(mask_inverse_bool)  # remove border stuff

    labels = measure.label(mask_inverse_bool, connectivity=1)
    labels_no_edge = measure.label(mask_inverse_bool_no_edge, connectivity=1)

    return labels_no_edge  # labels
    # fig,ax = plt.subplots(figsize=(10, 5))
    # ax.imshow(labels)
    # print(labels.max())


def region_probs(label_image, intensity_image):
    df = measure.regionprops(label_image, intensity_image=intensity_image)
    centers = [i.centroid for i in df]
    areas = [i.area for i in df]
    holes = [i.euler_number for i in df]  # could usefull for detection of nucleus
    image = [i.image for i in df]
    convex = [i.convex_image for i in df]
    bbox = [i.bbox for i in df]
    filled_image = [i.filled_image for i in df]
    intensity_image = [i.intensity_image for i in df]
    coords = [i.coords for i in df]
    centroid = [i.centroid for i in df]
    df = pd.DataFrame(
        {
            "centers": centers,
            "areas": areas,
            "holes": holes,
            "image": image,
            "convex": convex,
            "bbox": bbox,
            "filled_image": filled_image,
            "intensity_image": intensity_image,
            "coords": coords,
            "centroid": centroid,
        }
    )
    df = df[df.holes < 1]  # rough sorting
    df = df[df.areas > 1000]  # rough sorting
    df = df[df.areas < 30000]

    return df


"""
image_raw = ndimage.imread('try1.tif')
image = np.asarray(image_raw)
labels = number_of_cells(image)
df = region_probs(labels)

mask_bool, mask_inverse_bool = image_routine(image)

raw_bg_correct,val_per_pixel, pixels=extract_mask_from_raw(image,mask_bool, mask_inverse_bool)
"""


def cell_plotter(raw_bg_correct, df, mask_bool, name):
    fig, ax = plt.subplots(1, 3, figsize=(10, 5))
    ax[0].imshow(raw_bg_correct * 2, cmap="gray")
    ax[1].imshow(raw_bg_correct)
    for i in df["centers"]:
        ax[1].plot(i[1], i[0], "ro")

    ax[1].text(
        0.05,
        0.95,
        ("N = " + str(len(df["centers"]))),
        family="monospace",
        transform=ax[1].transAxes,
        fontsize=20,
        verticalalignment="top",
        color="white",
    )
    ax[2].imshow(mask_bool)
    ax[0].set_title("Raw image")
    ax[1].set_title("Located cells")
    ax[2].set_title("Located membrane")
    fig.tight_layout()

    fig.savefig(name + "_cell_count_.pdf")

    fig.clf()


def image_convex_creator(image, bbox, convex, centroid):
    # from area
    array_like = np.zeros(image.shape, dtype=bool)

    for i in range(len(centroid)):
        minr, minc, maxr, maxc = bbox[i]
        array_like[minr:maxr, minc:maxc] += convex[i]
    return array_like


def line_scanner(image):
    from skimage import measure

    yloc = 456
    image = ndimage.gaussian_filter(image, sigma=(1, 1), order=0)
    line1 = measure.profile_line(image, (yloc, 0), (yloc, 1388))
    fig, ax = plt.subplots(2, 1, figsize=(10, 5), sharex=True, sharey=False)
    ax[0].imshow(image, cmap="gray")
    ax[0].set_ylim(yloc - 100, yloc + 100)

    ax[0].axhline(y=yloc, xmin=0, xmax=1)
    ax[1].plot(line1)


def better_cell_membrane(image):
    image = np.asarray(image)
    median = np.median(image)
    # from skimage.segmentation import clear_border

    image2 = ndimage.gaussian_filter(image, sigma=(2, 2), order=0)
    image2 = ndimage.gaussian_filter(image2, sigma=(1, 1), order=0)
    mask_inv = np.ma.masked_where(image2 > median * 10, image)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(mask_inv, cmap="gray")


# fig,ax = plt.subplots(figsize=(10, 5))
# ax.imshow(image_raw,cmap = "gray")


def get_hull_image(image2, image):
    inside_hull = image[image2]
    return inside_hull


# inside_hull = get_hull_image(image2,image)


def get_non_membrane_signal_values(inside_hull):
    length = len(inside_hull)
    median = np.median(inside_hull)
    above_threshold = inside_hull > median * 5
    above_threshold = sum(above_threshold)
    total_sum = sum(inside_hull)
    BG_correct_total = total_sum - (length * median)
    val_per_pixel = BG_correct_total / above_threshold
    return BG_correct_total, val_per_pixel


def get_membrane_signal_values(outside_hull):
    length = len(outside_hull)
    median = np.median(outside_hull)
    above_threshold = outside_hull > median * 5
    above_threshold = sum(above_threshold)
    total_sum = sum(outside_hull)
    BG_correct_total = total_sum - (length * median)
    val_per_pixel = BG_correct_total / above_threshold
    return BG_correct_total, val_per_pixel


def get_membrane_signal(image, bbox, convex, centroid):
    # from area
    array_like = np.zeros(image.shape, dtype=bool)

    for i in range(len(centroid)):
        tmp_array = np.invert(convex[i])
        minr, minc, maxr, maxc = bbox[i]
        array_like[minr:maxr, minc:maxc] += tmp_array
    return array_like


def get_membrane_signal2(image, bbox, filled, centroid):
    # from area
    array_like = np.zeros(image.shape, dtype=bool)

    for i in range(len(centroid)):
        shape = filled[i].shape
        # shape = tuple([shape[0]+20,shape[1]+20])
        shape = tuple([shape[0], shape[1]])
        tmp_array = np.ones(shape, dtype=bool)
        minr, minc, maxr, maxc = bbox[i]
        # array_like[minr-10:maxr+10,minc-10:maxc+10] +=tmp_array
        array_like[minr:maxr, minc:maxc] += tmp_array
    return array_like


# bbox_img = get_membrane_signal(image,bbox,convex,centroid)
# bbox_img2 = get_membrane_signal2(image,bbox,filled,centroid)


# fig,ax = plt.subplots(figsize=(10, 5))
# ax.imshow(image,cmap = "gray")
# ax.imshow(convex_img,cmap = "Reds",alpha = 0.2)
# ax.imshow(bbox_img2-convex_img,cmap = "Blues",alpha = 0.2)

# first get bbox, substract convex then extract membrane signal


# fig,ax = plt.subplots(figsize=(10, 5))
# ax.imshow(image3-image2,cmap = "gray")


def remove_convex_from_bbox(image, bbox, convex, centroid, filled):
    convex_img = image_convex_creator(image, bbox, convex, centroid)
    bbox_img = get_membrane_signal2(image, bbox, filled, centroid)
    return bbox_img - convex_img


# membranes is membrane, convex_img is inside


def get_signal(image, convex_img, mask_membrane, coords):
    found_cells = len(coords)
    tmp_raw_convex = pd.DataFrame({"vals": (image[convex_img])})
    median_tmp_convex = np.median(tmp_raw_convex["vals"])
    convex_signal = [x for x in tmp_raw_convex["vals"] if x >= median_tmp_convex * 2]
    convex_signal
    if len(convex_signal) < 1:
        convex_signal_area_correct = "Na"
        convex_signal = "Na"
    else:
        convex_signal_area_correct = sum(convex_signal) / float(len(convex_signal))
        convex_signal = sum(convex_signal)

    pixels_convex = np.sum(convex_img)
    total_convex = np.sum(tmp_raw_convex["vals"])
    # area_corrected_convex = float(total_convex)/float(pixels_convex)
    error_pixel_convex = np.std(tmp_raw_convex["vals"])

    tmp_raw_membrane = pd.DataFrame({"vals": (image[mask_membrane])})
    median_tmp_membrane = np.median(tmp_raw_membrane["vals"])
    membrane_signal = [
        x for x in tmp_raw_membrane["vals"] if x >= median_tmp_membrane * 2
    ]
    if len(membrane_signal) < 1:
        membrane_signal_area_corrected = "Na"
        membrane_signal = "Na"
    else:
        membrane_signal_area_corrected = sum(membrane_signal) / float(
            len(membrane_signal)
        )
        membrane_signal = sum(membrane_signal)

    pixels_membrane = np.sum(mask_membrane)
    total_membrane = np.sum(tmp_raw_membrane["vals"])
    # area_corrected_membrane = float(total_membrane)/float(pixels_membrane)
    error_pixel_membrane = np.std(tmp_raw_membrane["vals"])

    df = pd.DataFrame(
        {
            "median_tmp_convex": median_tmp_convex,
            "Cells": found_cells,
            "pixels_convex": pixels_convex,
            "total_convex": total_convex,
            "convex_signal_area_correct_above_threshold": convex_signal_area_correct,
            "convex_signal_above_threshold": convex_signal,  #
            "error_pixel_convex": error_pixel_convex,
            "median_tmp_membrane": median_tmp_membrane,
            "pixels_membrane": pixels_membrane,
            "total_membrane": total_membrane,
            "membrane_signal_area_corrected_above_threshold": membrane_signal_area_corrected,
            "membrane_signal_above_threshold": membrane_signal,
            "error_pixel_membrane": error_pixel_membrane,
        },
        index=[0],
    )

    return df


mask_cmap = plt.cm.Blues
mask_cmap.set_under("k", alpha=0)

mask_cmap_r = plt.cm.Reds
mask_cmap_r.set_under("k", alpha=0)


def image_analyzer(sub_directory, Directory_main):
    counter = 0
    import glob

    for sub in sub_directory:
        image_list = []
        image_list.append(glob.glob(str(Directory_main + sub + "*.tif")))
        final_df = pd.DataFrame()

        for lister in image_list:
            for images in lister:
                image_raw = ndimage.imread(images)
                image = np.asarray(image_raw)
                image = image[:, :, 0]
                labels = number_of_cells(image)
                df = region_probs(labels, image)

                convex = df["convex"].tolist()
                image2 = df["intensity_image"].tolist()
                filled = df["filled_image"].tolist()
                coords = df["coords"].tolist()
                bbox = df["bbox"].tolist()
                centroid = df["centroid"].tolist()
                areas = df["areas"].tolist()
                convex_img = image_convex_creator(image, bbox, convex, centroid)

                mask_membrane = remove_convex_from_bbox(
                    image, bbox, convex, centroid, filled
                )

                signal_df = get_signal(image, convex_img, mask_membrane, coords)
                signal_df["image"] = images

                fig, ax = plt.subplots(1, 4, figsize=(12, 8))
                ax[0].imshow(image, cmap="gray")
                ax[0].set_title("Raw")
                ax[1].imshow(convex_img, cmap="Reds", alpha=0.2)
                ax[1].set_title("Inside")
                ax[2].imshow(mask_membrane, cmap="Blues")
                ax[2].set_title("Membrane")

                ax[3].imshow(image, cmap="gray")
                ax[3].imshow(convex_img, cmap="Reds", alpha=0.4)
                ax[3].imshow(mask_membrane, cmap="Blues", alpha=0.4)
                ax[3].set_title("Combined")

                fig.tight_layout()
                fig.savefig(str(images[:-4] + ".pdf"))
                fig.clf()
                final_df = final_df.append(signal_df, ignore_index=False)
                counter += 1
                print(counter)

        final_df.to_csv(
            Directory_main + sub + "__data__.csv",
            header=True,
            index=None,
            sep=" ",
            mode="a",
        )


def string_name_reader(name):  # return the condition'

    names = ["stim", "TAMRA-NPY", "PYY", "GUB"]  # PYY1, PYY3  # check for GUB after

    if name.find(names[0]) != -1:
        return "no_stim"

    elif name.find(names[1]) != -1:
        pos = name.find(names[1])
        tmp_name = name[pos : pos + 9]
        return str(tmp_name)

    elif name.find(names[2]) != -1:
        pos = name.find(names[2])
        tmp_name = name[pos : pos + 7]
        return str(tmp_name)

    elif name.find(names[3]) != -1:
        pos = name.find(names[3])
        tmp_name = name[pos + 5 : pos + 9]
        return tmp_name


def string_cell_reader(name):
    names = ["HEK"]
    if name.find(names[0]) != -1:
        return "HEK293_Y2_eYFP"
    else:
        return "Inkognito"


def string_year_reader(name):
    names = ["2018"]
    if name.find(names[0]) != -1:
        return "2018"
    else:
        return "2017"


# ready for looping over shit
Directory_main2 = "/Volumes/Soeren/Soren(Nikos)/Tamra-fluorescence/"
subs2 = [
    "1 uM Tamra-PYY analogue 1h/",
    "1 uM Tamra-PYY analogue 1h - red light!/",
    "100 nM Tamra-PYY analogue 1h/",
    "no stimulation_Tamra intensity/",
]
Directory_main = "/Volumes/Soeren/Soren(Nikos)/YFP fluorescence/"
subs = [
    "YFP fluorescence_1uM peptide_1h/",
    "YFP fluorescence_100nM peptide_1h/",
    "YFP fluorescene_no stimulation/",
]


# image_analyzer(subs,Directory_main)
# image_analyzer(subs2,Directory_main2)


# visualize data
csv_file = "/Volumes/Soeren/Soren(Nikos)/data_YFP/1µM__data__.csv"


cond = "1uM"
data = pd.read_csv(csv_file, low_memory=False, sep=" ")

data["Condition"] = data["image"].apply(string_name_reader)
data["Year"] = data["image"].apply(string_year_reader)
data["Cell"] = data["image"].apply(string_cell_reader)

import seaborn as sns

data = data.sort_values("Condition", ascending=True)
fig, ax = plt.subplots(figsize=(10, 5))
ax = sns.boxplot(x="Condition", y="Cells", data=data)
ax.set_ylim(0, 80)
plt.xticks(rotation="vertical")
ax.set_title(cond)
ax.set_xlabel("Drug")
fig.tight_layout()
fig.savefig("/Volumes/Soeren/Soren(Nikos)/data_YFP/Cell_count_" + cond + "_.pdf")

plt.clf()

data["count"] = data.groupby("Condition")["Cells"].transform(sum)
data_count = data.drop_duplicates(["Condition"])
data_count.to_csv(
    "/Volumes/Soeren/Soren(Nikos)/data_YFP/__count__" + cond + "_.csv",
    header=True,
    index=None,
    sep=" ",
    mode="a",
)


data["area_corrected_membrane"] = (
    data["total_membrane"] / data["pixels_membrane"]
) - data["median_tmp_membrane"]
data["area_corrected_convex"] = (data["total_convex"] / data["pixels_convex"]) - data[
    "median_tmp_convex"
]
data["ratio_convex_to_membrane"] = (
    data["area_corrected_convex"] / data["area_corrected_membrane"]
)


# data_1uM = data
# data_1uM.to_csv('/Volumes/Soeren/Soren(Nikos)/data_YFP/__data_1uM__.csv', header=True, index=None, sep=' ', mode='a')

# data_100nM = data
# data_100nM.to_csv('/Volumes/Soeren/Soren(Nikos)/data_YFP/__data_100nM__.csv', header=True, index=None, sep=' ', mode='a')

# data_nostim = data
# data_nostim.to_csv('/Volumes/Soeren/Soren(Nikos)/data_YFP/__data_nostim__.csv', header=True, index=None, sep=' ', mode='a')


data_full.to_csv(
    "/Volumes/Soeren/Soren(Nikos)/data_YFP/__data_full__.csv",
    header=True,
    index=None,
    sep=" ",
    mode="a",
)

del (data_here)
data_here = data_100nM.append(data_nostim)
data = data.sort_values("Condition", ascending=True)
data_here["count"] = data.groupby("Condition")["Cells"].transform(sum)

medians = data_here.groupby(["Condition"])["area_corrected_membrane"].median().values

data_count = data_here.drop_duplicates(["Condition"])
data_count = data_count["count"].tolist()

# data_count = [str(x) for x in data_count]
# data_count = ["n: " + i for i in data_count]
# pos = range(len(data_count))


from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements = [
    Patch(facecolor="dimgray", edgecolor="black", label="Membrane"),
    Patch(facecolor="lightgrey", edgecolor="black", label="Inside"),
    Line2D([0], [0], color="red", lw=3, label="No stim membrane"),
    Line2D([0], [0], color="blue", lw=3, label="No stim inside"),
]


fig, ax = plt.subplots(figsize=(10, 5))
ax = sns.boxplot(
    x="Condition",
    y="area_corrected_membrane",
    data=data_here,
    color="dimgrey",
    saturation=0.3,
)
ax = sns.boxplot(
    x="Condition",
    y="area_corrected_convex",
    data=data_here,
    color="lightgrey",
    saturation=0.3,
)
ax.plot(
    [0, 19],
    [
        data_nostim["area_corrected_membrane"].median(),
        data_nostim["area_corrected_membrane"].median(),
    ],
    "red",
    linewidth=2,
    alpha=0.5,
)
ax.plot(
    [0, 19],
    [
        data_nostim["area_corrected_convex"].median(),
        data_nostim["area_corrected_convex"].median(),
    ],
    "blue",
    linewidth=2,
    alpha=0.5,
)
ax.legend(["1", "2", "3", "4"], loc="upper right")
ax.legend(handles=legend_elements, loc="upper left")
plt.xticks(rotation="vertical")
ax.set_title("1 uM")
ax.set_xlabel("Drug")
ax.set_ylabel("Intensity [AU]")
fig.tight_layout()
plt.xticks(rotation="vertical")
ax.set_title("100 nM")
ax.set_xlabel("Drug")

# for tick,label in zip(pos,ax.get_xticklabels()):
#    ax.text(pos[tick], medians[tick], data_count[tick],
#            horizontalalignment='center', size='small', color='red', weight='semibold')


fig.savefig("/Volumes/Soeren/Soren(Nikos)/data_YFP/signal__100nm__.pdf")


legend_elements = [
    Patch(facecolor="skyblue", edgecolor="blue", label="Membrane"),
    Patch(facecolor="indianred", edgecolor="red", label="Inside"),
    Line2D([0], [0], color="blue", lw=3, label="No stim membrane"),
    Line2D([0], [0], color="red", lw=3, label="No stim inside"),
]

fig, ax = plt.subplots(figsize=(15, 10))
ax = sns.boxplot(
    x="Condition",
    y="area_corrected_membrane",
    hue="conc",
    width=0.7,
    data=data_full,
    palette="Blues",
    boxprops=dict(alpha=0.6),
)
ax = sns.boxplot(
    x="Condition",
    y="area_corrected_convex",
    hue="conc",
    width=0.7,
    data=data_full,
    palette="Reds",
    boxprops=dict(alpha=0.6),
)
# ax.plot([0,19], [data_nostim['area_corrected_membrane'].median(),data_nostim['area_corrected_membrane'].median()], 'blue', linewidth = 2, alpha = 0.5)
# ax.plot([0,19], [data_nostim['area_corrected_convex'].median(),data_nostim['area_corrected_convex'].median()], 'red', linewidth = 2, alpha = 0.5)
ax.set_xlabel("Drug")
ax.set_ylabel("Intensity [AU]")
plt.xticks(rotation="vertical")
fig.savefig("/Volumes/Soeren/Soren(Nikos)/data_YFP/signal__all__.pdf")


m
ax = sns.pointplot(
    x="Condition",
    y="area_corrected_membrane",
    hue="conc",
    width=0.7,
    data=data_full,
    palette="Blues",
    join=False,
    capsize=0.2,
)
ax = sns.pointplot(
    x="Condition",
    y="area_corrected_convex",
    hue="conc",
    width=0.7,
    data=data_full,
    palette="Reds",
    join=False,
    capsize=0.2,
)
# ax.plot([0,19], [data_nostim['area_corrected_membrane'].mean(),data_nostim['area_corrected_membrane'].median()], 'blue', linewidth = 2, alpha = 0.5)
# ax.plot([0,19], [data_nostim['area_corrected_convex'].mean(),data_nostim['area_corrected_convex'].median()], 'red', linewidth = 2, alpha = 0.5)
ax.set_xlabel("Drug")
ax.set_ylabel("Intensity [AU]")
plt.xticks(rotation="vertical")
fig.savefig("/Volumes/Soeren/Soren(Nikos)/data_YFP/signal__all__errorbars__.pdf")


fig, ax = plt.subplots(figsize=(15, 10))
ax = sns.pointplot(
    x="Condition",
    y="ratio_convex_to_membrane",
    hue="conc",
    width=0.7,
    data=data_full,
    join=False,
    capsize=0.2,
)
ax.set_xlabel("Drug")
ax.set_ylabel("Intensity [AU]")
plt.xticks(rotation="vertical")
ax.legend(loc="upper left")
fig.savefig("/Volumes/Soeren/Soren(Nikos)/data_YFP/signal__all__ratio__.pdf")


data_full["count"] = data_full.groupby(["Condition", "conc"])["Cells"].transform(sum)
cell_count = data_full.sort_values(["Condition"], ascending=True).drop_duplicates(
    ["Condition", "conc"]
)


data_count = data_full.groupby(["Condition", "conc"]).size()
new_df = data_count.to_frame(name="size").reset_index()
new_df["cells"] = cell_count["count"].tolist()

new_df.to_csv(
    "/Volumes/Soeren/Soren(Nikos)/data_YFP/__data_count__.csv",
    header=True,
    index=None,
    sep=" ",
    mode="a",
)

# read and split csv file after compounds


# data = pd.read_csv(csv_file, low_memory=False, sep = " ")


"""
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(image)

fig,ax = plt.subplots(figsize=(10, 5))
ax.imshow(filled[0],cmap = "gray")
ax.plot(coords[0])
ax.imshow(image,cmap = "gray")


fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(image)
for i in range(len(bbox)):
    # take regions with large enough areas

        # draw rectangle around segmented coins
    minr, minc, maxr, maxc = bbox[i]
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

ax.set_axis_off()
plt.tight_layout()
plt.show()
"""


"""



# make a little looping over stuff
Directory_main=os.getcwd()

import glob
image_list_stim = glob.glob(str(Directory_main+'/images_stim/*.tif'))


total_cells                 = []
all_areas                   = []
area_of_membrane_total      = []
avg_pixel_val               = []

Directory = str(Directory_main+'/images_stim/')
for image in image_list_stim:

    name = str(Directory+image[-36:])
    image_raw = ndimage.imread(image)
    image = np.asarray(image_raw)
    image = image[:,:,0]
    labels = number_of_cells(image)
    df = region_probs(labels)

    mask_bool, mask_inverse_bool = image_routine(image)
    raw_bg_correct,val_per_pixel, pixels=extract_mask_from_raw(image,mask_bool, mask_inverse_bool)
    cell_plotter(raw_bg_correct,df,mask_bool,name)
    total_cells.append(len(df['centers']))
    all_areas.append(df['areas'])
    area_of_membrane_total.append(pixels)
    avg_pixel_val.append(val_per_pixel)



total_cells_nostim                 = []
all_areas_nostim                   = []
area_of_membrane_total_nostim      = []
avg_pixel_val_nostim               = []


image_list_no_stim =glob.glob(str(Directory_main+'/images_no_stim/*.tif'))

Directory = str(Directory_main+'/images_no_stim/')
for image in image_list_no_stim:

    name = str(Directory+image[-30:])
    image_raw = ndimage.imread(image)
    image = np.asarray(image_raw)
    image = image[:,:,0]
    labels = number_of_cells(image)
    df = region_probs(labels)

    mask_bool, mask_inverse_bool = image_routine(image)
    raw_bg_correct,val_per_pixel, pixels=extract_mask_from_raw(image,mask_bool, mask_inverse_bool)
    cell_plotter(raw_bg_correct,df,mask_bool,name)
    total_cells_nostim.append(len(df['centers']))
    all_areas_nostim.append(df['areas'])
    area_of_membrane_total_nostim.append(pixels)
    avg_pixel_val_nostim.append(val_per_pixel)
"""
"""
fig,ax = plt.subplots(1,2,figsize=(10, 5), sharey= True)
ax[0].boxplot(total_cells)
ax[1].boxplot(total_cells_nostim)
ax[0].set_ylabel('Cells')
ax[0].set_title('Stimulated')
ax[1].set_title('No Stim')
fig.tight_layout()
fig.savefig('Cell_count.pdf')
fig.clf()


fig,ax = plt.subplots(1,2,figsize=(10, 5), sharey= True)
ax[0].boxplot(avg_pixel_val)
ax[1].boxplot(avg_pixel_val_nostim)
ax[0].set_ylabel('Membrane Int')
ax[0].set_title('Stimulated')
ax[1].set_title('No Stim')
fig.tight_layout()
fig.savefig('membrane_signal.pdf')
fig.clf()


fig,ax = plt.subplots(1,2,figsize=(10, 5), sharey= True)
ax[0].boxplot(all_areas)
ax[1].boxplot(all_areas_nostim)
ax[0].set_ylabel('Cell area [pixel]')
ax[0].set_title('Stimulated')
ax[1].set_title('No Stim')
fig.tight_layout()
fig.savefig('Avg_cell_area.pdf')
fig.clf()

fig,ax = plt.subplots(1,2,figsize=(10, 5), sharey= True)
ax[0].boxplot(area_of_membrane_total)
ax[1].boxplot(area_of_membrane_total_nostim)
ax[0].set_ylabel('Membrane area total [pixel]')
ax[0].set_title('Stimulated')
ax[1].set_title('No Stim')
fig.tight_layout()
fig.savefig('Total_membrane_area.pdf')
fig.clf()

"""
