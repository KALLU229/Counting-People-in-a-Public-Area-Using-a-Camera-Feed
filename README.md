# Counting-People-in-a-Public-Area-Using-a-Camera-Feed
A Streamlit-based real-time crowd counting system using YOLOv8 and DeepSORT for people detection, tracking, and counting from video or live camera feed.
This project is designed for public safety monitoring, crowd management, and surveillance applications.

## Features
Real-time people detection using YOLOv8
Multi-object tracking with DeepSORT
Entry/Exit counting
Supports video input and live camera
Streamlit dashboard with visual analytics
SQLite database for storing detection logs

## Requirements
Python 3.8 – 3.11
OS: Windows / Linux / macOS
Webcam (optional, for live camera mode)

## How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/KALLU229/Counting-People-in-a-Public-Area-Using-a-Camera-Feed.git
cd Counting-People-in-a-Public-Area-Using-a-Camera-Feed
2️⃣ Create Virtual Environment (Recommended)
python -m venv venv

Activate:
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate

3️⃣ Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Download YOLOv8 Model Weights
Model files are not included in the repository due to size limitations.
Download manually:
pip install ultralytics
YOLOv8 will auto-download weights on first run
OR place yolov8n.pt in the project root.
5️⃣ Run the Streamlit Application
streamlit run app.py

Open browser:
http://localhost:8501

## Input Options

Video File: Use the provided input5.mp4
Live Camera: Requires a connected webcam or IP camera
⚠️ Note: Live camera works only on local machine or server with camera access.

## Output
Crowd count visualization on dashboard
Saved frames/videos in output/ directory
Detection logs stored in SQLite database

## Author
Kanishka Kumar Shaw
B.Tech (CSE), Narula Institute of Technology 2027

## Licensed By kalludon
This project is for academic and research purposes.
⭐ If this project helped you, give it a star!
