from flask import Flask, jsonify, request, redirect, flash
from flask_pymongo import PyMongo, MongoClient
from flask_cors import CORS, cross_origin
from PIL import Image
import json
import bson
import glob
import os
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


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

base_dir_path = {}
faces = []
labels = []
dict_face_labels = {}

@app.route('/api/enrollTestImage', methods=['POST'])
@cross_origin()
def addTestImage():
    result = []
    fs = gridfs.GridFS(mongo.db)
    testImages = mongo.db.testImages
    image = request.files['img']
    pilImage = Image.open(image)
    open_cv_image = np.array(pilImage)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    imageString = open_cv_image.tostring()
    imageID = fs.put(imageString, encoding='utf-8')

    cv2Result = {
            'imageID': imageID,
            'shape': open_cv_image.shape,
            'dtype':str(open_cv_image.dtype)
    }

    testImages.update_one({'filename' : image.filename},{"$set" : cv2Result}, True)

    return jsonify({'result' : result})

@app.route('/api/clearDB', methods=['DELETE'])
@cross_origin()
def clearDB():
    client = MongoClient("mongodb://localhost")
    client.drop_database('andde')
    return ""

@app.route('/api/enrollDB', methods=['POST'])
@cross_origin()
def addImage():
    imageResult = []
    fs = gridfs.GridFS(mongo.db)
    images = mongo.db.images
    cv2 = mongo.db.cv2
    image = request.files['img']
    if not (image.filename.split('/')[1].startswith('.')):
        mongo.save_file(image.filename, image)
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
                'dtype':str(open_cv_image.dtype),
                'person': image.filename.split('/')[1]
        }
        images.update_one({'filename' : image.filename},{"$set" : imageResult}, True)
        cv2.update_one({'filename' : image.filename},{"$set" : cv2Result}, True)

    return jsonify({'result' : imageResult})

@app.route('/api/predict', methods=['POST'])
@cross_origin()
def predictImage():
    result = []
    fs = gridfs.GridFS(mongo.db)
    stringData = request.data.decode("utf-8").strip('"')
    data = json.loads(stringData)
    imgPath = data['image']

    populateLabels()
    faces, labels = prepareTrainingData()
    app.logger.info("Total Faces: " + str(len(faces)))
    app.logger.info("Total Labels: " + str(len(labels)))

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    resImg = predict(imgPath, face_recognizer)

    app.logger.info("Prediction Complete")
    app.logger.info(resImg)

    return jsonify({'result' : resImg})

@app.route("/api/getImage/<path:filename>", methods=['GET'])
def get_upload(filename):
    return mongo.send_file(filename,cache_for=99999999)

def populateLabels():
    col = mongo.db.images
    cursor = col.find({})
    label = -1
    text = ""
    for index, doc in enumerate(cursor):
        if not( doc['id'] == text):
            label += 1
        text = doc['id']
        dict_face_labels[index] = {"text": text, "label": label}


def prepareTrainingData():
    col = mongo.db.images
    cv2 = mongo.db.cv2
    fs = gridfs.GridFS(mongo.db)
    cursor = col.find({})
    label = -1
    for doc in cursor:
        for item in dict_face_labels:
            entry = dict_face_labels.get(item)
            if entry["text"] == doc['filename'].split('/')[1]:
                label = entry["label"]
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

def predict(imgPath, faceRec):
    app.logger.info("IMG PATH: " + imgPath)
    testImages = mongo.db.testImages
    cv2 = mongo.db.cv2
    fs = gridfs.GridFS(mongo.db)
    img = testImages.find_one({'filename':imgPath})
    gOut = fs.get(img['imageID'])
    image = np.frombuffer(gOut.read(), dtype=np.uint8)
    image = np.reshape(image, img['shape'])
    face, rect = detect_face(image)
    label = faceRec.predict(face)[0]
    app.logger.info("LABEL id: " + str(label))
    label_text = ""

    label_text = dict_face_labels.get(label)["text"]

    app.logger.info("LABEL TEXT: " + label_text)
    resImg = cv2.find_one({'person':label_text})
    return resImg['filename']


if __name__ == '__main__':
    app.run(debug=True)