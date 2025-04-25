import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage import io, color
from PIL import Image

data = np.load("data_files1/Cn1_3_5_thermomixer_4days_s1_segm_cellposev1.npz")
print()
image = io.imread("Cn1_3_5_thermomixer_4days_s1_20x_BF.tif")

mask = data["arr_0"]
count_dict = {}

print(mask)
print(mask[np.nonzero(mask)])
print(np.nonzero(mask))

for c in mask[np.nonzero(mask)]:
    if c not in count_dict:
        count_dict[c] = 0
    count_dict[c] += 1