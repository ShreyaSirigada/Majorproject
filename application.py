
import threading
import time
import cv2
from ultralytics import YOLO
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime


# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Global variables
video_path = 'input1.mp4'
cap_detection = cv2.VideoCapture(video_path)
cap_stream = cv2.VideoCapture(video_path)
traffic_data = pd.DataFrame(columns=['timestamp', 'vehicle_count'])
data_lock = threading.Lock()
detection_active = threading.Event()
detection_paused = threading.Event()
streaming_active = threading.Event()
detection_thread = None

def detect_vehicles():
    global detection_active, detection_paused, traffic_data
    while detection_active.is_set():
        if detection_paused.is_set():
            time.sleep(1)
            continue

        ret, frame = cap_detection.read()
        if not ret:
            cap_detection.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        results = model(frame)[0]
        vehicle_count = sum(1 for box in results.boxes if int(box.cls[0]) in [2, 3, 5, 7])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with data_lock:
            traffic_data = pd.concat([traffic_data, pd.DataFrame([[timestamp, vehicle_count]], columns=traffic_data.columns)], ignore_index=True)

        time.sleep(1)

def gen_frames():
    while streaming_active.is_set():
        ret, frame = cap_stream.read()
        if not ret:
            cap_stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        results = model(frame)[0]
        for box in results.boxes:
            cls_id = int(box.cls[0])
            if cls_id in [2, 3, 5, 7]:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, model.names[cls_id], (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

def train_and_predict():
    with data_lock:
        if len(traffic_data) < 10:
            return "Not enough data"
        df = traffic_data.copy()
        df['minute'] = pd.to_datetime(df['timestamp']).dt.minute
        X = df[['minute']]
        y = df['vehicle_count']
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        next_minute = (datetime.now().minute + 1) % 60
        prediction = model_lr.predict([[next_minute]])[0]
        return max(0, int(prediction))