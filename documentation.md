# AI Buoys Smart Buoys Documentation

## Project Overview

AI Buoys is a system of smart buoys equipped with computer vision models to detect schools of fish in real time. These autonomous buoys are deployed at sea to monitor underwater activity and relay detection data back to fishermen. The goal is to optimize fishing efforts by pinpointing high-density fish locations.

---

## Problem and Solution

Fishermen often spend hours locating viable fishing sites, which leads to wasted time, fuel, and manpower when results are poor. AI Buoys solves this by continuously scanning the surrounding waters using onboard cameras and machine learning models. When fish are detected, the buoy sends an alert with location coordinates, dramatically reducing resource waste.

---

## AI Technologies

- Computer Vision  
- YOLO-based object detection  
- Real-time video processing pipelines  

---

## Installation and Run

### Server Side

#### Getting Started

1. Clone the repository  
   ```bash
   git clone https://github.com/your-org/AIHackathon2025_AIBuoy_SmartBuoy_Backend.git
   cd AIHackathon2025_AIBuoy_SmartBuoy_Backend
   ```

2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask server  
   ```bash
   python -m flask run --host=0.0.0.0
   ```

4. Configure and run the buoy’s vision module  
   ```bash
   python -m buoy_main_cv_yolo --source <camera_or_video_path>
   ```

---

### App

1. Download the mobile or web client from the provided release assets.  
2. Open the configuration file and set the server’s base URL to your deployment endpoint.  
3. Launch the application and log in with your credentials.  
4. View real-time fish detection alerts on the map dashboard.  

---