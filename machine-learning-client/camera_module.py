#Camera Module
#Load the cascades 
#Capture video from the webcam

import cv2
# import pymongo
import time
import os
# from dotenv import load_dotenv
from flask import Flask, request, jsonify

# load_dotenv()

# MongoDB setup
# mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# client = pymongo.MongoClient(mongo_uri)
# db = client['productivity_db']
# collection = db['focus_data']
# app = Flask(__name__)

# @app.route('/process-video', methods=['POST'])
# def process_video():
#     uploaded_file = request.files['file']
#     if uploaded_file:
#         # Save the file temporarily
#         video_path = "processed_video.webm"
#         uploaded_file.save(video_path)
#         capture_focus_data(uploaded_file)
#         # Run your ML model or processing logic here
#         # Example: result = your_ml_model.process(video_path)
#         result = {"message": "Video processed successfully!"}
        
#         # Return the result
#         return jsonify(result), 200
#     else:
#         return jsonify({"error": "No file received"}), 400

    
def start_camera(output_video):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    temp_path = "temp_video.webm"
    output_video.save(temp_path)

    cap = cv2.VideoCapture(temp_path)
    # cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not access webcam")
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video, fourcc, 20.0, (640, 480))
    
    total_time = 0
    focus_time = 0
    session_start_time = time.time()
    start_time = None

    print("Press 'q' to stop the camera")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            if start_time is None:
                start_time = time.time()
            else:
                focus_time += time.time() - start_time
                start_time = time.time()
        else:
            start_time = None

        total_time = time.time() - session_start_time

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        cv2.putText(frame, f"Focus Time: {focus_time:.2f} sec", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Total Time: {total_time:.2f} sec", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Focus Monitor', frame)

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Stopping camera")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return total_time, focus_time



    # print("file is processed")
    # # Save to MongoDB
    # focus_metric = {"timestamp": time.time(), "focus_time": focus_time}
    # collection.insert_one(focus_metric)

    # print (f"Focus time: {focus_time:.2f} seconds")
    # return focus_time

# if __name__ == "__main__":
#     app.run(port=5002)
# # if __name__ == "__main__":
#     try:
#         print("Starting focus monitor...")
#         capture_focus_data()
#     except Exception as e:
#         print(f"An error occurred: {e}")
