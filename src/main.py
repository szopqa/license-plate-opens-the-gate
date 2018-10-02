import os
import matplotlib.pyplot as plt
from skimage.morphology import opening, square, closing

from Reader import Reader
from LicensePlateValidator import LicensePlateValidator 
from CanonicalCorrelationAnalyzer import CanonicalCorrelationAnalyzer
from ImageDisplay import ImageDisplay

reader = Reader('../input_images/car2.jpg')
binary_image = reader.get_binary_resized(1)

cca = CanonicalCorrelationAnalyzer(binary_image, LicensePlateValidator(allowed_mistake = 0.2))

cca.find_plate_like_objects()

print(cca.plate_like_objects)

for plate_like_object in cca.plate_like_objects:
  ImageDisplay.show_image(plate_like_object)
