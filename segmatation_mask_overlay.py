import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage import io, color

mask_data = np.load("data_files1/cn1/Cn1_3_5_thermomixer_4days_s1_segm_cellposev1.npz")
image = io.imread("Cn1_3_5_thermomixer_4days_s1_20x_BF.tif")
mask = mask_data["arr_0"]

# df = pd.DataFrame(mask)
# df.to_csv("saved_data.csv")

im_max = np.max(image, axis=0)
mx = np.max(im_max)
rescaled = im_max / mx

colors = []
for i in range(np.max(mask)):
    colors.append(tuple([np.random.choice(range(255))/255, np.random.choice(range(255))/255, np.random.choice(range(255))/255]))
plt.imshow(color.label2rgb(label=mask, image=rescaled, colors=colors, alpha=0.15, bg_label=0, bg_color=None))

plt.savefig('overlay.png', dpi=1000)
# plt.show()
