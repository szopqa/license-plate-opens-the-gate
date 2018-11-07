from CharactersSegmentator import CharactersSegmentator
from CharactersModel import CharactersModel
from Reader import Reader
from ImageDisplay import ImageDisplay
from Predictor import Predictor
from ImageSaver import ImageSaver
from ModelMapper import ModelMapper

reader = Reader('../output_images/2018-10-17T19:25:41_1.png')
# reader = Reader('../output_images/2018-11-03T15:58:28_2.png')

segmentator = CharactersSegmentator(CharactersModel())

license_plate = reader.get_binary()

characters_matrix = segmentator.get_characters_from_license_plate(license_plate)

saver = ImageSaver('../characters')
model_mapper = ModelMapper()

predictor = Predictor(model_mapper)
predictor.clasify_characters(characters_matrix)
characters = predictor.get_classified_characters()

print(characters)

# for each_character_matrix in characters_matrix :
  # saver.save_as_train_data(each_character_matrix, model_mapper.train_image_width, model_mapper.train_image_height)