from enum import unique
import os
from time import monotonic
import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, flash, redirect, jsonify, request, session, logging, url_for, Response, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, AdminLoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import threading
import time
import cv2
from ultralytics import YOLO
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta


def generate_time_slots(start_hour=8, end_hour=12):
    slots = []
    for hour in range(start_hour, end_hour):
        start_time = datetime.strptime(f"{hour}:00", "%H:%M")
        end_time = start_time + timedelta(hours=1)
        time_slot = f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"
        slots.append(time_slot)
    return slots


app = Flask(__name__)

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/kitsw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists('secret.key'):
    with open('secret.key', 'wb') as f:
        f.write(Fernet.generate_key())

with open('secret.key', 'rb') as f:
    encryption_key = f.read()

cipher_suite = Fernet(encryption_key)

db = SQLAlchemy(app)

class TrafficData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    direction=db.Column(db.String(10), nullable=False)
    vehicle_count=db.Column(db.Integer)
    timestamp=db.Column(db.Text)

model = YOLO('yolov8n.pt')

video_path = None
cap_detection = None
cap_stream = None
detection_active = threading.Event()
detection_paused = threading.Event()
streaming_active = threading.Event()
data_lock = threading.Lock()
traffic_data = pd.DataFrame(columns=['timestamp', 'vehicle_count'])

class EncryptedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('You have successfully logged in.', "success")
            session['logged_in'] = True
            session['email'] = user.email
            session['userid'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            flash('Username or Password Incorrect', "danger")
    return render_template('login.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin_login/', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        if username == "admin@gmail.com" and password == "admin":
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('ahome'))
        else:
            flash('Username or Password Incorrect', "danger")
    return render_template('admin.html', form=form)

@app.route('/ahome/')
def ahome():
    return render_template('adminHome.html')

@app.route('/viewTraffic/')
def view_traffic():
    data=TrafficData.query.all()
    return render_template('viewTraffic.html',data=data)

@app.route('/viewBrand/')
def viewBrand():
    mobileList = db.session.query(User).all()
    return render_template('viewBrand.html', myList=mobileList)

@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    id = request.args.get('id')
    m = db.session.query(User).get(id)
    db.session.delete(m)
    db.session.commit()
    return redirect(url_for('viewBrand'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/', methods=['GET'])
def upload():
    return render_template('upload1.html')
@app.route('/upload1/', methods=['POST'])
def upload_file():
    global video_path, cap_detection, cap_stream, traffic_data

    if 'fileName' not in request.files:
        return jsonify(success=False, error="No file part")

    file = request.files['fileName']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(saved_path)

        video_path = saved_path
        cap_detection = cv2.VideoCapture(video_path)
        cap_stream = cv2.VideoCapture(video_path)
        traffic_data = pd.DataFrame(columns=['timestamp', 'vehicle_count'])

        return redirect(url_for('show'))  # Redirect to the show route
    else:
        return jsonify(success=False, error="Invalid file type.")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_list)


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

@app.route('/show')
def show():
    print("HI....................")
    return render_template('start_video.html', prediction="N/A")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global detection_thread
    if not detection_active.is_set():
        detection_active.set()
        detection_paused.clear()
        streaming_active.set()
        detection_thread = threading.Thread(target=detect_vehicles, daemon=True)
        detection_thread.start()
        return jsonify({"message": "Vehicle detection started."})
    else:
        return jsonify({"message": "Vehicle detection is already running."})

@app.route('/pause_detection', methods=['POST'])
def pause_detection():
    if detection_active.is_set() and not detection_paused.is_set():
        detection_paused.set()
        return jsonify({"message": "Vehicle detection paused."})
    else:
        return jsonify({"message": "Vehicle detection is not active or already paused."})

@app.route('/resume_detection', methods=['POST'])
def resume_detection():
    if detection_active.is_set() and detection_paused.is_set():
        detection_paused.clear()
        return jsonify({"message": "Vehicle detection resumed."})
    else:
        return jsonify({"message": "Vehicle detection is not paused or not active."})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global detection_thread
    if detection_active.is_set():
        detection_active.clear()
        detection_paused.clear()
        streaming_active.clear()
        if detection_thread is not None:
            detection_thread.join()
        
        return jsonify({"message": "Vehicle detection stopped."})
    else:
        return jsonify({"message": "Vehicle detection is not active."})

@app.route('/predict_traffic', methods=['POST'])
def predict_traffic():
    prediction = train_and_predict()
    return jsonify({"prediction": prediction})

@app.route('/chart/',methods=['GET','POST'])
def chart():
    return render_template('chart.html')

@app.route('/getAll',methods=['GET','POST'])
def getAll():
    return render_template('multi_route_traffic.html')
if __name__ == '__main__':
    with app.app_context():
        if not TrafficData.query.first():
            time_slots=generate_time_slots()
            TrafficData.query.delete()
            db.session.commit()
            sample_data=[
                TrafficData(direction="North",timestamp=time_slots[0],vehicle_count=120),
                TrafficData(direction="South",timestamp=time_slots[1],vehicle_count=150),
                TrafficData(direction="East",timestamp=time_slots[2],vehicle_count=180),
                TrafficData(direction="West",timestamp=time_slots[3],vehicle_count=130),
            ]
            db.session.add_all(sample_data)
            db.session.commit()
            print("Sample data added to the database.")
    app.run(debug=True)
