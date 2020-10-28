from flask import Flask, jsonify, request, redirect, flash
from flask_pymongo import PyMongo, MongoClient
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from PIL import Image
import gridfs
import image_processing as pi

# *****************************************************************
#   IMPORT FOLLOWING DEPENDENCIES                                 *
# *****************************************************************
#   opencv-contrib-python	                                      *
#   flask 				                                          *
#   flask-cors			                                          *
#   jinja2				                                          *
#   pillow				                                          *
#   numpy				                                          *
# *****************************************************************

app = Flask(__name__)
cors = CORS(app)

app.config['MONGO_URI'] = 'mongodb://localhost/maskeraid'
app.config['CORS_HEADERS'] = 'Content-Type'

mongo = PyMongo(app)
app.secret_key = "maskeraidServer"

#This is where all the AI Code can be placed
#Whatever import information extracted from the code that should be displayed
#will be returned as a json from any method that can be accessed from an api
#as shown below.  This api is being called from src/client/pages/Maskeraid.tsx
#line 22 when the button is clicked
@app.route('/api/test', methods=['GET'])
@cross_origin()
def test():
    result = {'fileName' : 'path/exampleFile.png', 'FirstName' : 'Derek', 'LastName' : 'Desentz'}
    return jsonify({'result' : result})


# ***********************************************************************************
# USAGE:
# ------
# Run this command form Terminal:        $ npm run server
# This will fire up the web application on  http://127.0.0.1:5000/
# To test LBHP Algorithm enter url          http://127.0.0.1:5000/predict
# Following output should be displayed on the web page:
# public/resources/normal_pics_db/faces/Charles_Zach/Charles_Zach.normal.pgm
# This is the address of Resulting image
# ***********************************************************************************
@app.route('/predict', methods=['GET'])
@cross_origin()
def match_test_image():
    base_dir = 'public/resources/normal_pics_db'
    test_img = 'public/resources/test_pics_with_specs/Charles_Zach.glasses.pgm'
    result_return_path = pi.process_images(base_dir, test_img)
    return result_return_path

# *******************************************************************************************
# Base Directory and Test Image path is hard-coded for testing purpose. The task is to
# pass these two parameters and the Selected AI Algorithm (in this case it is LBHP) from
# another page to this End-Point.
# The 'return' should render an HTML page with Test Image and Result Image
# *******************************************************************************************


if __name__ == '__main__':
    app.run(debug=True)