class LicensePlateValidator():
  
  # Info based on wikipedia article (https://pl.wikipedia.org/wiki/Tablice_rejestracyjne_w_Polsce)
  # 
  # A plate is considered present if and only if:
  #  * Width to height ratio is between real license plate ratio +/- allowed mistake
  #  * TODO: The plate falls entirely within the image bounds.
  #  * TODO: The plate’s width is less than 80% of the image’s width, and the plate’s height is less than 87.5% of the image’s height.
  #  * TODO: The plate’s width is greater than 60% of the image’s width or the plate’s height is greater than 60% of the image’s height.

  def __init__(self, real_l_p_width = 520, real_l_p_height = 114, allowed_mistake = 0.1):
    self.__real_l_p_width = real_l_p_width
    self.__real_l_p_height = real_l_p_height
    self.__real_l_p_width_to_height_ratio = float(self.__real_l_p_width / self.__real_l_p_height)

    self.set_allowed_mistake(allowed_mistake)

    self.__min_allowed_ratio = float(self.__real_l_p_width_to_height_ratio - self.__allowed_deviation)
    self.__max_allowed_ratio = float(self.__real_l_p_width_to_height_ratio + self.__allowed_deviation)


  """
  sets mistake allowed in width to height ratio calculation
  during classification of license plate like objects
  new_allowed_mistake: float; number in range of <0; 1). Default set to 0.05
  """
  def set_allowed_mistake(self, new_allowed_mistake):
    if new_allowed_mistake < 0 or new_allowed_mistake >= 1:
      raise ValueError(f'Expected new_allowed_mistake value to be in range of <0; 1) but got {new_allowed_mistake}')
    self.__allowed_mistake = new_allowed_mistake
    self.__allowed_deviation = self.__allowed_mistake * self.__real_l_p_width_to_height_ratio

  """
  Checks if plate like objects width to height ratio is between
  real license plate ratio +/- allowed mistake
  """
  def validate_width_and_height(self, region_width, region_height):    
    region_width_to_height_ratio = float(region_width / region_height)

    print(f'DEBUG: Checking if: {region_width_to_height_ratio} is between {self.__min_allowed_ratio} and {self.__max_allowed_ratio}')

    width_to_height_ratio_condition = region_width_to_height_ratio >= self.__min_allowed_ratio and region_width_to_height_ratio <= self.__max_allowed_ratio
    width_and_height_values_condition = region_width >= region_height

    all_conditions_fulfilled = width_to_height_ratio_condition and width_and_height_values_condition

    return all_conditions_fulfilled