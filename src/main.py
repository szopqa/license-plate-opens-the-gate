import os
import matplotlib.pyplot as plt
from skimage.morphology import opening, square, closing

from Reader import Reader
from LicensePlateValidator import LicensePlateValidator 
from CanonicalCorrelationAnalyzer import CanonicalCorrelationAnalyzer

reader = Reader('../input_images/car3.jpg')

licensePlateValidator = LicensePlateValidator()
cca = CanonicalCorrelationAnalyzer(reader, licensePlateValidator)

cca.get_plate_like_objects()

print(cca.plate_like_objects)

# In order to see the output of script run it with DISP_GRAY=1 environment variable
if 'DISP_GRAY' in os.environ: 
  fig, (ax1, ax2) = plt.subplots(1,2)

  ax1.imshow(closing(reader.full_car_image, square(3)), cmap="gray")
  # ax1.imshow(image_grayscaled, cmap="gray")
  ax2.imshow(reader.binary_image, cmap="gray")
  
  plt.show()