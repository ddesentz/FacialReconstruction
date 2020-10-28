import copy
import os
import cv2
import numpy as np

base_dir_path = {}
faces = []
labels = []
dict_face_labels = {}


def create_face_dictionary(path):
    cnt = 0
    for subdir, dirs, files in os.walk(path):
        sbdir_nm = subdir.split("/")[-1]
        dict_face_labels[cnt] = sbdir_nm
        cnt += 1


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y + w, x:x + h], faces[0]  # could return more than one image


def prepare_training_data(data_folder_path):
    label = -1
    for subdir, dirs, files in os.walk(data_folder_path):
        if subdir.startswith("."):
            continue
        else:
            dirname = (subdir.split("/")[-1])
            for k, v in dict_face_labels.items():
                if v == dirname:
                    label = int(k)
                    break

            for f in files:
                if f.startswith("."):
                    continue
                else:
                    subject_dir_path = subdir + "/" + f
                    img = cv2.imread(subject_dir_path)
                    face, rect = detect_face(img)
                    if face is not None:
                        faces.append(face)
                        labels.append(label)
    return faces, labels


def get_normal_base_image(orig_name):
    answer_img_path = ""
    for root, dirs, files in os.walk(base_dir_path[0]):
        if root.split("/")[-1] == orig_name:
            for f in files:
                if f.find((".normal.")) != -1:
                    answer_img_path = root + "/" + f
    return answer_img_path


def predict(test_img, faceRec):
    origImg = cv2.imread(test_img)
    img = copy.copy(origImg)
    face, rect = detect_face(img)
    label = faceRec.predict(face)[0]
    label_text = ""

    for k, v in dict_face_labels.items():
        if k == label:
            label_text = str(v)

    ans_path = get_normal_base_image(label_text)

    return img, ans_path


def process_images(path, test_img):
    base_dir_path[0] = path
    print("Base Directory is: ", path)
    print("Test Image is: ", test_img)
    create_face_dictionary(path)
    faces, labels = prepare_training_data(path)
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))

    predicted_img1, result_return_path = predict(test_img, face_recognizer)
    print("Prediction complete")

    return result_return_path
