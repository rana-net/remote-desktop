import socket
import struct
import cv2
import mss
import numpy as np
import pickle
import time
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
import pyautogui

mouse = MouseController()
keyboard = KeyboardController()

screen_width, screen_height = pyautogui.size()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))
server_socket.listen(1)

print("Waiting for connection...")
client_socket, addr = server_socket.accept()
print("Connected to:", addr)

with mss.mss() as sct:
    while True:
        try:
            screenshot = sct.grab(sct.monitors[1])
            img = np.array(screenshot)

            img = cv2.resize(img, (480, 270))

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
            _, buffer = cv2.imencode('.jpg', img, encode_param)

            data = buffer.tobytes()
            message = struct.pack("Q", len(data)) + data
            client_socket.sendall(message)

            # Receive control
            client_socket.settimeout(0.001)
            try:
                control_data = client_socket.recv(1024)
                if control_data:
                    event = pickle.loads(control_data)

                    if event["type"] == "move":
                        mouse.position = (event["x"], event["y"])

                    elif event["type"] == "click":
                        mouse.click(Button.left)

                    elif event["type"] == "key":
                        key = event["key"]

                        try:
                            keyboard.press(key)
                            keyboard.release(key)
                        except:
                            # Special keys
                            if key == "space":
                                keyboard.press(Key.space)
                                keyboard.release(Key.space)
                            elif key == "enter":
                                keyboard.press(Key.enter)
                                keyboard.release(Key.enter)

            except:
                pass

            time.sleep(0.03)

        except Exception as e:
            print("Sender Error:", e)
            break

client_socket.close()
server_socket.close()