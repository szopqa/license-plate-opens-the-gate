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
from CharactersModel import CharactersModel
from ModelMapper import ModelMapper
from Predictor import Predictor

reader = Reader('../input_images/car2.jpg')
binary_image = reader.get_binary()
ImageDisplay.show_image(binary_image)

# saver = ImageSaver()

binary_image_resized = reader.get_binary_resized(1)
license_plate_validator = LicensePlateValidator(allowed_mistake_on_ratio=0.3)
cca = CanonicalCorrelationAnalyzer(binary_image_resized, license_plate_validator)

plate_like_objects_coordinates = cca.find_plate_like_objects_coordinates()
plate_like_object_images = ResizedToOriginalMapper(binary_image).get_plate_like_objects_by_coordinates(plate_like_objects_coordinates)

valid_plate_like_object_images = list(filter(license_plate_validator.validate_plate_like_objects, plate_like_object_images))

model_mapper = ModelMapper()
segmentator = CharactersSegmentator(CharactersModel())

predictor = Predictor(model_mapper)


for each_plate_like_object_image in valid_plate_like_object_images:
  ImageDisplay.show_image(each_plate_like_object_image)
  
  characters_matrix = segmentator.get_characters_from_license_plate(each_plate_like_object_image)
  predictor.clasify_characters(characters_matrix)
  characters = predictor.get_classified_characters()
  print(characters)
  