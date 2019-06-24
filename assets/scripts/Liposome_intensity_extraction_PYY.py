import os
import time
import numpy as np
from PIL import Image
from multiprocessing import Pool
from pims import ImageSequence
import numpy as np
import pandas as pd
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt
from skimage import feature
import scipy.ndimage as ndimage
from skimage.feature import blob_log
import trackpy as tp
import os
from scipy.ndimage.filters import gaussian_filter
from timeit import default_timer as timer
from glob import glob
from iminuit import Minuit
from probfit import BinnedLH, Chi2Regression, Extended, BinnedChi2, UnbinnedLH, gaussian
from pims import TiffStack
import pandas as pd
from skimage.feature import blob_log
import seaborn as sns


lip_BG_size = 60
lip_int_size = 40  # yields 49 pixels


def image_loader_video(video):
    images_1 = TiffStack(video)
    return images_1


def cmask(index, array, BG_size, int_size):
    a, b = index
    nx, ny = array.shape
    y, x = np.ogrid[-a : nx - a, -b : ny - b]
    mask = (
        x * x + y * y <= lip_int_size
    )  # radius squared - but making sure we dont do the calculation in the function - slow
    mask2 = x * x + y * y <= lip_int_size + 9  # to make a "gab" between BG and roi

    BG_mask = x * x + y * y <= lip_BG_size
    BG_mask = np.bitwise_xor(BG_mask, mask2)
    return (sum((array[mask]))), np.median(((array[BG_mask])))


def runner(folder):
    files = glob(str(folder + "*.tif"))

    blue_vids = []
    red_vids = []
    for filepath in files:
        if filepath.find("red") != -1:
            red_vids.append(filepath)
            print("ads")
        else:
            blue_vids.append(filepath)
            print("das")
    blue_vids.sort()
    red_vids.sort()

    blue_signal = []
    blue_bg = []
    blue_corrected = []
    red_signal = []
    red_bg = []
    red_corrected = []
    frame_list = []
    video_list = []

    for video in range(len(blue_vids)):
        video_blue = image_loader_video(blue_vids[video])
        video_red = image_loader_video(red_vids[video])

        video_counter = video
        for frame in range(len(video_blue)):
            size_maker = np.ones(video_blue[frame].shape)
            ind = 50, 50  # dont ask - leave it here, it just makes sure the below runs
            mask_size, BG_size = cmask(ind, size_maker, lip_BG_size, lip_int_size)
            mask_size = np.sum(mask_size)

            xy = pd.DataFrame(
                blob_log(
                    video_blue[frame],
                    min_sigma=1,
                    max_sigma=20,
                    threshold=0.05,
                    overlap=0.01,
                )
            )
            # xy =pd.DataFrame(blob_log(video_blue[frame],min_sigma=1,max_sigma=20,threshold=0.05,overlap = 0.01))

            x = xy[0].tolist()
            y = xy[1].tolist()
            frame_count = frame
            for i in range(len(x)):
                index = (x[i], y[i])
                mask, BG_mask = cmask(
                    index, video_blue[frame], lip_BG_size, lip_int_size
                )
                blue_signal.append(mask)
                blue_bg.append(BG_mask)
                blue_corrected.append(mask - (BG_mask * mask_size))

                mask, BG_mask = cmask(
                    index, video_red[frame], lip_BG_size, lip_int_size
                )
                red_signal.append(mask)
                red_bg.append(BG_mask)
                red_corrected.append(mask - (BG_mask * mask_size))
                frame_list.append(frame_count)
                video_list.append(video_counter)

    df = pd.DataFrame(
        {
            "blue_signal": blue_signal,
            "blue_bg": blue_bg,
            "blue_corrected": blue_corrected,
            "red_signal": red_signal,
            "red_bg": red_bg,
            "red_corrected": red_corrected,
            "frame": frame,
            "video": video,
        }
    )
    df.to_csv(str(folder + "__data__.csv"), header=True, index=None, sep=",", mode="w")


folders = [
    "/Volumes/Soeren/esben_liposome/GUB002349/",
    "/Volumes/Soeren/esben_liposome/GUB002350/",
    "/Volumes/Soeren/esben_liposome/GUB002351/",
    "/Volumes/Soeren/esben_liposome/GUB002352/",
]


for folder in folders:
    runner(folder)


def df_realign(df):
    df = df[df.blue_corrected > 0]
    df = df[df.red_corrected > 0]

    df["corrected_red_signal"] = df["red_corrected"] / np.sqrt(df["blue_corrected"])
    return df


# treating
df1 = pd.read_csv(
    "/Volumes/Soeren/esben_liposome/GUB002349/__data__.csv", low_memory=False, sep=","
)
df1 = df_realign(df1)
df1["set"] = "49"
df2 = pd.read_csv(
    "/Volumes/Soeren/esben_liposome/GUB002350/__data__.csv", low_memory=False, sep=","
)
df2 = df_realign(df2)
df2["set"] = "50"
df3 = pd.read_csv(
    "/Volumes/Soeren/esben_liposome/GUB002351/__data__.csv", low_memory=False, sep=","
)
df3 = df_realign(df3)
df3["set"] = "51"
df4 = pd.read_csv(
    "/Volumes/Soeren/esben_liposome/GUB002352/__data__.csv", low_memory=False, sep=","
)
df4 = df_realign(df4)
df4["set"] = "52"


save_path = "/Volumes/Soeren/esben_liposome/"

fig, ax = plt.subplots(figsize=(3, 3))
ax.hist(
    df1["corrected_red_signal"],
    25,
    alpha=0.5,
    color="grey",
    normed=False,
    range=(0, 500),
)
ax.hist(
    df2["corrected_red_signal"],
    25,
    alpha=0.5,
    color="red",
    normed=False,
    range=(0, 500),
)
ax.hist(
    df3["corrected_red_signal"],
    25,
    alpha=0.5,
    color="blue",
    normed=False,
    range=(0, 500),
)
ax.hist(
    df4["corrected_red_signal"],
    25,
    alpha=0.5,
    color="green",
    normed=True,
    range=(0, 500),
)

ax.legend(["GUB0049", "GUB0050", "GUB0051", "GUB0052"])
ax.set_ylabel("Density", size=14)
ax.set_xlabel("Intensity [A.U.]", size=14)
ax.tick_params(axis="both", which="major", labelsize=10)
ax.tick_params(axis="both", which="minor", labelsize=10)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(False)

fig.tight_layout()
fig.savefig(str(save_path + "__data7__.pdf"))


sum1 = np.sum(df1["corrected_red_signal"]) / len(df1["corrected_red_signal"])
std1 = np.std(df1["corrected_red_signal"]) / np.sqrt(len(df1["corrected_red_signal"]))
sum2 = np.sum(df2["corrected_red_signal"]) / len(df2["corrected_red_signal"])
std2 = np.std(df2["corrected_red_signal"]) / np.sqrt(len(df2["corrected_red_signal"]))
sum3 = np.sum(df3["corrected_red_signal"]) / len(df3["corrected_red_signal"])
std3 = np.std(df3["corrected_red_signal"]) / np.sqrt(len(df3["corrected_red_signal"]))
sum4 = np.sum(df4["corrected_red_signal"]) / len(df4["corrected_red_signal"])
std4 = np.std(df4["corrected_red_signal"]) / np.sqrt(len(df4["corrected_red_signal"]))


summed = [sum1, sum2, sum3, sum4]
stds = [std1, std2, std3, std4]

fig, ax = plt.subplots(figsize=(3, 3))
ax.bar([1, 2, 3, 4], summed, yerr=stds, alpha=0.7, color="grey", width=0.5)
plt.xticks([1, 2, 3, 4], ("0049", "0050", "0051", "0052"))
ax.set_ylabel("Intensity [A.U.]", size=14)
ax.tick_params(axis="both", which="major", labelsize=10)
ax.tick_params(axis="both", which="minor", labelsize=10)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(False)

fig.tight_layout()
fig.savefig(str(save_path + "__data8__.pdf"))

summed
stds


df4.to_csv(str(save_path + "__0052__.csv"), header=True, index=None, sep=",", mode="w")
