from flask import Flask, render_template, Response, session, jsonify
from camera import VideoCamera

app = Flask(__name__)


# Store cameras for each direction
cameras = {
    'north': VideoCamera('static/uploads/input1.mp4'),
    'south': VideoCamera('static/uploads/input1.mp4'),
    'east': VideoCamera('static/uploads/input1.mp4'),
    'west': VideoCamera('static/uploads/input1.mp4')
}

@app.route("/")
def index():
    session['logged_in'] = True  # Auto-login for now
    return render_template("traffic_dashboard.html")

@app.route("/video_feed/<direction>")
def video_feed(direction):
    if direction in cameras:
        return Response(cameras[direction].get_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Invalid direction", 404

@app.route("/predict_traffic/<direction>", methods=["POST"])
def predict_traffic(direction):
    if direction in cameras:
        count = cameras[direction].predict_traffic()
        return jsonify({'prediction': count})
    return jsonify({'error': 'Invalid direction'}), 400

if __name__ == "__main__":
    app.run(debug=True)
