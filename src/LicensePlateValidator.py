import json
from PIL import Image

class LicensePlateValidator():
  
  # Info based on wikipedia article (https://pl.wikipedia.org/wiki/Tablice_rejestracyjne_w_Polsce)
  # 
  # A plate is considered present if and only if:
  #  * Width to height ratio is between real license plate ratio +/- allowed mistake
  #  * Plate lite object has white to black pixels ratio as analyzed license plates
  #  * TODO: The plate falls entirely within the image bounds.
  #  * TODO: The plate’s width is less than 80% of the image’s width, and the plate’s height is less than 87.5% of the image’s height.
  #  * TODO: The plate’s width is greater than 60% of the image’s width or the plate’s height is greater than 60% of the image’s height.

  def __init__(
    self, 
    real_l_p_width = 520, 
    real_l_p_height = 114, 
    allowed_mistake_on_ratio = 0.1,
    allowed_mistake_on_whites_to_black = 0.1,
    white_to_black_results_path = './data_utils/results.json'
  ):
    self.__real_l_p_width = real_l_p_width
    self.__real_l_p_height = real_l_p_height
    self.__real_l_p_width_to_height_ratio = float(self.__real_l_p_width / self.__real_l_p_height)

    self.__load_and_set_white_to_black_ratio(white_to_black_results_path, allowed_mistake_on_whites_to_black)
    self.set_allowed_mistake_on_ratio(allowed_mistake_on_ratio)

    self.__min_allowed_ratio = float(self.__real_l_p_width_to_height_ratio - self.__allowed_deviation)
    self.__max_allowed_ratio = float(self.__real_l_p_width_to_height_ratio + self.__allowed_deviation)

  """
  loads results of white to black pixels ratio in existing license plates
  saved as json file
  """
  def __load_and_set_white_to_black_ratio(self, white_to_black_results_path, allowed_mistake):
    with open(white_to_black_results_path, 'r') as results_json_file:
      results = json.load(results_json_file)
      self.__min_whites_total = float(results["min_whites_total"] - results["min_whites_total"] * allowed_mistake)
      self.__max_whites_total = float(results["max_whites_total"] + results["max_whites_total"] * allowed_mistake)

  """
  validates if license plate has valid white to black pixels ratio
  """
  def __validate_white_to_black_pixels_ration(self, plate_like_object):
    image = Image.fromarray(plate_like_object, mode = 'L')

    whites = 0
    blacks = 0

    for y in range(image.height):
      for x in range(image.width):
        pixel = image.getpixel((x, y))
        if(pixel == 255):
          blacks += 1
        else:
          whites += 1

    total = whites + blacks
    white_as_percentage = float(whites/total) * 100

    min_ratio = self.__min_whites_total
    max_ratio = self.__max_whites_total
    print(f'DEBUG: Analyzing white to black ratio: {white_as_percentage} should be between <{min_ratio},{max_ratio}>')

    return white_as_percentage >= min_ratio and white_as_percentage <= max_ratio

  """
  sets mistake allowed in width to height ratio calculation
  during classification of license plate like objects
  new_allowed_mistake: float; number in range of <0; 1). Default set to 0.05
  """
  def set_allowed_mistake_on_ratio(self, new_allowed_mistake):
    if new_allowed_mistake < 0 or new_allowed_mistake >= 1:
      raise ValueError(f'Expected new_allowed_mistake value to be in range of <0; 1) but got {new_allowed_mistake}')
    self.__allowed_mistake_on_ratio = new_allowed_mistake
    self.__allowed_deviation = self.__allowed_mistake_on_ratio * self.__real_l_p_width_to_height_ratio

  """
  Checks if plate like objects width to height ratio is between
  real license plate ratio +/- allowed mistake
  """
  def validate_region_width_and_height(self, region_width, region_height):    
    region_width_to_height_ratio = float(region_width / region_height)

    print(f'DEBUG: Checking if: {region_width_to_height_ratio} is between {self.__min_allowed_ratio} and {self.__max_allowed_ratio}')

    width_to_height_ratio_condition = region_width_to_height_ratio >= self.__min_allowed_ratio and region_width_to_height_ratio <= self.__max_allowed_ratio
    width_and_height_values_condition = region_width >= region_height

    all_conditions_fulfilled = width_to_height_ratio_condition and width_and_height_values_condition

    return all_conditions_fulfilled


  """
  simple chain of responsibility implementation executing all validators on plate like images
  """
  def validate_plate_like_objects(self, plate_like_object):
    isValid = False

    # validating black to white pixels ratio
    isValid = self.__validate_white_to_black_pixels_ration(plate_like_object)


    return isValid
