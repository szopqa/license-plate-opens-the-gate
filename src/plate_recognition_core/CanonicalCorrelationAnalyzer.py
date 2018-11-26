from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image

import os

class CanonicalCorrelationAnalyzer():
  """
  binary_image: Image; Binary image read
  licensePlateValidator: LicensePlateValidator; LicensePlateValidator object
  """
  def __init__(self, binary_image, licensePlateValidator, min_region_area_as_percentage = 0.1, max_region_area_as_percentage = 5):
    self.__licensePlateValidator = licensePlateValidator
    self.__binary_image = binary_image
    self.__labeled_image = measure.label(self.__binary_image, return_num = False, connectivity = 2)

    self.__binary_image_height, self.__binary_image_width = Image.fromarray(binary_image).size;
    self.__binary_image_area = self.__binary_image_height * self.__binary_image_width
    print(f'DEBUG: Image height: {self.__binary_image_height}, width: {self.__binary_image_width}, size: {self.__binary_image_area}')

    self.__min_region_area = self.__calculate_min_area(min_region_area_as_percentage)
    self.__max_region_area = self.__calculate_max_area(max_region_area_as_percentage)
    
    self.__plate_like_objects_coordinates = []


  @property
  def plate_like_objects_coordinates(self):
    return self.__plate_like_objects_coordinates

  def __calculate_min_area(self, min_region_area_as_percentage):
    min_area = float(min_region_area_as_percentage / 100) * self.__binary_image_area
    print(f'Min region area: {min_area}')
    return min_area

  def __calculate_max_area(self, max_region_area_as_percentage):
    max_area = float(max_region_area_as_percentage / 100) * self.__binary_image_area
    print(f'Max region area: {max_area}')
    return max_area

  def __is_region_area_invalid(self, region_area):
    return region_area < self.__min_region_area or region_area > self.__max_region_area

  def __show_with_rectangles(self):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    for plate_like_object in self.__plate_like_objects_coordinates:
      min_row = plate_like_object.get("min_row")
      min_col = plate_like_object.get("min_col")
      max_row = plate_like_object.get("max_row")
      max_col = plate_like_object.get("max_col")
      
      region_width = max_col - min_col
      region_height = max_row - min_row

      rectBorder = patches.Rectangle((min_col, min_row), region_width, region_height, edgecolor="red", linewidth=2, fill=False)
      ax1.add_patch(rectBorder)

    ax1.imshow(self.__binary_image, cmap="gray")
    ax2.imshow(self.__labeled_image)
    plt.show()

  """
  Returns frame coordinates which fulfills license plate conditions
  """
  def find_plate_like_objects_coordinates(self):

    found_regions = regionprops(self.__labeled_image)
    for each_region in found_regions:

      if self.__is_region_area_invalid(each_region.area):
        continue

      min_row, min_col, max_row, max_col = each_region.bbox
      
      region_width = max_col - min_col
      region_height = max_row - min_row

      if self.__licensePlateValidator.validate_region_width_and_height(region_width, region_height):
        self.__plate_like_objects_coordinates.append(
          dict(
            min_row = min_row, 
            max_row = max_row, 
            min_col = min_col, 
            max_col = max_col
          )
        )
          
    if 'DISP' in os.environ and self.__plate_like_objects_coordinates: 
      self.__show_with_rectangles()

    return self.__plate_like_objects_coordinates