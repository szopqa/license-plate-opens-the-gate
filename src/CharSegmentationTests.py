from CharactersSegmentator import CharactersSegmentator
from CharactersValidator import CharactersValidator
from Reader import Reader
from ImageDisplay import ImageDisplay
from Predictor import Predictor
from ImageSaver import ImageSaver
from ModelMapper import ModelMapper

reader = Reader('../output_images/2018-10-17T19:26:16_2.png')
# reader = Reader('../output_images/2018-10-17T19:25:53_1.png')

segmentator = CharactersSegmentator(CharactersValidator())

license_plate = reader.get_binary()

characters = segmentator.get_characters_from_license_plate(license_plate)

saver = ImageSaver('../characters')
model_mapper = ModelMapper()

predictor = Predictor(model_mapper)
predictor.clasify_characters(characters)
characters = predictor.get_classified_characters()

print(characters)

# for character in characters:
  # saver.save_as_train_data(character, model_mapper.train_image_width, model_mapper.train_image_height)