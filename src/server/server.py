from flask import Flask, jsonify, request, redirect, flash
from flask_pymongo import PyMongo, MongoClient
from flask_cors import CORS, cross_origin
from PIL import Image
import gridfs
import json
import glob
import os
import image_processing as pi
import tempfile
import shutil

app = Flask(__name__)
cors = CORS(app)

app.config['MONGO_URI'] = 'mongodb://localhost/maskeraid'
app.config['CORS_HEADERS'] = 'Content-Type'

mongo = PyMongo(app)
app.secret_key = "maskeraidServer"

@app.route('/api/enrollDB', methods=['POST'])
@cross_origin()
def addImage():
    image = request.files['img']
    result = []
    mongo.save_file(image.filename, image)
    result.append(image.filename)

    app.logger.info(result)
    return jsonify({'result' : result})

@app.route('/api/predict', methods=['POST'])
@cross_origin()
def match_test_image():
    result = []
    dirpath = tempfile.mkdtemp()
    app.logger.info(dirpath)

    stringData = request.data.decode("utf-8").strip('"')
    data = json.loads(stringData)

    base_dir = 'public/resources/normal_pics_db'
    test_img = 'public/resources/test_pics_with_specs/Charles_Zach.glasses.pgm'
    #result_return_path = pi.process_images(base_dir, test_img)

    shutil.rmtree(dirpath)
    return jsonify({'result' : result})

if __name__ == '__main__':
    app.run(debug=True)