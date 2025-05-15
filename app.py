from flask import Flask
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ CORS configuration — allow your Vercel frontend
CORS(app, resources={r"/*": {"origins": "https://castfrontend.vercel.app"}})

# ✅ Use threading async_mode (eventlet removed)
socketio = SocketIO(
    app,
    cors_allowed_origins="https://castfrontend.vercel.app",
    async_mode='threading',
    logger=True,
    engineio_logger=True
)

@app.route('/')
def index():
    return "Server is running"

@socketio.on('connect')
def handle_connect():
    print("🟢 Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("🔴 Client disconnected")

@socketio.on('join-room')
def handle_join(room):
    print(f"[🟢] Admin joined room: {room}")
    join_room(room)

@socketio.on('screen-data')
def handle_screen(data):
    room = data.get("room")
    print(f"[📺] Emitting screen-data to room: {room}")
    emit('screen-data', data.get("data"), room=room)

@socketio.on('audio-data')
def handle_audio(data):
    room = data.get("room")
    print(f"[🔊] Emitting audio-data to room: {room}")
    emit('audio-data', data.get("data"), room=room)

@socketio.on('video-data')
def handle_video(data):
    room = data.get("room")
    print(f"[📷] Emitting video-data to room: {room}")
    emit('video-data', data.get("data"), room=room)

if __name__ == '__main__':
    # ✅ Use dynamic port for Render hosting
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
