from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

from flask_cors import CORS
import yaml

app = Flask(__name__)
app.config["MONGO_URI"] = yaml.safe_load(open('database.yaml'))['uri']
mongo = PyMongo(app)
CORS(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['name']
        age = body['age']

        mongo.db.users.insert_one({
            "name": name,
            "age": age
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'name': name,
            'age': age
        })

    # GET all data from database
    if request.method == 'GET':
        all_data = mongo.db.users.find()
        data_json = []
        for data in all_data:
            user_id = str(data['_id'])
            name = data['name']
            age = data['age']
            data_dict = {
                'id': user_id,
                'name': name,
                'age': age
            }
            data_json.append(data_dict)

        return jsonify(data_json)

if __name__ == '__main__':
    app.debug = True
    app.run()
