import matplotlib.pyplot as plt
from skimage.io import imread
from skimage import data
from skimage.filters import try_all_threshold

img = imread('../input_images/car2.jpg', as_grey=True)

fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
plt.show()