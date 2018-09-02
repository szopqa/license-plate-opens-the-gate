from skimage import measure
from skimage.measure import regionprops

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import greyscale
import numpy as np
import os

# Labeling connected regions
label_image, num_of_labels = measure.label(greyscale.binary_car_image, return_num=True, connectivity=2)
print(f'Found {num_of_labels} labels in current image')

print(f'Image width: {greyscale.binary_car_image.shape[0]}')
print(f'Image height: {greyscale.binary_car_image.shape[1]}')

plate_dimensions = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions

plate_objects_cordinates = []
plate_like_objects = []

fig, (ax1, ax2) = plt.subplots(1, 2)

# regionprops creates a list of properties of all the labelled regions
for region in regionprops(label_image):
    if region.area < 50:
        continue

    min_row, min_col, max_row, max_col = region.bbox
    region_height = max_row - min_row
    region_width = max_col - min_col

    rect_border_all = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="yellow", linewidth=2, fill=False)
    ax1.add_patch(rect_border_all)
    
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        plate_like_objects.append(greyscale.binary_car_image[min_row:max_row, min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col, max_row, max_col))

        rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rectBorder)

# In order to see the output of script run it with DISP_CCA=2 environment variable
if 'DISP_CCA' in os.environ:
    ax1.imshow(label_image)
    ax2.imshow(greyscale.gray_car_image_resized, cmap="gray")
  
    plt.show()