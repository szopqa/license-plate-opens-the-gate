class LicensePlateValidator():
  
  # Info based on wikipedia article (https://pl.wikipedia.org/wiki/Tablice_rejestracyjne_w_Polsce)
  def __init__(self, real_l_p_width = 520, real_l_p_height = 114, allowed_mistake = 0.17):
    self._real_l_p_width = real_l_p_width
    self._real_l_p_height = real_l_p_height
    self._real_l_p_width_to_height_ratio = float(self._real_l_p_width / self._real_l_p_height)

    self.set_allowed_mistake(allowed_mistake)

  """
  sets mistake allowed in width to height ratio calculation
  during clasification of license plate like objects
  new_allowed_mistake: float; number in range of <0; 1). Default set to 0.05
  """
  def set_allowed_mistake(self, new_allowed_mistake):
    if new_allowed_mistake < 0 or new_allowed_mistake >= 1:
      raise ValueError(f'Expected new_allowed_mistake value to be in range of <0; 1) but got {new_allowed_mistake}')
    self._allowed_mistake = new_allowed_mistake
    self._allowed_deviation = self._allowed_mistake * self._real_l_p_width_to_height_ratio

  """
  Checks if plate like objects width to height ratio is between
  real license plate ratio +/- allowed mistake
  """
  def validate_width_and_height(self, region_width, region_height):
    min_allowed_ratio = float(self._real_l_p_width_to_height_ratio - self._allowed_deviation)
    max_allowed_ratio = float(self._real_l_p_width_to_height_ratio + self._allowed_deviation)
    
    region_width_to_height_ratio = float(region_width / region_height)

    print(f'DEBUG: Ratio: {region_width_to_height_ratio} should be between {min_allowed_ratio} and {max_allowed_ratio}')
    return region_width_to_height_ratio >= min_allowed_ratio and region_width_to_height_ratio <= max_allowed_ratio



# LPV = LicensePlateValidator()

# result = LPV.validate_width_and_height(4.7,1)
# print(result)
# LPV.set_allowed_mistake(0.1)
# result2 = LPV.validate_width_and_height(4.8,1)
# print(result2)
