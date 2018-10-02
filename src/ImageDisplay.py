from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class ImageDisplay():

  @staticmethod
  def show_image(image_matrix):
    print(f'Image width: {image_matrix.shape[0]}')
    print(f'Image height: {image_matrix.shape[1]}')
    img = Image.fromarray(image_matrix, mode='L')
    img.show()
  
