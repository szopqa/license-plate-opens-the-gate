import os
import numpy as np
from skimage import measure
from skimage.measure import regionprops
from skimage.transform import resize

import matplotlib.patches as patches
import matplotlib.pyplot as plt



# TODO: Add some more 'space' to found characters in order to make it easier to clasify characters


class CharactersSegmentator (): 

  def __init__(self, characters_validator, character_width = 20, character_height = 20):
    self.__characters_validator = characters_validator
    self.__character_width = character_width
    self.__character_height = character_height

    self.__characters_found = []
    self.__coordinates_of_characters_found = []

  def __label_license_plate (self, license_plate):
    return measure.label(license_plate, connectivity = 2)

  def __show_with_rectangles(self, license_plate, labelled_plate):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    for each_character_coordinate in self.__coordinates_of_characters_found:
      (min_row, min_col, max_row, max_col) = each_character_coordinate
      
      region_width = max_col - min_col
      region_height = max_row - min_row

      rectBorder = patches.Rectangle((min_col, min_row), region_width, region_height, edgecolor="red", linewidth=2, fill=False)
      ax2.add_patch(rectBorder)

    ax1.imshow(labelled_plate, cmap="gray")
    ax2.imshow(license_plate, cmap="gray")
    plt.show()

  def __get_margins(self, diff):
    if diff % 2 == 0:
      left_margin = int(diff / 2)
      right_margin = int(diff / 2)
      return (left_margin, right_margin)
    else:
      left_margin = int(diff / 2)
      right_margin = int(diff / 2) + 1
      return (left_margin, right_margin)


  # TODO: Current solution seems to be way to much complicated. Idea is to fill images with white pixels
  """
  Model was trained on 20x20 images, so characters with different size
  have to be resized
  """
  def __resize_to_match_model(self, license_plate, min_row, max_row, min_col, max_col):
    current_width = max_col - min_col
    current_height = max_row - min_row

    print(f'current_width: {current_width}')
    print(f'current_height: {current_height}')

    if current_width > self.__character_width and current_height > self.__character_height:
      return resize(license_plate[min_row :max_row, min_col:max_col], (self.__character_width, self.__character_height))

    if current_width < self.__character_width:
      diff = self.__character_width - current_width
      left_margin, right_margin = self.__get_margins(diff)
      min_col -= left_margin
      max_col += right_margin
    
    if current_height < self.__character_height:
      diff = self.__character_height - current_height
      top_margin, bottom_margin = self.__get_margins(diff)   
      min_row -= top_margin
      max_row += bottom_margin
    
    
    current_width = max_col - min_col
    current_height = max_row - min_row

    print(f'Modified current_width: {current_width}')
    print(f'Modified current_height: {current_height}')

    return license_plate[min_row :max_row, min_col:max_col]

  def get_characters_from_license_plate(self, license_plate):
    (
      min_height, 
      max_height, 
      min_width, 
      max_width 
    ) = self.__characters_validator.get_characters_dimensions(license_plate)
    
    license_plate = np.invert(license_plate)
    
    print(f'DEBUG: License plate characters width should be from { min_width } to { max_width }')
    print(f'DEBUG: License plate characters height should be from { min_height } to { max_height }')

    labelled_plate = self.__label_license_plate(license_plate)

    for each_region in regionprops(labelled_plate):
      
      min_row, min_col, max_row, max_col = each_region.bbox
      
      region_width = max_col - min_col
      region_height = max_row - min_row

      if region_width >= region_height:
        continue


      print(f'DEBUG: Analyzing region\'s width: { region_width }, height { region_height }')


      if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
        self.__characters_found.append(license_plate[min_row :max_row, min_col:max_col])
        self.__coordinates_of_characters_found.append((min_row, min_col, max_row, max_col))
      
    if 'DISP' in os.environ and self.__characters_found: 
      self.__show_with_rectangles(license_plate, labelled_plate)

    return self.__characters_found