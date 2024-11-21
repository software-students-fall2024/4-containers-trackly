"""
Flask web application for Trackly
"""

import os
from flask import Flask, request, Response,render_template, redirect, url_for, jsonify
import requests
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import subprocess
import sys
import time
import logging

sys.path.append('/app/machine-learning-client')
# from camera_module import start_camera

load_dotenv()

def create_app():
    app = Flask(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )

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
        app.db = None
    except errors.ConfigurationError as fig_e:
        print(f"Error configuring MongoDB Database: {fig_e}")
        app.db = None

    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            name = request.form.get('name')
            task = request.form.get('task')
            time = request.form.get('time')

            if app.db:
                app.db["tasks"].insert_one({"name": name, "task": task, "time": time})
                tasks = list(app.db["tasks"].find({}, {"_id": 0}))
                print(tasks)
            else:
                print("Could not connect to database")

        return render_template("home.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route('/start-focusing')
    def start_focusing():
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

    @app.route('/start-session', methods=['POST'])
    def start_session():
        video_path = "session_video.avi"
        
        try:
            ml_video_info = "http://machine-learning-client:5002/process-video"
            response = requests.get(ml_video_info)
            if response.status_code != 200:
                return jsonify({"error": str(e)}), {response.status_code}
            
            session_data = response.json()

            ml_client_url = "http://machine-learning-client:5002/process-session"
            response = requests.post(ml_client_url, json=session_data)
            ml_results = response.json()

            session_data.update(ml_results)
            session_data["video_path"] = video_path
            db.sessions.insert_one(session_data)
            return jsonify({"message": "Session complete", "data": session_data}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/session-details')
    def session_details():
        total_time = request.args.get('total_time', default=0, type=int)
        focused_time = request.args.get('focused_time', default=0, type=int)
        return render_template('session-details.html', total_time=total_time, focused_time=focused_time)

    @app.route('/file-data', methods=['POST'])
    def handle_video_upload():
        app.logger.info(request.files)
        uploaded_file = request.files.get("file")
        app.logger.info(uploaded_file)
        if not uploaded_file:
            return jsonify({"error": "No file"}), 400
        
        app.logger.info(f"Received file: {uploaded_file.filename} of type {uploaded_file.mimetype}")
        
        video_path = "uploaded_video.webm"
        app.logger.info("testing file-data upload ")
        uploaded_file.save(video_path)
        
        ml_client_url = "http://machine-learning-client:5002/process-video"
        
        try:
            with open(video_path, 'rb') as video:
                response = requests.post(ml_client_url, files={"file": video})
            if response.status_code == 200:
                result = response.json()
                app.logger.info("Video processed successfully:", result)

                total_time = result.get("total_time")
                focused_time = result.get("focused_time")

                if app.db is not None:
                    focus_percentage = (focused_time / total_time) * 100 if total_time > 0 else 0
                    session_data = {
                        "total_time": total_time,
                        "focused_time": focused_time,
                        "focus_percentage": focus_percentage,
                        "timestamp": time.time()
                    }
                    app.db["sessions"].insert_one(session_data)
                    app.logger.info("Session data saved")

                return redirect(url_for('session_details', total_time = result['total_time'], focused_time=result['focused_time']))
            else:
                app.logger.info("Error in processing video:", response.text)
                return jsonify({"error app.py": "ML client error", "details": response.text}), response.status_code
        except requests.ConnectionError as e:
            app.logger.info(f"Error connecting to ML client: {e}")
            return jsonify({"error": "Unable to connect to ML Client", "details": str(e)}), 500

    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=int(FLASK_PORT))
