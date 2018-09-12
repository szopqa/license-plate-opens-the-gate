import os
import matplotlib.pyplot as plt
from skimage.morphology import opening, square, closing

from Reader import Reader
from LicensePlateValidator import LicensePlateValidator 
from CanonicalCorrelationAnalyzer import CanonicalCorrelationAnalyzer

reader = Reader('../input_images/car3.jpg')

image_grayscaled = reader.full_car_image
binary = reader.binary_image

licensePlateValidator = LicensePlateValidator()
cca = CanonicalCorrelationAnalyzer(binary, licensePlateValidator)

cca.get_plate_like_objects()

print(cca.plate_like_objects)

# In order to see the output of script run it with DISP_GRAY=1 environment variable
if 'DISP_GRAY' in os.environ: 
  fig, (ax1, ax2) = plt.subplots(1,2)

  ax1.imshow(closing(image_grayscaled, square(3)), cmap="gray")
  # ax1.imshow(image_grayscaled, cmap="gray")
  ax2.imshow(binary, cmap="gray")
  
  plt.show()