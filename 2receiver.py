import socket
import struct
import cv2
import numpy as np
import pickle
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = "0.tcp.in.ngrok.io"  # change for ngrok
port = 13705

client_socket.connect((host_ip, port))

data = b""
payload_size = struct.calcsize("Q")

window_width = 480
window_height = 270

screen_width = 1920
screen_height = 1080

prev_time = 0


def mouse_event(event, x, y, flags, param):
    scaled_x = int(x * screen_width / window_width)
    scaled_y = int(y * screen_height / window_height)

    if event == cv2.EVENT_MOUSEMOVE:
        control = {"type": "move", "x": scaled_x, "y": scaled_y}
        client_socket.send(pickle.dumps(control))

    elif event == cv2.EVENT_LBUTTONDOWN:
        control = {"type": "click"}
        client_socket.send(pickle.dumps(control))


def key_event(key):
    try:
        if hasattr(key, 'char') and key.char:
            control = {"type": "key", "key": key.char}
        else:
            control = {"type": "key", "key": str(key)}
        client_socket.send(pickle.dumps(control))
    except:
        pass


cv2.namedWindow("Remote Screen")
cv2.setMouseCallback("Remote Screen", mouse_event)

# Keyboard listener
from pynput import keyboard

listener = keyboard.Listener(on_press=key_event)
listener.start()

while True:
    try:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet

        if len(data) < payload_size:
            break

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        if len(frame_data) == 0:
            continue

        np_data = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        if frame is None:
            continue

        # 🔥 FPS calculation
        new_time = time.time()
        fps = int(1 / (new_time - prev_time + 0.0001))
        prev_time = new_time

        # 🔥 UI Overlay
        cv2.putText(frame, f"FPS: {fps}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.putText(frame, "Press ESC to exit", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)

        cv2.imshow("Remote Screen", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    except Exception as e:
        print("Receiver Error:", e)
        break

cv2.destroyAllWindows()
client_socket.close()