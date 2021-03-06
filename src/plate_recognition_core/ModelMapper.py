from PIL import Image
import numpy as np
from skimage.filters import threshold_otsu

class ModelMapper():
  def __init__(self, train_image_width = 20, train_image_height = 20, invert_image_colours = True):
    self.__train_image_width = train_image_width
    self.__train_image_height = train_image_height
    self.__invert_image_colours = invert_image_colours

  def __invert_colours_before_classification(self, image_as_matrix):
    image_as_matrix[image_as_matrix == 255] = 1
    image_as_matrix[image_as_matrix == 0] = 255
    image_as_matrix[image_as_matrix == 1] = 0

    return image_as_matrix

  def resize_image_to_match_model(self, image_as_matrix):
    if self.__invert_image_colours:
      image_as_matrix = self.__invert_colours_before_classification(image_as_matrix)
      
    img = Image.fromarray(image_as_matrix, mode = 'L')
    resized = img.resize((self.__train_image_width, self.__train_image_height), Image.ANTIALIAS)
    thresholdValue = threshold_otsu(np.array(resized))
    binary = np.array(resized) > thresholdValue
    return binary.astype('uint8') * 255

  @property
  def train_image_width(self):
    return self.__train_image_width

  @property
  def train_image_height(self):
    return self.__train_image_height