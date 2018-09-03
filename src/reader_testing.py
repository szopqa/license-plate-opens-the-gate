import os
import matplotlib.pyplot as plt

from Reader import Reader

reader = Reader('../input_images/car2.jpg')

image_grayscaled = reader.full_car_image
binary = reader.binary_image

# In order to see the output of script run it with DISP_GRAY=1 environment variable
if 'DISP_GRAY' in os.environ: 
  fig, (ax1, ax2) = plt.subplots(1,2)

  ax1.imshow(image_grayscaled, cmap="gray")
  ax2.imshow(binary, cmap="gray")
  
  plt.show()