import os
from PIL import Image
import numpy as np
import json

def count_in_all_images(image_dir):
  processed = []
  for each_license_plate in os.listdir(f'{image_dir}'):
    processed.append(count_white(f'{image_dir}/{each_license_plate}'))
  return processed

def count_white(image_path):
  img = Image.open(image_path)
  whites = 0
  blacks = 0

  for y in range(img.height):
    for x in range(img.width):
      pixel = img.getpixel((x, y))
      if(pixel == 255):
        blacks += 1
      else:
        whites += 1

  return (
    image_path,
    blacks,
    whites
  )

def calculate_white_as_percentage(each_result):
  image_path, blacks, whites = each_result
  total = blacks + whites
  whites_percentage = float(whites/total) * 100
  print (f'DEBUG: Analyzing image : {image_path}: white pixels are {whites_percentage} % of total')

  return whites_percentage


# # # # # # # # # # # # 
#         Main        #
# # # # # # # # # # # # 

# reading and analyzing license plates
image_dir = './license_plates'
results = count_in_all_images(image_dir)

# calculating white pixels as percentage of all existing in license plate
white_percentages = list(map(calculate_white_as_percentage, results))

# saving min, max and median of whites percentage
license_plate_analyze_results = dict([
  ("min_whites_total", np.min(white_percentages)),
  ("max_whites_total", np.max(white_percentages)),
  ("median_whites_total", np.median(white_percentages))
])

# saving results to file
results_json_path = './results.json'
with open(results_json_path, 'w') as res_json:
  json.dump(license_plate_analyze_results, res_json)
