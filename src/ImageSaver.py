from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

class ImageSaver():

  imagesSaved = 0;

  def __init__(self, savedImagesDir='../output_images'): 
    self.__now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    self.__savedImagesDir = savedImagesDir

    if not os.path.exists(savedImagesDir):
      os.makedirs(savedImagesDir)

  def save(self, image_matrix):
    ImageSaver.imagesSaved += 1
    image_name = f'{self.__savedImagesDir}/{self.__now}_{ImageSaver.imagesSaved}.png';

    img = Image.fromarray(image_matrix, mode = 'L')
    img.save(image_name);
