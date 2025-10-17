from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json

app = Flask(__name__)

# ---- MongoDB Atlas Connection ----
client = MongoClient("mongodb+srv://Govind:<Govind1155>@cluster0.qk7lihq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["flask_demo"]
collection = db["Govind"]

# ---- API route ----
@app.route('/api')
def api_data():
    with open("data.json") as file:
        data = json.load(file)
    return jsonify(data)

# ---- Home page with form ----
@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            
            if not name or not email:
                raise ValueError("Both name and email are required!")

            # Insert into MongoDB
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for('success'))
        
        except Exception as e:
            error_message = str(e)
    return render_template('index.html', error=error_message)

# ---- Success page ----
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
