import os
import numpy as np
from skimage import measure
from skimage.measure import regionprops
from skimage.transform import resize

import matplotlib.patches as patches
import matplotlib.pyplot as plt



# TODO: Add some more 'space' to found characters in order to make it easier to clasify characters


class CharactersSegmentator (): 

  def __init__(self, characters_validator):
    self.__characters_validator = characters_validator
    self.__coordinates_of_characters_found = []
    self.__characters_found = []

  def __label_license_plate (self, license_plate):
    return measure.label(license_plate, connectivity = 2)

  def __show_with_rectangles(self, license_plate):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    for each_character_coordinate in self.__coordinates_of_characters_found:
      (min_row, min_col, max_row, max_col) = each_character_coordinate
      
      region_width = max_col - min_col
      region_height = max_row - min_row

      rectBorder = patches.Rectangle((min_col, min_row), region_width, region_height, edgecolor="red", linewidth=2, fill=False)
      ax2.add_patch(rectBorder)

    ax1.imshow(license_plate, cmap="gray")
    ax2.imshow(license_plate, cmap="gray")
    plt.show()


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

    min_region_area = min_height * min_width
    max_region_area = max_height * max_width

    labelled_plate = self.__label_license_plate(license_plate)

    for each_region in regionprops(labelled_plate):
      
      min_row, min_col, max_row, max_col = each_region.bbox
      
      region_width = max_col - min_col
      region_height = max_row - min_row

      if region_width >= region_height:
        continue


      print(f'DEBUG: Analyzing region\'s width: { region_width }, height { region_height }')


      if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
        self.__coordinates_of_characters_found.append((min_row, min_col, max_row, max_col))
        character = license_plate[min_row :max_row, min_col:max_col]

        # resizing characters to 20X20 and then appending each character into the characters list
        self.__characters_found.append(resize(character, (20, 20)))
      

      # this is just to keep track of the arrangement of the characters
      # column_list.append(x0)

    if 'DISP' in os.environ and self.__coordinates_of_characters_found: 
      self.__show_with_rectangles(license_plate)