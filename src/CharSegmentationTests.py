from CharactersSegmentator import CharactersSegmentator
from CharactersValidator import CharactersValidator
from Reader import Reader
from ImageDisplay import ImageDisplay
from Predictor import Predictor

reader = Reader('../output_images/2018-10-17T19:26:16_2.png')
# reader = Reader('../output_images/2018-10-16T21:05:58_1.png')

segmentator = CharactersSegmentator(CharactersValidator())

license_plate = reader.get_binary()

characters = segmentator.get_characters_from_license_plate(license_plate)


# predictor = Predictor()
# predictor.clasify_characters(characters)
# characters = predictor.get_classified_characters()


index = 0
for character in characters:
  if index > 0:
    ImageDisplay.show_image(character)
  index += 1