import os
import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug import secure_filename
from helpers import JSONEncoder, dateify, make_satellite_sets

import pdb

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME', 'starbooks')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/starbooks')

mongo = PyMongo(app)

#### ENDPOINTS ####

@app.errorhandler(404)
def page_not_found(e):
    endpoint = request.path
    message = 'Bad Endpoint: {}'.format(endpoint)
    return jsonify({'error': message})


@app.route('/api/v1/satellites', methods=['GET'])
def get_satellites():
    satellites = mongo.db.satellites
    output = []
    for item in satellites.find():
        errors = item.get('errors')
        output.append({
            'satellite_id': item.get('satellite_id'),
            'timestamp': dateify(item.get('timestamp')),
            'set_id': item.get('set_id'),
            'condition': item.get('condition'),
            'status': item.get('status'),
            'errors': errors.split('|') if errors else []
        })
    if not output:
        return jsonify({'error': 'No Results Found'})
    return jsonify({'data': output})


@app.route('/api/v1/upload', methods=['POST'])
def file_upload():
    coll = mongo.db.satellites
    fileobj = request.files['file']
    try:
        text = fileobj.read()
        output = json.loads(text)
    except:
        output = 'Invalid JSON'
    else:
        sets = make_satellite_sets(output)
        for s in sets:
            key = {
                'satellite_id': s.satellite_id,
                'set_id': s.set_id
            }
            record = coll.find_one(key)
            if record:
                coll.update(key, s)
            else:
                coll.insert(s)
    return ''


#### RUN APP ####

if __name__ == '__main__':
    DEBUG = True #os.getenv('DEBUG', True)
    HOST = 'localhost' #os.getenv('HOST', 'localhost')
    PORT = 8000 #os.getenv('PORT', 5000)

    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT
    )

