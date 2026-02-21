python
#!/usr/bin/env python3
import cv2
import mediapipe as mp
from pymavlink import mavutil
import time

# --- Setup MediaPipe ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Added Face Detection for the "Follow" mode when no hands are visible
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# --- MAVLink Connection ---
# serial0 is the RPi Zero's UART. 57600 is standard for MAVLink
try:
    master = mavutil.mavlink_connection('/dev/serial0', baud=57600)
    print("Link to DarwinFPV F411: ACTIVE")
except:
    print("Running in Simulation/No Serial Mode")

def get_follow_command(face_center_x, frame_width):
    """
    Calculate Yaw/Roll to keep the person in the center of the frame.
    Simple P-controller logic (Proportional).
    """
    center_threshold = 0.15 # 15% margin
    error = (face_center_x / frame_width) - 0.5
    
    if abs(error) > center_threshold:
        if error > 0: return "YAW_RIGHT"
        else: return "YAW_LEFT"
    return "STABILIZED_FOLLOW"

def main():
    cap = cv2.VideoCapture(0)
    # RPi Camera resolution should be low to keep FPS high on Pi Zero
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 1. Try to find HANDS first (Manual Control)
        hand_results = hands.process(rgb_frame)
        
        if hand_results.multi_hand_landmarks:
            # Gesture logic here (Thumb Up, Palm, etc.)
            print("Control Mode: GESTURE_ACTIVE")
        else:
            # 2. If no hands, try to find FACE (Auto-Follow Mode)
            face_results = face_detection.process(rgb_frame)
            if face_results.detections:
                for detection in face_results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    center_x = bbox.xmin + (bbox.width / 2)
                    command = get_follow_command(center_x, 1.0)
                    print(f"Control Mode: AUTO_FOLLOW -> {command}")
            else:
                # 3. Last resort: Safety Hover
                print("Control Mode: FAILSAFE_HOVER")

        # Don't overload the CPU, 20fps is plenty for a 3-inch drone
        time.sleep(0.05)

    cap.release()

if __name__ == "__main__":
    main()
