import os
import matplotlib.pyplot as plt
from skimage.morphology import opening, square, closing

from Reader import Reader
from LicensePlateValidator import LicensePlateValidator 
from CanonicalCorrelationAnalyzer import CanonicalCorrelationAnalyzer
from ImageDisplay import ImageDisplay
from ImageSaver import ImageSaver
from ResizedToOriginalMapper import ResizedToOriginalMapper
from CharactersSegmentator import CharactersSegmentator
from CharactersValidator import CharactersValidator

reader = Reader('../input_images/car3.jpg')
saver = ImageSaver();

binary_image = reader.get_binary()
binary_image_resized = reader.get_binary_resized(1)

cca = CanonicalCorrelationAnalyzer(binary_image_resized, LicensePlateValidator(allowed_mistake = 0.3))

plate_like_objects_coordinates = cca.find_plate_like_objects_coordinates()


images = ResizedToOriginalMapper(binary_image).get_plate_like_objects_by_coordinates(plate_like_objects_coordinates);

segmentator = CharactersSegmentator(CharactersValidator())

for plate_like_object_image in images:
  print(plate_like_object_image.shape)
  segmentator.get_characters_from_license_plate(plate_like_object_image)
  ImageDisplay.show_image(plate_like_object_image)
  ImageDisplay.show_filtered_image(plate_like_object_image)
  saver.save(plate_like_object_image)