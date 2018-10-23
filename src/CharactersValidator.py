class CharactersValidator(): 

  def __init__(
    self, 
    char_height_as_percentage_of_plate_min = 55, 
    char_height_as_percentage_of_plate_max = 90, 
    char_width_as_percentage_of_plate_min = 5,
    char_width_as_percentage_of_plate_max = 15
    ):
    self.__char_height_as_percentage_of_plate_min = char_height_as_percentage_of_plate_min / 100
    self.__char_height_as_percentage_of_plate_max = char_height_as_percentage_of_plate_max / 100
    self.__char_width_as_percentage_of_plate_min = char_width_as_percentage_of_plate_min / 100
    self.__char_width_as_percentage_of_plate_max = char_width_as_percentage_of_plate_max / 100

  """
  assumptions that the width of single character
  should be between 5% and 15% of the license plate,
  and height should be between 55% and 80%
  """
  def get_characters_dimensions(self, license_plate):
    return (
      self.__char_height_as_percentage_of_plate_min * license_plate.shape[0], 
      self.__char_height_as_percentage_of_plate_max * license_plate.shape[0], 
      self.__char_width_as_percentage_of_plate_min * license_plate.shape[1], 
      self.__char_width_as_percentage_of_plate_max * license_plate.shape[1]
    )