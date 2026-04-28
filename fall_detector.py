import cv2
import mediapipe as mp
import numpy as np

class FallDetectionModel:
    def __init__(self, confidence=0.5):
        # Initialize the MediaPipe Pose model
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=confidence,
            min_tracking_confidence=confidence
        )

    def process_frame(self, frame):
        """Processes a single frame, draws skeletal landmarks, and checks for falls."""
        fall_detected = False
        
        # Convert BGR (OpenCV) to RGB (MediaPipe)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        
        # Convert back to BGR for drawing
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            # Draw the skeleton on the frame
            self.mp_drawing.draw_landmarks(
                image_bgr, 
                results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
            
            # Extract specific landmarks (Y-coordinates: 0.0 is top, 1.0 is bottom)
            landmarks = results.pose_landmarks.landmark
            nose_y = landmarks[self.mp_pose.PoseLandmark.NOSE.value].y
            left_ankle_y = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y
            right_ankle_y = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y
            
            avg_ankle_y = (left_ankle_y + right_ankle_y) / 2.0
            
            # Fall Heuristic: If the head is vertically very close to the ankles
            vertical_distance = abs(nose_y - avg_ankle_y)
            
            if vertical_distance < 0.2: 
                fall_detected = True
                
        return image_bgr, fall_detected