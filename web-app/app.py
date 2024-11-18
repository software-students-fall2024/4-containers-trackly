"""
Flask web application for Trackly
"""

import os
from flask import Flask, request, Response,render_template, redirect, url_for
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import cv2
camera=cv2.VideoCapture(0)

load_dotenv()

def create_app():

    """
    Configure Flask Application
    Returns: Flask App
    """

    app = Flask(__name__)

    mongo_uri = os.getenv("MONGO_URI","mongodb://localhost:27017")

    if mongo_uri is None:
        raise ValueError("Error with mongo_URI")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client.get_database("Trackly")
        app.db = db
        #collection = db["entries"]
        print("Connected to MongoDB")
    except errors.ServerSelectionTimeoutError as con_e:
        print(f"Error connecting to MongoDB Database: {con_e}")
        app.db =  None
    except errors.ConfigurationError as fig_e:
        print(f"Error configuring MongoDB Database: {fig_e}")
        app.db = None
    def generate_frames():
        while True:
            sucess, frame = camera.read()
            if not sucess:
                break
            else:
                ret, buffer = cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
            app.db["tasks"].insert_one({"name": name, "task": task, "time": time})
            tasks = list(app.db["tasks"].find({}, {"_id": 0}))
            print(tasks)

            # Redirect to the start-focusing page
            return redirect(url_for('start_focusing'))
        return render_template("home.html")

    @app.route('/start-focusing')
    def start_focusing():
        # Render the start-focusing screen (replace with your actual HTML rendering logic)
        tasks = list(app.db["tasks"].find({}, {"_id": 0}))
        if tasks:
            print(f"Tasks: {tasks}")
        else:
            print("No tasks found.")
        return render_template("start-focusing.html")
    @app.route('/camera')
    def video():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=int(FLASK_PORT))
