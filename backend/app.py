# backend/app.py
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np
from ultralytics import YOLO
from utils import decode_frame, encode_frame, draw_tracks
from sort import Sort

# 1) App & SocketIO
app = Flask(__name__, template_folder="../frontend/public")
socketio = SocketIO(app, cors_allowed_origins="*")

# 2) Load model
MODEL = YOLO("yolov8n.pt")  # or your .pt path

# 3) Init tracker
tracker = Sort()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("frame")
def on_frame(data_url):
    img = decode_frame(data_url)
    res = MODEL(img)[0]
    dets = []
    for box in res.boxes:
        x1,y1,x2,y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        dets.append([x1,y1,x2,y2,conf])
    dets = np.array(dets) if dets else np.empty((0,5))
    tracks = tracker.update(dets)
    out = draw_tracks(img, tracks)
    emit("annotated", encode_frame(out))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
