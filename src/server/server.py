from flask import Flask, jsonify, request, redirect, flash
from flask_pymongo import PyMongo, MongoClient
from flask_cors import CORS, cross_origin
from PIL import Image
import json
import bson
import glob
import os
import image_processing as pi
import cv2
import numpy as np
import gridfs
from io import StringIO

app = Flask(__name__)
cors = CORS(app)

app.config['MONGO_URI'] = 'mongodb://localhost/maskeraid'
app.config['CORS_HEADERS'] = 'Content-Type'

mongo = PyMongo(app)
app.secret_key = "maskeraidServer"

base_dir_path = {}
faces = []
labels = []
dict_face_labels = {}

@app.route('/api/enrollDB', methods=['POST'])
@cross_origin()
def addImage():
    fs = gridfs.GridFS(mongo.db)
    images = mongo.db.images
    cv2 = mongo.db.cv2
    image = request.files['img']
    pilImage = Image.open(image)
    open_cv_image = np.array(pilImage)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    imageString = open_cv_image.tostring()
    imageID = fs.put(imageString, encoding='utf-8')

    imageResult = {
        'filename': image.filename,
        'id': image.filename.split('/')[1]
    }
    cv2Result = {
            'imageID': imageID,
            'shape': open_cv_image.shape,
            'dtype':str(open_cv_image.dtype)
    }
    images.update_one({'filename' : image.filename},{"$set" : imageResult}, True)
    cv2.update_one({'filename' : image.filename},{"$set" : cv2Result}, True)
    #mongo.save_file(image.filename, image)

    return jsonify({'result' : imageResult})

@app.route('/api/predict', methods=['POST'])
@cross_origin()
def predictImage():
    result = []
    stringData = request.data.decode("utf-8").strip('"')
    data = json.loads(stringData)

    populateLabels()
    f, l = prepareTrainingData()
    app.logger.info("Total Faces: " + str(len(f)))
    app.logger.info("Total Labels: " + str(len(l)))

    return jsonify({'result' : result})


def populateLabels():
    col = mongo.db.images
    cursor = col.find({})
    cnt = 0
    for doc in cursor:
        dict_face_labels[cnt] = doc['id']
        cnt += 1


def prepareTrainingData():
    col = mongo.db.images
    cv2 = mongo.db.cv2
    fs = gridfs.GridFS(mongo.db)
    cursor = col.find({})
    label = -1
    for doc in cursor:
        for k,v in dict_face_labels.items():
            if v == doc['filename'].split('/')[1]:
                label = int(k)
                #app.logger.info(label)
                break

        img = cv2.find_one({'filename':doc['filename']})

        gOut = fs.get(img['imageID'])
        image = np.frombuffer(gOut.read(), dtype=np.uint8)
        image = np.reshape(image, img['shape'])
        face, rect = detect_face(image)

        if face is not None:
            faces.append(face)
            labels.append(label)

    return faces, labels


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y + w, x:x + h], faces[0]  # could return more than one image

if __name__ == '__main__':
    app.run(debug=True)