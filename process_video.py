import cv2
import numpy as np
import os

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    output_path = video_path.replace("uploads", "results")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(3)), int(cap.get(4))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    player_movements = []
    shot_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Simple background subtraction for movement detection
        if "prev_frame" in locals():
            frame_diff = cv2.absdiff(prev_frame, blurred)
            _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    player_movements.append((x, y))

        prev_frame = blurred

        # Fake AI shot detection
        if np.random.rand() > 0.98:
            shot_count += 1
            cv2.putText(frame, "Shot Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        out.write(frame)

    cap.release()
    out.release()

    report = {
        "total_movements": len(player_movements),
        "total_shots": shot_count,
        "improvement_suggestions": "Improve footwork, increase reaction speed."
    }

    return output_path, report
