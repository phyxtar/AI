from flask import Flask, request, jsonify, send_from_directory
import cv2
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow all origins

UPLOAD_FOLDER = "uploads"
FRAME_FOLDER = "frames"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAME_FOLDER, exist_ok=True)

def extract_frames(video_path, frame_folder):
    """ Extract key frames (shots & movements) from the video """
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    shot_images = []
    movement_images = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 30 == 0:  # Save every 30th frame
            filename = f"frame_{frame_count}.jpg"
            frame_path = os.path.join(frame_folder, filename)
            cv2.imwrite(frame_path, frame)

            if frame_count % 60 == 0:  
                shot_images.append(filename)  # Shots every 60 frames
            else:
                movement_images.append(filename)  # Movement frames

        frame_count += 1

    cap.release()
    return shot_images, movement_images

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)

    shot_images, movement_images = extract_frames(video_path, FRAME_FOLDER)

    report = {
        "total_movements": len(movement_images),
        "total_shots": len(shot_images),
        "improvement_suggestions": [
            "Increase foot speed.",
            "Improve backhand shot consistency.",
            "Better positioning for smashes.",
        ],
        # ✅ Fix URLs
        "shot_images": [f"http://127.0.0.1:5000/frames/{img}" for img in shot_images],
        "movement_images": [f"http://127.0.0.1:5000/frames/{img}" for img in movement_images],
    }

    return jsonify({"message": "Video uploaded successfully", "report": report})

# ✅ Add Route to Serve Images
@app.route("/frames/<filename>")
def get_frame(filename):
    return send_from_directory(FRAME_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
