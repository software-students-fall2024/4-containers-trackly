"""
Flask web application for Trackly
"""

import os
from flask import Flask, request, Response,render_template, redirect, url_for, jsonify
import requests
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import subprocess

load_dotenv()

def create_app():

    """
    Configure Flask Application
    Returns: Flask App
    """

    app = Flask(__name__)

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")

    if mongo_uri is None:
        raise ValueError("Error with URI")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client.get_database("Trackly")
        app.db = db
        print("Connected to MongoDB")
    except errors.ServerSelectionTimeoutError as con_e:
        print(f"Error connecting to MongoDB Database: {con_e}")
        app.db =  None
    except errors.ConfigurationError as fig_e:
        print(f"Error configuring MongoDB Database: {fig_e}")
        app.db = None

    @app.route("/", methods=['GET', 'POST'])
    def home():
        """
        Serves home page
        """
        if request.method == 'POST':
            # Handle the form submission
            name = request.form.get('name')
            task = request.form.get('task')
            time = request.form.get('time')

            # Insert into the "tasks" collection
            if app.db:
                app.db["tasks"].insert_one({"name": name, "task": task, "time": time})
                tasks = list(app.db["tasks"].find({}, {"_id": 0}))
                print(tasks)
            else:
                print("Could not connect to database")

            # Redirect to the start-focusing page
        return redirect(url_for('start_focusing'))

    @app.route('/start-focusing')
    def start_focusing():
        # Render the start-focusing screen (replace with your actual HTML rendering logic)
        tasks = []
        try:
            if app.db:
                tasks = list(app.db["tasks"].find({}, {"_id": 0}))
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
        
        try:
            result = subprocess.run(['python', 'camera_module.py'], capture_output=True, text=True)
            focus_time = result.stdout.strip()
            return render_template("start-focusing.html", tasks=tasks, focus_time=focus_time)
        except Exception as e:
            print(f"Error starting session: {e}")
            return render_template("start-focusing.html", tasks=tasks, focus_time=focus_time)
            
        # tasks = list(app.db["tasks"].find({}, {"_id": 0}))
        # if tasks:
        #     print(f"Tasks: {tasks}")
        # else:
        #     print("No tasks found.")
        # return render_template("start-focusing.html") #tasks=tasks
    
   
    @app.route('/file-data', methods=['POST'])
    def handle_video_upload():
        # Retrieve the uploaded file
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            return jsonify({"error": "No file"}), 400
        
        # Save the file temporarily
        video_path = "uploaded_video.webm"
        uploaded_file.save(video_path)
        
        # Send the video to the ML client for processing
        ml_client_url = "http://machine-learning-client:5002/process-video"  # Replace with ML client URL
        
        try:
            with open(video_path, 'rb') as video:
                response = requests.post(ml_client_url, files={"file": video})
            if response.status_code == 200:
                print("Video processed successfully:", response.json())
                return jsonify(response.json()), 200
            else:
                print("Error in processing video:", response.text)
                return jsonify({"error": "ML client error", "details": response.text}), response.status_code
        except requests.ConnectionError as e:
            print(f"Error connecting to ML client: {e}")
            return jsonify({"error": "Unable to connect to ML Client", "details": str(e)}), 500

    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=int(FLASK_PORT))
