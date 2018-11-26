class ResizedToOriginalMapper():
  def __init__(self, original_binary_image):
    self.__original_binary_image = original_binary_image
    self.__plate_like_images_from_original = []

  """
  plate_like_objects_from_resized: Dictionary; containing 'min_row', 'min_col', 'max_row', 'max_col' keys
  """
  def get_plate_like_objects_by_coordinates(self, plate_like_objects_coordinates):
    for plate_like_object in plate_like_objects_coordinates:

      min_row = plate_like_object.get("min_row")
      min_col = plate_like_object.get("min_col")
      max_row = plate_like_object.get("max_row")
      max_col = plate_like_object.get("max_col")

      self.__plate_like_images_from_original.append(self.__original_binary_image[min_row:max_row, min_col:max_col])

    return self.__plate_like_images_from_original