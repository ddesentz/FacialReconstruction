from flask import Flask, jsonify, request, redirect, flash
from flask_pymongo import PyMongo, MongoClient
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from PIL import Image
import gridfs

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

if __name__ == '__main__':
    app.run(debug=True)