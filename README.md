# 🚨 AI Vision Safety Hub

**Automated CCTV Anomaly Detection & Crisis Routing for Hospitality Venues**

Built for the **Solution Challenge 2026 - Build with AI**, this prototype transforms passive CCTV cameras into active sentinels. Using real-time computer vision, the system monitors video feeds for physical anomalies (like slip-and-falls) and leverages Google's Gemini API to instantly generate context-aware, localized emergency alerts.

---

## 🌟 Key Features
* **Zero-Latency Anomaly Detection:** Uses skeletal tracking to detect rapid vertical drops indicative of a fall or injury.
* **Context-Aware Escalation:** Integrates with the Google Gemini API (`gemini-1.5-flash`) to generate professional, situation-specific emergency dispatch alerts.
* **Live Incident Dashboard:** A clean, dark-mode web interface built with Streamlit for security personnel to monitor feeds and view incoming alerts.
* **Hardware Agnostic:** Processes standard video formats, allowing it to act as an intelligent layer over existing hotel CCTV infrastructure.

---

## 🛠️ Tech Stack
* **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Computer Vision:** [OpenCV](https://opencv.org/) & [Google MediaPipe](https://developers.google.com/mediapipe) (Pose Tracking)
* **Generative AI:** [Google Gemini API](https://ai.google.dev/)
* **Data Processing:** NumPy

---

## 📂 Project Structure

```text
├── app.py                 # The main Streamlit dashboard and application logic
├── fall_detector.py       # Custom computer vision model utilizing MediaPipe Pose
├── requirements.txt       # Python dependencies required to run the project
└── README.md              # Project documentation
```
## 🚀 Getting Started

Follow these instructions to set up and run the AI Vision Safety Hub on your local machine.

### Prerequisites
* Python 3.8 or higher installed on your system.
* A valid **Google Gemini API Key**. You can get one from Google AI Studio.
* A sample CCTV video clip (e.g., `.mp4`) to simulate a camera feed.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ai-vision-safety-hub.git](https://github.com/YOUR_USERNAME/ai-vision-safety-hub.git)
   cd ai-vision-safety-hub
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. **Start the application:**
   Ensure your virtual environment is active, then run:
   ```bash
   streamlit run app.py
   ```

2. **Configure the Dashboard:**
   * The app will automatically open in your default web browser (usually at `http://localhost:8501`).
   * In the sidebar, paste your Gemini API Key.
   * Upload a sample CCTV video file.

3. **Simulate:**
   * Watch the live feed as the AI draws skeletal landmarks. When a fall is detected, the system will pause briefly to query the Gemini API and output a high-priority red alert on the dashboard.

## 🔮 Future Development
* **Multi-Camera Spatial Mapping:** Tracking an emergency as it moves across different camera zones in a large resort.
* **Direct EMS Integration:** Automatically forwarding critical Gemini alerts directly to local ambulance or fire dispatch systems.
* **Expanded Threat Detection:** Integrating YOLOv8 to detect environmental hazards like smoke, fire, or unattended baggage.

---
**Team Arkz | Solution Challenge 2026**