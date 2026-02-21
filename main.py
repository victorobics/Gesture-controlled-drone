python
#!/usr/bin/env python3
import cv2
import mediapipe as mp
from pymavlink import mavutil
import time

# --- Setup MediaPipe ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# --- MAVLink Connection ---
# serial0 es el alias para el UART de la RPi Zero 2 W (GPIO 14/15)
try:
    master = mavutil.mavlink_connection('/dev/serial0', baud=57600)
    master.wait_heartbeat() # Espera a confirmar conexión con el dron
    print("Link to DarwinFPV F411: ACTIVE")
except Exception as e:
    print(f"Serial Error: {e}. Running in Simulation Mode")
    master = None

def send_nav_command(command, p7_val=0):
    """Envía comandos de navegación (Takeoff/Land) via MAVLink"""
    if master:
        master.mav.command_long_send(
            master.target_system, master.target_component,
            command, 0, 0, 0, 0, 0, 0, 0, p7_val
        )

def count_fingers(hand_landmarks):
    """Lógica para detectar cuántos dedos están levantados (Botones Virtuales)"""
    tips = [8, 12, 16, 20] # Índices de las puntas de los dedos
    count = 0
    # Pulgar (basado en coordenada X para mano derecha/izquierda)
    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x: count += 1
    # Otros 4 dedos (basado en coordenada Y: punta más alta que el nudillo)
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            count += 1
    return count

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    print("--- SYSTEM READY: STAND BY ---")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 1. Prioridad: GESTOS (CONTROL MANUAL)
        hand_results = hands.process(rgb_frame)
        
        if hand_results.multi_hand_landmarks:
            for hand_lms in hand_results.multi_hand_landmarks:
                fingers = count_fingers(hand_lms)
                
                if fingers == 5: # PALMA ABIERTA = BOTÓN DESPEGAR
                    print("GESTURE: OPEN PALM -> TAKING OFF")
                    if master:
                        master.arducopter_arm() # Armar motores
                        send_nav_command(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, p7_val=1.2)
                
                elif fingers == 0: # PUÑO CERRADO = BOTÓN ATERRIZAR
                    print("GESTURE: FIST -> LANDING")
                    send_nav_command(mavutil.mavlink.MAV_CMD_NAV_LAND)
        
        else:
            # 2. Si no hay manos: SEGUIMIENTO DE CARA (AUTO-FOLLOW)
            face_results = face_detection.process(rgb_frame)
            if face_results.detections:
                for det in face_results.detections:
                    bbox = det.location_data.relative_bounding_box
                    center_x = bbox.xmin + (bbox.width / 2)
                    
                    # Lógica simple de centrado (Yaw)
                    if center_x < 0.4: print("AUTO_FOLLOW: ROTATE LEFT")
                    elif center_x > 0.6: print("AUTO_FOLLOW: ROTATE RIGHT")
                    else: print("AUTO_FOLLOW: TARGET CENTERED")
            else:
                # 3. Sin objetivos: MODO SEGURO (HOVER)
                print("MODE: SAFE HOVER (Stabilizing)")

        time.sleep(0.05) # Evita sobrecalentamiento de la RPi Zero 2

    cap.release()

if __name__ == "__main__":
    main()
