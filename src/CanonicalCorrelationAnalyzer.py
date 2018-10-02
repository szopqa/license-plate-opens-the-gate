from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import os

class CanonicalCorrelationAnalyzer():
  """
  binary_image: Image; Binary image read
  licensePlateValidator: LicensePlateValidator; LicensePlateValidator object
  """
  def __init__(self, binary_image, licensePlateValidator):
    self.__licensePlateValidator = licensePlateValidator
    self.__binary_image = binary_image
    (
      self.__labeled_image, 
      num_of_labels
    ) = measure.label(self.__binary_image, return_num=True, connectivity=2)
    print(f'DEBUG: Found {num_of_labels} labels in current image')

    self._plate_like_objects = []

  @property
  def plate_like_objects(self):
    return self._plate_like_objects

  def find_plate_like_objects(self):
    for each_region in regionprops(self.__labeled_image):
      
      # TODO: Add more accurate method of ignoring small regions
      if each_region.area < 100:
          continue

      min_row, min_col, max_row, max_col = each_region.bbox
      
      region_width = max_col - min_col
      region_height = max_row - min_row

      if self.__licensePlateValidator.validate_width_and_height(region_width, region_height):
        self._plate_like_objects.append(self.__binary_image[min_row:max_row, min_col:max_col])
          
        # TODO: Move plotting to separate class
        if 'DISP' in os.environ: 
          fig, (ax1, ax2) = plt.subplots(1, 2)
          rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
          ax1.add_patch(rectBorder)

          ax1.imshow(self.__binary_image, cmap="gray")
          ax2.imshow(self.__labeled_image)
          
          plt.show()