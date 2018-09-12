import numpy as np
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.transform import resize
from PIL import Image
import numpy as np

class Reader():
  """
  reads the image in grayscale and thresholds the image
  image_location: str; full image directory path
  img_max_width: int; max_width of image, height will
  be calculated dynamically to keep same image ratio
  """
  def __init__(self, image_location, img_max_width=600):
    read_image = imread(image_location, as_grey=True)

    self._img_max_width = img_max_width
    self.full_car_image = self.read_and_resize_if_necessary(read_image)
    self.binary_image = self.threshold(self.full_car_image)

  def _resize_image(self, image_to_resize, ratio):
    width = self._img_max_width
    height = round(width / ratio)
    return resize(image_to_resize, (height, width))

  """
  uses the otsu threshold method to generate a binary image
  gray_image: 2D array: gray scale image to be thresholded
  Returns:
  2-D array of the binary image each pixel is either 1 or 0
  """
  def threshold(self, gray_image):
    thresholdValue = threshold_otsu(gray_image)
    return gray_image > thresholdValue

  """
  function is used to resize the image before further
  processing if the image is too big. The resize is done
  in such a way that the aspect ratio is still maintained
  image_to_resize: 2D-Array of the image to be resized
  Returns:
  resized image or the original image if resize is not
  necessary
  """
  def read_and_resize_if_necessary(self, image_to_resize):
    height, width = image_to_resize.shape
    ratio = float(width / height)

    if width > self._img_max_width:
        return self._resize_image(image_to_resize, ratio)

    return image_to_resize

  """
  function is used to resize binary image
  Returns:
  resized image or the original image if resize is not
  necessary
  """
  def get_binary_resized(self, resize_ratio):
    gray_car_image = Image.fromarray(self.full_car_image)
    nx, ny = gray_car_image.size
    gray_car_image_resized = gray_car_image.resize((int(nx*resize_ratio), int(ny*resize_ratio)), Image.BICUBIC)
    return self.threshold(np.asarray(gray_car_image_resized))

