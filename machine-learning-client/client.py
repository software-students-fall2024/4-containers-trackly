# #Client
# import cv2  # OpenCV for video capture
# import pymongo  # MongoDB client
# import time
# import os
# from dotenv import load_dotenv
# import camera_module

# load_dotenv()

# # MongoDB setup
# mongo_uri = os.getenv("MONGO_URI")
# client = pymongo.MongoClient(mongo_uri)
# db = client['productivity_db']
# collection = db['focus_data']

# def capture_focus_data():
#     # OpenCV video capture setup
#     cap = cv2.VideoCapture(0)  # Use the first camera connected to your computer

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Placeholder: Focus detection logic to be implemented here
#         focus_metric = {"timestamp": time.time(), "focus_score": 0.75}  # Dummy value for now
        
#         # Save to MongoDB
#         collection.insert_one(focus_metric)

#          # Display the frame with a simple message
#         cv2.putText(frame, "Focus Score: 0.75", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
#                     1, (255, 0, 0), 2, cv2.LINE_AA)
        
#         # Display the frame
#         cv2.imshow('Focus Monitor', frame)
        
#         # Exit on 'q' key
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             print("Exiting focus monitor...")
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     try:
#         capture_focus_data()
#     except Exception as e:
#         print(f"An error occurred rip: {e}")
from flask import Flask, request, jsonify
import os
from camera_module import start_camera
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.StreamHandler(),  # Log to the console
        logging.FileHandler("app.log")  # Log to a file (optional)
    ]
)
result = {}

@app.route('/process-video', methods=['GET','POST'])
def process_video():
    if request.method=='POST':
        uploaded = request.files.get("file")
        if not uploaded:
            app.logger.error("No video file")
            return jsonify({"error": "No video file"})
        
        try:
            video_path = os.path.join("/tmp", uploaded.filename)
            app.logger.info(uploaded)
            uploaded.save(video_path)
            app.logger.info(f"File saved to: {video_path}")

            ## Machine Learning algorithm for calculation here
            total_time, focused_time = 0, 0
            try:
                total_time, focused_time = start_camera(video_path)
            except:
                app.logger.info("client.py, start-camera failed")

            # total_time = 600
            # focused_time = 450

            result = {
                "message": "Processed",
                "total_time": total_time,
                "focused_time": focused_time
            }
            app.logger.info(f"Processed video: total_time={total_time}, focused_time={focused_time}")
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"client.py error": str(e)}), 500
    elif request.method == 'GET':
       try:
           if not result:
               return jsonify({"error": "No processed data available"}), 404
           return jsonify(result), 200
       except Exception as e:
           app.logger.error(f"Error retrieving processed data: {str(e)}")
           return jsonify({"error": str(e)}), 500


@app.route('/process-session', methods=['POST'])
def process_session():

    data = request.json
    total_time = data.get("total_time")
    focused_time = data.get("focused_time")

    if total_time is None or focused_time is None:
        return jsonify({"error": "Invalid session data"}), 400
    
    if total_time > 0:
        focus_percentage = (focused_time / total_time) * 100
    else:
        focus_percentage = 0
    
    if focus_percentage > 75:
        insight = "Excellent focus"
    elif focus_percentage > 50:
        insight = "Good focus"
    else:
        insight = "Needs improvement"
    
    return jsonify({"Focus Percentage": focus_percentage, "Insight": insight}), 200

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5002)
