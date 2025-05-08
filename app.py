from flask import Flask
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return "Server is running"

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

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
    socketio.run(app, host="0.0.0.0", port=10000)