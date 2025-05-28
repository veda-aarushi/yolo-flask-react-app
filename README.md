# YOLO Flask React App

A real-time object detection and tracking web application using YOLOv8, Flask-SocketIO, and React.

---

## 🚀 Features

* **Real-time detection** of objects via webcam
* **SORT-based tracking** with unique IDs
* **Low-latency** streaming with optimized frame size and JPEG compression
* **Pure-Python tracker** (no native builds)
* **Docker-ready** (optional)

---

## 🔧 Tech Stack

* **Backend**: Python, Flask, Flask-SocketIO, Ultralytics YOLOv8, FilterPy SORT, OpenCV, NumPy
* **Frontend**: React, Socket.IO client, HTML5 video & canvas

---

## 📝 Prerequisites

* **Python 3.9+**
* **Node.js 16+ & npm**
* **(Optional) Docker & Docker Compose**

---

## 🛠️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/veda-aarushi/yolo-flask-react-app.git
cd yolo-flask-react-app
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# Windows:
.
```

## ⚡ Usage

### Running without Docker

**Backend** (tab 1):

```bash
cd backend
venv\Scripts\Activate.ps1  # Windows
# OR source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python app.py
```

**Frontend** (tab 2):

```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` and allow camera access. Live detections will appear on the canvas.

### Running with Docker

```bash
docker-compose up --build
```

* Backend on port **5000**
* Frontend on port **3000**

---

## 📁 Project Structure

```
yolo-flask-react-app/
├── backend/
│   ├── app.py          # Flask-SocketIO server
│   ├── sort.py         # Pure-Python SORT tracker
│   ├── utils.py        # frame encode/decode helpers
│   └── requirements.txt
└── frontend/
    ├── public/         # static HTML
    └── src/
        ├── index.js    # React entry point
        └── App.js      # optimized video loop & canvas
```

---

## 📦 Dockerfiles

* **backend/Dockerfile**: Builds the Flask-SocketIO server. It starts from a slim Python image, installs build tools (CMake, compilers), copies and installs Python dependencies, and runs `app.py` on port 5000.
* **frontend/Dockerfile**: Uses a Node.js Alpine image, installs npm dependencies, copies source files, runs `npm run build`, and serves the static React build on port 3000 using the `serve` package.

## 🤝 Contributing

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. Feel free to use and modify.
