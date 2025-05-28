import React, { useRef, useEffect } from 'react';
import { io } from 'socket.io-client';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const socketRef = useRef(null);

  // Dimensions & JPEG quality
  const WIDTH = 320;
  const HEIGHT = 240;
  const QUALITY = 0.6;  // between 0.0 and 1.0

  useEffect(() => {
    // 1) Connect to backend
    socketRef.current = io('http://localhost:5000');

    // 2) Start webcam at specified resolution
    navigator.mediaDevices.getUserMedia({
      video: { width: WIDTH, height: HEIGHT }
    }).then(stream => {
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    });

    // 3) Sending loop control
    let busy = false;

    // 4) Receive annotated frames
    socketRef.current.on('annotated', data => {
      const img = new Image();
      img.src = data;
      img.onload = () => {
        const ctx = canvasRef.current.getContext('2d');
        ctx.drawImage(img, 0, 0);
        busy = false;  // ready for next
      };
    });

    // 5) Function to send the next frame
    const sendNext = () => {
      if (busy) return;
      busy = true;

      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, WIDTH, HEIGHT);

      const frame = canvas.toDataURL('image/jpeg', QUALITY);
      socketRef.current.emit('frame', frame);
    };

    // 6) Kick off at ~10 FPS
    const timer = setInterval(sendNext, 100);

    return () => {
      clearInterval(timer);
      socketRef.current.disconnect();
    };
  }, []);

  return (
    <div>
      <h1>YOLOv8 Real-Time Object Detection & Tracking</h1>
      <video
        ref={videoRef}
        style={{ display: 'none' }}
        width={WIDTH}
        height={HEIGHT}
      />
      <canvas
        ref={canvasRef}
        width={WIDTH}
        height={HEIGHT}
      />
    </div>
  );
}

export default App;
