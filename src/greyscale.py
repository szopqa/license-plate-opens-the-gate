import os
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

RESIZE_RATIO = .8
INPUT_IMAGES_DIRECTORY = 'input_images'
SAMPLE_IMAGE = 'car3.jpg'

image_path = os.path.join(INPUT_IMAGES_DIRECTORY, SAMPLE_IMAGE)

# Reading image in greyscale and resizing it
gray_car_image = Image.fromarray(imread(image_path, as_gray=True) *  255)

nx, ny = gray_car_image.size
gray_car_image_resized = gray_car_image.resize((int(nx*RESIZE_RATIO), int(ny*RESIZE_RATIO)), Image.BICUBIC)

# Threshold calculation
threshold_value = threshold_otsu(np.asarray(gray_car_image_resized))

# Changing image to binary
binary_car_image = gray_car_image_resized > threshold_value

# In order to see the output of script run it with DISP_GRAY=1 environment variable
if 'DISP_GRAY' in os.environ:
  fig, (ax1, ax2) = plt.subplots(1, 2)

  ax1.imshow(gray_car_image_resized, cmap="gray")
  ax2.imshow(binary_car_image, cmap="gray")
  
  plt.show()