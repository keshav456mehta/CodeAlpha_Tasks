# 🚀 Real-Time Object Detection & Tracking with YOLOv8

A real-time computer vision project that performs **object detection and multi-object tracking** using **YOLOv8**, **ByteTrack**, and **OpenCV**. The system supports both webcam and video inputs and displays object labels, tracking IDs, FPS, and class-wise statistics in real time.

## ✨ Features

- 🎯 Real-time object detection with YOLOv8
- 🔄 Multi-object tracking using ByteTrack
- 📹 Supports webcam and video files
- 🆔 Persistent tracking IDs
- 📊 Live FPS monitoring and object count
- 🏷️ Optional confidence score display
- 🎨 Color-coded bounding boxes and labels
- ⚡ Fast and lightweight implementation

## 🛠️ Tech Stack

- Python
- OpenCV
- Ultralytics YOLOv8
- ByteTrack

## 📂 Project Structure

```
├── detect.py
├── requirements.txt
├── yolov8n.pt
├── yolov8s.pt
└── one.mp4
```

## 📦 Installation

### 1️⃣ Create a Virtual Environment

```bash
python -m venv yolo_env
```

### 2️⃣ Activate the Environment

**Windows**

```bash
yolo_env\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Required Packages

```bash
pip install ultralytics opencv-python
```

## ▶️ Usage

### Webcam Input

```bash
python detect.py
```

### Video File Input

```bash
python detect.py --source one.mp4
```

### Display Confidence Scores

```bash
python detect.py --source one.mp4 --show-conf
```

## 📸 Output

- Bounding boxes with object labels
- Unique tracking IDs
- Real-time FPS display
- Per-class object count breakdown
- Support for multiple objects simultaneously

## 📋 Requirements

```text
ultralytics>=8.0.0
opencv-python>=4.8.0
```

## 🎥 Demo

The project can detect and track multiple objects in real time from a webcam or video stream while maintaining unique IDs for each object.

---

⭐ Developed as **Task 4: Object Detection & Tracking** for the **CodeAlpha Artificial Intelligence Internship**.
