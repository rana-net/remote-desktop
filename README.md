# 🖥️ Remote Desktop System (Python)

A real-time remote desktop application built using Python sockets that enables live screen streaming and remote control (mouse + keyboard) over a network.

---

## 🚀 Features

* 📡 Real-time screen streaming using OpenCV
* 🖱️ Remote mouse control
* ⌨️ Remote keyboard input
* ⚡ Low-latency transmission using optimized compression
* 🔄 Custom TCP protocol with frame size handling
* 🌐 Works over LAN and Internet (via ngrok)

---

## 🛠️ Tech Stack

* Python
* OpenCV (cv2)
* Socket Programming (TCP)
* MSS (screen capture)
* NumPy
* Pynput (input control)

---

## ⚙️ How It Works

1. Sender captures screen frames using MSS
2. Frames are compressed (JPEG) and serialized
3. Data is sent over TCP socket with size prefix
4. Receiver reconstructs frames and displays using OpenCV
5. Mouse and keyboard events are sent back to sender

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Sender

```bash
cd sender
python server.py
```

### 3. Run Receiver

```bash
cd receiver
python client.py
```

---

## 🌍 Remote Access (ngrok)

```bash
ngrok tcp 9999
```

Update client:

```python
host_ip = "your-ngrok-url"
port = your-port
```

---

## ⚡ Performance Notes

* FPS depends on resolution and compression
* Lower resolution = lower latency
* TCP ensures reliability but adds delay
* Real-world systems use UDP + H264 for better performance

---

## 📌 Future Improvements

* UDP-based streaming (low latency)
* H264 encoding
* Multi-client support
* GUI interface
* Authentication system



---
