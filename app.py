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
    try:
        collection_name = 'users'
        # Query the 'users' collection
        data_from_collection = mongo.db[collection_name].find()

        # Convert MongoDB cursor to list of dictionaries
        data_list = list(data_from_collection)

        # If you want to return JSON response
        return jsonify(data_list)
        
        # If you want to return HTML template with the data
        # return render_template('your_template.html', data=data_list)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            'error': 'Failed to fetch data from MongoDB'
        })

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
