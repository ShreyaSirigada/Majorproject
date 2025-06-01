import cv2
from ultralytics import YOLO
import threading

class VideoCamera:
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.lock = threading.Lock()
        self.model = YOLO("yolov8n.pt")  # Replace with your trained model
        self.frame = None

    def get_frames(self):
        while True:
            success, frame = self.video.read()
            if not success:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            with self.lock:
                self.frame = frame.copy()

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def predict_traffic(self):
        with self.lock:
            if self.frame is None:
                return 0
            results = self.model(self.frame, verbose=False)
            vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
            count = 0
            for result in results:
                for cls in result.boxes.cls:
                    if int(cls.item()) in vehicle_classes:
                        count += 1
            return count
