from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import scipy.misc

class ImageSaver():

  imagesSaved = 0

  def __init__(self, savedImagesDir='../output_images'): 
    self.__now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    self.__savedImagesDir = savedImagesDir

    if not os.path.exists(savedImagesDir):
      os.makedirs(savedImagesDir)

  def __matrix_to_image(self, image_matrix):
    return Image.fromarray(image_matrix, mode = 'L')

  def __save(self, image, image_name):
    image.save(image_name)

  def __set_image_name(self):
    ImageSaver.imagesSaved += 1
    return f'{self.__savedImagesDir}/{self.__now}_{ImageSaver.imagesSaved}.png'

  def save(self, image_matrix):
    self.__save(self.__matrix_to_image(image_matrix), self.__set_image_name())

  def save_resized(self, image_matrix, width, height):    
    img = self.__matrix_to_image(image_matrix)
    resized = img.resize((width, height), Image.ANTIALIAS)
    self.__save(resized, self.__set_image_name())

  def save_as_train_data(self, image_matrix, width, height):
    self.__savedImagesDir = '../characters'

    # image_matrix[image_matrix == 255] = 1
    # image_matrix[image_matrix == 0] = 255
    # image_matrix[image_matrix == 1] = 0
    img = self.__matrix_to_image(image_matrix)
    resized = img.resize((width, height), Image.ANTIALIAS)
    self.__save(resized, self.__set_image_name())

  def save_single_frame(self, image_frame):
    scipy.misc.imsave(self.__set_image_name(), image_frame)