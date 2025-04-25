import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# TODO: set paths and pixel sizes
path1 = r"C:\Users\jonat\Documents\NYU_Reserach\PythonProjects\CellSegmentation\data_files1"
path2 = r"C:\Users\jonat\Documents\NYU_Reserach\PythonProjects\CellSegmentation\data_files2"
pixel_size1 = ((496.96 / 2304) ** 2)
pixel_size2 = ((117.92 / 1608) ** 2)
output_path = r"C:\Users\jonat\Documents\NYU_Reserach\PythonProjects\CellSegmentation"


def create_size_list(folder_path: str, p_size: float):
    """
    Creates a list of all the sizes of every cell. Use this for each strain individually then concatenate at the end.

    :param folder_path: data path with each strain in its own folder
    :param p_size: size of a single pixel
    :return:
    """
    masks_list = []
    with os.scandir(folder_path) as files:
        for file in files:
            if not str(file.name).endswith(".npz"):
                continue
            masks_list.append(np.load(file.path)["arr_0"])

    l = sum([np.max(pos_mask[np.nonzero(pos_mask)]) for pos_mask in masks_list])
    size_list = np.zeros(l)
    index_pointer = 0

    for pos_mask in masks_list:
        nonzero_vals = pos_mask[np.nonzero(pos_mask)]

        for cell_num in nonzero_vals:
            size_list[cell_num - 1 + index_pointer] += 1

        index_pointer += np.max(nonzero_vals)

    for i in range(len(size_list)):
        size_list[i] *= p_size
    for i in range(len(size_list) - 1, 0, -1):
        # TODO: outlier cutoff size
        if size_list[i] > 160:
            size_list = np.delete(size_list, i)

    return size_list


# TODO: creating list for each set of data that have different pixel sizes then concatenating them together
graphing_data1 = []
with os.scandir(path1) as files:
    for file in files:
        if os.path.isdir(file.path):
            graphing_data1.append(create_size_list(file.path, pixel_size1))

graphing_data2 = []
with os.scandir(path2) as files:
    for file in files:
        if os.path.isdir(file.path):
            graphing_data1.append(create_size_list(file.path, pixel_size2))

all_graphing_data = graphing_data1 + graphing_data2

# TODO: set graph width and height
sns.set_theme(rc={'figure.figsize': (15, 8.27)})
swarm = sns.swarmplot(data=all_graphing_data, orient='v', zorder=10, size=2.3)
# TODO: set graph and axes titles
swarm.set(xlabel='Strain', ylabel='Cell Size (microns^2)', title="Cell Sizes", )
# TODO: change xtick names here
swarm.set_xticks(range(len(all_graphing_data)), labels=["cn1a", "cn3a", "cn5a", "cn1b", "cn3b", "cn5b"])

sns.boxplot(showmeans=True,
            meanline=True,
            meanprops={'color': 'k', 'ls': '-', 'lw': 1},
            medianprops={'visible': False},
            whiskerprops={'visible': False},
            zorder=10,
            data=all_graphing_data,
            showfliers=False,
            showbox=False,
            showcaps=False,
            ax=swarm)

# plt.show()
plt.savefig(fname=output_path + "\\graph.pdf", dpi=1000)
