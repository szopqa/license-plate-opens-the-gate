import time
from PIL import Image

import scipy.misc
import skimage
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

from plate_recognition_core.Reader import Reader
from plate_recognition_core.SlidingWindow import SlidingWindow
from plate_recognition_core.ImageDisplay import ImageDisplay
from plate_recognition_core.ImageSaver import ImageSaver
from plate_recognition_core.ModelMapper import ModelMapper
from plate_recognition_core.Predictor import Predictor

def show_with_rectangle(image, x, y, window_width, window_height):
  ImageDisplay.show_with_rectangle(x, y, window_width, window_height, image)

def run():
  for (x, y, each_image_frame) in window_slider.slide(binary_image):
    show_with_rectangle(binary_image, x, y, window_width, window_height)  
    
    resized = skimage.transform.resize(each_image_frame, (MODEL_HEIGHT, MODEL_WIDTH))
    saver.save_single_frame(resized)
    time.sleep(1 * 0.001 * 100)


MODEL_WIDTH = 128
MODEL_HEIGHT = 64
TRAINED_MODEL_PATH = './models/svc/svc2.pkl'

saver = ImageSaver('./out_image_frames')
reader = Reader('../input_images/car3.jpg')
binary_image = reader.get_grayscaled()

x = binary_image.shape[1]
y = binary_image.shape[0]

window_width = int(x/2)
window_height = int(y/4)

x_step_size = int(window_width / 4) - 1
y_step_size = int(window_height / 4) - 1

window_slider = SlidingWindow(
  window_width = window_width,
  window_height = window_height, 
  x_step_size = x_step_size, 
  y_step_size = y_step_size 
)

model_mapper = ModelMapper(MODEL_WIDTH, MODEL_HEIGHT)
predictor = Predictor(model_mapper, )

run()