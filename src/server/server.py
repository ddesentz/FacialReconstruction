import json

import cv2
import gridfs
import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo, MongoClient

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
# faces = []
# labels = []
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
    # imageString = open_cv_image.tostring() # tobytes
    imageString = open_cv_image.tobytes()
    imageID = fs.put(imageString, encoding='utf-8')

    cv2Result = {
        'imageID': imageID,
        'shape': open_cv_image.shape,
        'dtype': str(open_cv_image.dtype)
    }
    testImages.remove()
    testImages.update_one({'filename': image.filename}, {"$set": cv2Result}, True)

    return jsonify({'result': result})


@app.route('/api/clearDB', methods=['DELETE'])
@cross_origin()
def clearDB():
    client = MongoClient("mongodb://localhost")
    client.drop_database('maskeraid')
    return ""


@app.route('/api/enrollDB', methods=['POST'])
@cross_origin()
def addImage():
    fs = gridfs.GridFS(mongo.db)
    images = mongo.db.images
    # cv2 = mongo.db.cv2
    ceevee2 = mongo.db.ceevee2
    image = request.files['img']
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
    ceevee2.update_one({'filename': image.filename}, {"$set": cv2Result}, True)

    return jsonify({'result': imageResult})


@app.route('/api/predict', methods=['POST'])
@cross_origin()
def predictImage():
    # faces = []
    # labels = []
    result = []
    fs = gridfs.GridFS(mongo.db)
    stringData = request.data.decode("utf-8").strip('"')
    data = json.loads(stringData)
    imgPath = data['image']

    # req_data = request.get_json()
    app.logger.info("String data is: {}".format(stringData))

    populateLabels()
    faces, labels = prepareTrainingData()
    app.logger.info("Total Faces: " + str(len(faces)))
    app.logger.info("Total Labels: " + str(len(labels)))

    face_recognizer = ''
    if data['algorithm'] == 'LBHP':
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    elif data['algorithm'] == 'EIGEN':
        face_recognizer = cv2.face.EigenFaceRecognizer_create()
    elif data['algorithm'] == 'FISHER':
        face_recognizer = cv2.face.FisherFaceRecognizer_create()
    else:
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    app.logger.info("Algo is: {}".format(data['algorithm']))

    face_recognizer.train(faces, np.array(labels))
    app.logger.info("Training done!")
    try:
        # -----------

        # -----------
        resImg = predict(imgPath, face_recognizer)
        app.logger.info("Prediction done")
        app.logger.info("Prediction Complete")
        app.logger.info(resImg)
        if resImg is not None:
            app.logger.info("Prediction Complete ")
            return jsonify({'result': resImg})
        else:
            app.logger.info("Prediction Complete in None")
            return jsonify({'result': 'public/NoMatchFound.jpg'})
    except Exception as e:
        app.logger.info("Exception occurred finding resImg")
        return jsonify({'result': 'public/NoMatchFound.jpg'})


    # return jsonify({'result': resImg})



@app.route("/api/getImage/<path:filename>", methods=['GET'])
def get_upload(filename):
    if filename == 'public/NoMatchFound.jpg':
        return filename
    else:
        return mongo.send_file(filename, cache_for=99999999)



def populateLabels():
    col = mongo.db.images
    cursor = col.find({})
    cnt = 0
    for doc in cursor:
        dict_face_labels[cnt] = doc['id']
        app.logger.info("Item {} has Id {}".format(doc['id'], cnt))
        cnt += 1
    for k, v in dict_face_labels.items():
        app.logger.info("Key {} has Value {}".format(str(k), str(v)))


def prepareTrainingData():
    faces = []
    labels = []
    col = mongo.db.images
    ceevee2 = mongo.db.ceevee2
    fs = gridfs.GridFS(mongo.db)
    cursor = col.find({})
    label = -1
    for doc in cursor:
        for k, v in dict_face_labels.items():
            if v == doc['filename'].split('/')[1]:
                label = int(k)
                break

        img = ceevee2.find_one({'filename': doc['filename']})
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
    # face_cascade = cv2.CascadeClassifier(
    #     cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1) # 3 1.2, 5   cv2.CvFeatureParams_LBP
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return cv2.resize(gray[y:y + w, x:x + h], (224, 224)), faces[0]
    # return gray[y:y + w, x:x + h], faces[0]  # could return more than one image


def predict(imgPath, faceRec):
    testImages = mongo.db.testImages
    ceevee2 = mongo.db.ceevee2
    fs = gridfs.GridFS(mongo.db)
    img = testImages.find_one({'filename': imgPath})

    # fn = testImages.filename
    # if fn in ()
    # ----------
    gOut = fs.get(img['imageID'])
    image = np.frombuffer(gOut.read(), dtype=np.uint8)
    image = np.reshape(image, img['shape'])
    face, rect = detect_face(image)

    label = faceRec.predict(face)[0]
    label_text = ""

    app.logger.info("Label is: {}".format(label))
    # app.logger.info("Confidence is {}".format(confidence))

    for k, v in dict_face_labels.items():
        if k == label:
            label_text = str(v)

    resImg = ceevee2.find_one({'person': label_text})
    app.logger.info("Value of resImg: ", resImg)
    return resImg['filename']
    # ----------




    # if label_text == '' or label_text is None:
    #     return 'public/NoMatchFound.jpg'
    # else:
    #     return resImg['filename']


if __name__ == '__main__':
    app.run(debug=True)
