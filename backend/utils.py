# backend/utils.py
import cv2, base64, numpy as np

def decode_frame(data_url: str) -> np.ndarray:
    _, encoded = data_url.split(',',1)
    img_data = base64.b64decode(encoded)
    arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

def encode_frame(frame: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', frame)
    jpg = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{jpg}"

def draw_tracks(frame: np.ndarray, tracks: np.ndarray) -> np.ndarray:
    for x1,y1,x2,y2,tid in tracks.astype(int):
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(frame, str(tid), (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return frame
