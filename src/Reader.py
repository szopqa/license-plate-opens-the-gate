import numpy as np
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.transform import resize
from PIL import Image

class Reader():
  """
  image_location: str; full image directory path
  img_max_width: int; max_width of image, height will
  be calculated dynamically to keep same image ratio
  """
  def __init__(self, image_location, img_max_width=600):
    read_image = imread(image_location, as_gray=True)

    self._img_max_width = img_max_width
    self.__car_image_grayscaled = self.__read_and_resize_if_necessary(read_image)

  def __resize_image(self, image_to_resize, ratio):
    width = self._img_max_width
    height = round(width / ratio)
    return resize(image_to_resize, (height, width))

  """
  function is used to resize the image before further
  processing if the image is too big
  """
  def __read_and_resize_if_necessary(self, image_to_resize):
    height, width = image_to_resize.shape
    ratio = float(width / height)

    if width > self._img_max_width:
        return self.__resize_image(image_to_resize, ratio)

    return image_to_resize

  """
  uses the otsu threshold method to generate a binary image
  """
  def __threshold(self, gray_image):
    thresholdValue = threshold_otsu(gray_image)
    binary = gray_image > thresholdValue
    return binary.astype('uint8') * 255

  """
  Returns binary image resized by given ratio
  """
  def get_binary_resized(self, resize_ratio):
    gray_car_image = Image.fromarray(self.__car_image_grayscaled)
    nx, ny = gray_car_image.size
    gray_car_image_resized = gray_car_image.resize((int(nx*resize_ratio), int(ny*resize_ratio)), Image.BICUBIC)
    return self.__threshold(np.asarray(gray_car_image_resized))
  
  """
  Returns binary image resized to given size
  """
  def get_binary_fixed_resize(self, width, height):
    gray_car_image = Image.fromarray(self.__car_image_grayscaled)
    nx, ny = gray_car_image.size
    gray_car_image_resized = gray_car_image.resize((width, height), Image.BICUBIC)
    return self.__threshold(np.asarray(gray_car_image_resized))

  """
  Returns binary image
  """
  def get_binary(self):
    return self.__threshold(self.__car_image_grayscaled)

  """
  Returns greyscaled image
  """
  def get_grayscaled(self):
    return self.__car_image_grayscaled