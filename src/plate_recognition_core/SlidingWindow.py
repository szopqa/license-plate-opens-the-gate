class SlidingWindow():

  def __init__(
    self,
    window_width, 
    window_height, 
    x_step_size, 
    y_step_size,
    start_point_x = 0, 
    start_point_y = 0
  ):
    self.__window_width = window_width
    self.__window_height = window_height 
    self.__x_step_size = x_step_size
    self.__y_step_size = y_step_size
    self.__start_point_x = start_point_x
    self.__start_point_y = start_point_y

  def __get_image_size(self, image):
    width = image.shape[1]
    height = image.shape[0]
    return ( width, height )

  def slide(self, image):

    im_width, im_height = self.__get_image_size(image)
    
    window_max_x_position = int(im_width - self.__window_width)
    window_max_y_position = int(im_height - self.__window_height)

    print(f'DEBUG: Initialized sliding window which will slide from {(self.__start_point_x,self.__start_point_y)}' + 
      f'to {(window_max_x_position, window_max_y_position)} with steps: x step = {self.__x_step_size}, y step = {self.__y_step_size}')
    print(f'DEBUG: Window dimensions: {self.__window_width} by {self.__window_height}')

    # slides a window across the image
    for y in range(self.__start_point_y, window_max_y_position, self.__y_step_size):
      for x in range(self.__start_point_x, window_max_x_position, self.__x_step_size):
        # print(f'sliding: x: {x} y: {y}')
        yield (x, y, image[y:y + self.__window_height, x:x + self.__window_width])



