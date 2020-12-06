import json

import cv2
import gridfs
import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo, MongoClient

app = Flask(__name__)

cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

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
    # imageString = open_cv_image.tostring()
    imageString = open_cv_image.tobytes()
    imageID = fs.put(imageString, encoding='utf-8')

    cv2Result = {
        'imageID': imageID,
        'shape': open_cv_image.shape,
        'dtype': str(open_cv_image.dtype)
    }

    testImages.update_one({'filename': image.filename}, {"$set": cv2Result}, True)
    app.logger.info("Message: Test Image {} added to database".format(image))
    return jsonify({'result': result})


@app.route('/api/clearDB', methods=['DELETE'])
@cross_origin()
def clearDB():
    client = MongoClient("mongodb://localhost")
    client.drop_database('coldcuts')
    app.logger.info("Message: MongoDB Database Cleared")
    return ""


@app.route('/api/enrollDB', methods=['POST'])
@cross_origin()
def addImage():
    fs = gridfs.GridFS(mongo.db)
    images = mongo.db.images
    cv2 = mongo.db.cv2
    image = request.files['img']
    imageResult = {}
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
            'dtype': str(open_cv_image.dtype),
            'person': image.filename.split('/')[1]
        }
        images.update_one({'filename': image.filename}, {"$set": imageResult}, True)
        cv2.update_one({'filename': image.filename}, {"$set": cv2Result}, True)
        app.logger.info("Message: Filename {} added to MongoDB Database".format(image.filename))
    return jsonify({'result': imageResult})


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
    app.logger.info("Message: Predict Image method Completed")

    return jsonify({'result': resImg})


@app.route("/api/getImage/<path:filename>", methods=['GET'])
def get_upload(filename):
    return mongo.send_file(filename, cache_for=99999999)


def populateLabels():
    col = mongo.db.images
    cursor = col.find({})
    cnt = 0
    for doc in cursor:
        dict_face_labels[cnt] = doc['id']
        cnt += 1


def prepareTrainingData():
    faces = []
    labels = []
    col = mongo.db.images
    cv2 = mongo.db.cv2
    fs = gridfs.GridFS(mongo.db)
    cursor = col.find({})
    label = -1
    for doc in cursor:
        app.logger.info("Document is: {}".format(doc))
        for k, v in dict_face_labels.items():
            if v == doc['filename'].split('/')[1]:
                label = int(k)
                break

        img = cv2.find_one({'filename': doc['filename']})
        # img = cv2.resize(img, (448, 448), interpolation=cv2.INTER_AREA)
        gOut = fs.get(img['imageID'])
        image = np.frombuffer(gOut.read(), dtype=np.uint8)
        image = np.reshape(image, img['shape'])
        face, rect = detect_face(image)

        if face is not None:
            faces.append(face)
            labels.append(label)
    app.logger.info("Message: Training Data Prepared")
    return faces, labels


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.array(gray, dtype='uint8')

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    facesx = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=1)  # 5   1  1.2   2
    if len(facesx) == 0:
        return None, None
    (x, y, w, h) = facesx[0]
    app.logger.info("Message: Face Detection Complete")
    return gray[y:y + w, x:x + h], facesx[0]  # could return more than one image


def predict(imgPath, faceRec):
    app.logger.info("preeict at 219 started")
    testImages = mongo.db.testImages
    cv2 = mongo.db.cv2
    fs = gridfs.GridFS(mongo.db)
    img = testImages.find_one({'filename': imgPath})
    gOut = fs.get(img['imageID'])
    image = np.frombuffer(gOut.read(), dtype=np.uint8)
    image = np.reshape(image, img['shape'])
    app.logger.info("Before Detect Face")
    face, rect = detect_face(image)
    app.logger.info("After Detect Face")
    label = faceRec.predict(face)[0]
    app.logger.info("Label is {}".format(label))
    label_text = ""

    for k, v in dict_face_labels.items():
        if k == label:
            label_text = str(v)

    app.logger.info("Label Text is: {}".format(label_text))
    resImg = cv2.find_one({'person': label_text})

    app.logger.info("Message: Prediction Complete")
    return resImg['filename']


def resize_test_image(img):  # from 54
    resizedImage = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)  # INTER_AREA
    return resizedImage


if __name__ == '__main__':
    print("Started app ...")
    app.run(debug=True)
