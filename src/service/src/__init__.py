import os, json
from flask import Flask, flash, request, redirect, url_for, session, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

import sys, os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENTIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app, expose_headers='Authorization')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def uploadFile():
    target = os.path.join(UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])

    file.save(destination)

    session['uploadFilePath']=destination
    response = {
        'success': 'true'
    }

    res = Response(json.dumps(response), status=200, mimetype='text/plain')

    return res

app.secret_key = os.urandom(24)
