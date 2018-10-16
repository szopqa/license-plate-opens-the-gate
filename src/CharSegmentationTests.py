from CharactersSegmentator import CharactersSegmentator
from CharactersValidator import CharactersValidator
from Reader import Reader

reader = Reader('../output_images/2018-10-16T21:05:58_1.png')

segmentator = CharactersSegmentator(CharactersValidator())

license_plate = reader.get_binary()

segmentator.get_characters_from_license_plate(license_plate)