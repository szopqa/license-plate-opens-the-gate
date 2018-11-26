from plate_recognition_core.CharactersSegmentator import CharactersSegmentator
from plate_recognition_core.CharactersModel import CharactersModel
from plate_recognition_core.Reader import Reader
from plate_recognition_core.ImageDisplay import ImageDisplay
from plate_recognition_core.Predictor import Predictor
from plate_recognition_core.ImageSaver import ImageSaver
from plate_recognition_core.ModelMapper import ModelMapper

reader = Reader('./data_utils/license_plates/DLU64819.png')

segmentator = CharactersSegmentator(CharactersModel())

license_plate = reader.get_binary()

characters_matrix = segmentator.get_characters_from_license_plate(license_plate)

saver = ImageSaver('../characters')
model_mapper = ModelMapper(invert_image_colours=True)

predictor = Predictor(model_mapper)
predictor.clasify_characters(characters_matrix)
characters = predictor.get_classified_characters()

print(characters)

for each_character_matrix in characters_matrix :
  saver.save_as_train_data(each_character_matrix, model_mapper.train_image_width, model_mapper.train_image_height)