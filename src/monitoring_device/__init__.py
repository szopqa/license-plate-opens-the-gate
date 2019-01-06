"""
Script should be run inside Raspberry Pi.
It detects movement on Raspi, takes image if detected and sends it to plate recognition service
which in response sends characters of detected license plate.
"""

import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
from picamera import PiCamera
import requests

def capture_image(camera):
    image_name = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    camera.capture('/home/pi/Desktop/{}.jpg'.format(image_name))
    return image_name

def send_captured_image(image_path):
    files = {
        'file': (image_path, open(image_path, 'rb')),
    }

    response = requests.post('http://localhost:5000/upload', files=files)

def run_monitoring_device():
    # hardware setup
    camera = PiCamera()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN) 
    camera.start_preview() # inicjalizacja kamery
    sleep(5)    

    try:
        time.sleep(2) # stabilizacja sensora
        while True:
            if GPIO.input(23):
                print("Motion Detected...")
                image_name = capture_image(camera)
                response = send_captured_image(image_name)
                print('Response: {}'.format(send_captured_image))
                time.sleep(3)
            time.sleep(0.1)

    except:
        GPIO.cleanup()
    finally:
        camera.stop_preview()



if __name__ == "__main__":
    run_monitoring_device()