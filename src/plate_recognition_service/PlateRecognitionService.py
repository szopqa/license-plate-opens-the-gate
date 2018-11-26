import os, json
from flask import Flask, flash, request, redirect, url_for, session, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

import sys, os

class PlateRecognitionService():

    def __init__(self, image_analyzer, image_upload_folder = './uploads'):
        self.__image_analyzer = image_analyzer
        self.__image_upload_folder = os.path.join(image_upload_folder)

    def __set_routes(self, app):
        @app.route('/upload', methods = ['POST'])
        def uploadFile():
            
            self.__create_upload_dir();
            file = request.files['file']

            filename = secure_filename(file.filename)
            image_path = f'{self.__image_upload_folder}/{filename}'

            file.save(image_path)

            session['uploadFilePath'] = image_path
            
            detected_license_plates = self.__image_analyzer.analyze_uploaded_image(image_path)

            response = {
                'success': 'true',
                'detected_license_plates': detected_license_plates
            }

            return Response(
                json.dumps(response), 
                status = 200, 
                mimetype='text/plain'
            )

    def __setup(self, app):
        CORS(app, expose_headers='Authorization')
        app.config['UPLOAD_FOLDER'] = self.__image_upload_folder
        app.secret_key = os.urandom(24)

        self.__set_routes(app)

    def __create_upload_dir(self):
        if not os.path.isdir(self.__image_upload_folder):
            os.mkdir(self.__image_upload_folder)

    def start(self, port): 
        app = Flask(__name__)
        self.__setup(app)
        app.run(debug = True, host = "0.0.0.0", use_reloader = False, port = port)