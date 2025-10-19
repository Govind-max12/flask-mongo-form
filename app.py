from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

# ✅ Use the variable, not the string
client = MongoClient(MONGO_URI)
db = client["flask_demo"]
collection = db["Govind"]

@app.route('/api')
def api_data():
    with open("data.json") as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            if not name or not email:
                raise ValueError("Both name and email are required!")

            collection.insert_one({"name": name, "email": email})
            return redirect(url_for('success'))
        
        except Exception as e:
            error_message = str(e)
    return render_template('index.html', error=error_message)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
