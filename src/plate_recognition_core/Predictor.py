import os
from sklearn.externals import joblib

class Predictor():
  
  def __init__(self, model_mapper, model_path = '../models/svc/svc.pkl'):
    self.__model = self.__load_model(model_path)
    self.__model_mapper = model_mapper
    self.__classification_result = []
    self.__license_plate_characters = ''


  def __load_model(self, model_path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    model_dir = os.path.join(current_dir, model_path)  
    return joblib.load(model_dir)

  def clasify_characters(self, characters):
    for each_character in characters:
      each_character_resized = self.__model_mapper.resize_image_to_match_model(each_character).reshape(1, -1)
      result = self.__model.predict(each_character_resized)
      self.__classification_result.append(result)
    
  def get_classified_characters(self):
    for each_predict in self.__classification_result:
      self.__license_plate_characters += each_predict[0]
      
    return self.__license_plate_characters