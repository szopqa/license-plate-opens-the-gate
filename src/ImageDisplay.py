from PIL import Image, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import cv2

class ImageDisplay():

  @staticmethod
  def show_image(image_matrix):
    print(f'Image height: {image_matrix.shape[0]}')
    print(f'Image width: {image_matrix.shape[1]}')
    img = Image.fromarray(image_matrix, mode='L')
    img.show()

  @staticmethod
  def show_filtered_image(image_matrix):
    img = Image.fromarray(image_matrix, mode='L')
    filtered = img.filter(ImageFilter.MedianFilter())
    filtered.show()
  
  @staticmethod
  def show_with_rectangle(x, y, window_width, window_height, image):
    clone = image.copy()
    cv2.rectangle(clone, (x, y), (x + window_width, y + window_height), (0, 0, 0), 2)
    cv2.imshow("Sliding Window - License Plate Opens The Gate", clone)
    cv2.waitKey(1)