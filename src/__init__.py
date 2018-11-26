import os

from ImageAnalyzer import ImageAnalyzer
from plate_recognition_service.PlateRecognitionService import PlateRecognitionService

if __name__ == "__main__":
    character_recognition_model_path = f'{os.getcwd()}/models/svc/svc.pkl'

    image_analyzer = ImageAnalyzer(character_recognition_model_path, 0.4)
    service = PlateRecognitionService(image_analyzer).start(port = 5000)


