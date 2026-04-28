import streamlit as st
import cv2
import tempfile
import time
import os
import google.generativeai as genai
from fall_detector import FallDetectionModel

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Vision Safety Hub", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a professional dark dashboard look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .alert-box { padding: 20px; background-color: #7f1d1d; border-left: 5px solid #ef4444; border-radius: 5px; margin-top: 20px;}
    .alert-text { font-family: monospace; font-size: 1.2rem; color: #fca5a5; }
    </style>
""", unsafe_allow_html=True)

st.title("🚨 AI Vision Safety Hub")
st.subheader("Automated CCTV Anomaly Detection & Crisis Routing")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("System Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.sidebar.file_uploader("Upload CCTV Footage (MP4)", type=["mp4", "mov"])

# --- GEMINI AI SETUP ---
def generate_emergency_alert(location):
    """Calls Gemini API to generate a context-aware alert."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"A physical slip and fall has just been detected by the AI CCTV system in the {location}. Generate a short, urgent, professional 2-sentence alert to be dispatched to the on-site hospitality security team. Do not use hashtags."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"CRITICAL INCIDENT DETECTED. Dispatch security to {location} immediately. (AI Error: {e})"

# --- MAIN DASHBOARD LOGIC ---
if uploaded_file is not None and api_key:
    # Save the uploaded video temporarily so OpenCV can read it
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📷 Live Camera Feed: Main Lobby")
        video_placeholder = st.empty()
        
    with col2:
        st.markdown("### 🔔 System Alerts")
        alert_placeholder = st.empty()
        alert_placeholder.info("System Armed. Monitoring feed for anomalies...")

    # Initialize the model and video capture
    vision_model = FallDetectionModel(confidence=0.5)
    cap = cv2.VideoCapture(tfile.name)
    
    alert_triggered = False
    
    # Process the video frame by frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Run the frame through our custom model
        processed_frame, is_fall = vision_model.process_frame(frame)
        
        # Convert BGR back to RGB for Streamlit to display it correctly
        frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
        
        # Trigger Gemini if a fall is detected (and only do it once per video to save API calls)
        if is_fall and not alert_triggered:
            alert_placeholder.warning("⚠️ Anomaly Detected! Analyzing severity...")
            
            # Call Gemini
            gemini_response = generate_emergency_alert("Main Lobby Camera 3")
            
            # Display the generated alert using our custom CSS
            alert_html = f"""
            <div class="alert-box">
                <h4 style="color: white; margin-top:0;">🚨 CRITICAL ESCALATION</h4>
                <p class="alert-text">{gemini_response}</p>
            </div>
            """
            alert_placeholder.markdown(alert_html, unsafe_allow_html=True)
            alert_triggered = True
            
        # Control playback speed (adjust if video runs too fast/slow)
        time.sleep(0.03)

    cap.release()
    os.remove(tfile.name)
    
elif not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to arm the system.")
else:
    st.info("👈 Please upload a test video to begin the simulation.")
