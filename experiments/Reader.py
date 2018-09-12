import numpy as np
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.transform import resize

class Reader():

  def __init__(self, image_location, img_max_width=600):
    """
    reads the image in grayscale and thresholds the image
    image_location: str; full image directory path
    img_max_width: int; max_width of image, height will 
    be calculated dynamically to keep same image ratio
    """
    read_image = imread(image_location, as_grey=True)

    self.__img_max_width = img_max_width
    self.full_car_image = self.read_and_resize_if_necessary(read_image)
    self.binary_image = self.threshold(self.full_car_image)

  def __resize_image(self, image_to_resize, ratio):
    width = self.__img_max_width
    height = round(width / ratio)
    return resize(image_to_resize, (height, width))

  def threshold(self, gray_image):
    """
    uses the otsu threshold method to generate a binary image

    Parameters:
    -----------
    gray_image: 2D array: gray scale image to be thresholded

    Return:
    --------
    2-D array of the binary image each pixel is either 1 or 0
    """
    thresholdValue = threshold_otsu(gray_image)
    return gray_image > thresholdValue

  def read_and_resize_if_necessary(self, image_to_resize):
      """
      function is used to resize the image before further
      processing if the image is too big. The resize is done
      in such a way that the aspect ratio is still maintained

      Parameters:
      ------------
      image_to_resize: 2D-Array of the image to be resized

      Return:
      --------
      resized image or the original image if resize is not
      necessary
      """
      height, width = image_to_resize.shape
      ratio = float(width / height)

      if width > self.__img_max_width:
        return self.__resize_image(image_to_resize, ratio)
      
      return image_to_resize