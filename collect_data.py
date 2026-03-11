import cv2
import mediapipe as mp
import numpy as np
import os
import time

# Settings
DATA_DIR = "dataset"
NUM_IMAGES = 50  # Number of samples per gesture
SQUARE_SIZE = 400 # Display window size

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

def normalize_landmarks(hand_landmarks):
    """Normalize landmarks: relative to wrist (landmark 0)"""
    landmarks = []
    # Base landmark (wrist) is used as the origin (0, 0)
    base_x = hand_landmarks.landmark[0].x
    base_y = hand_landmarks.landmark[0].y
    
    for lm in hand_landmarks.landmark:
        landmarks.append(lm.x - base_x)
        landmarks.append(lm.y - base_y)
    
    return np.array(landmarks)

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    gesture_name = input("Enter gesture name (e.g. THANK YOU, PLEASE, A, B): ").upper()
    save_path = os.path.join(DATA_DIR, gesture_name)
    os.makedirs(save_path, exist_ok=True)

    cap = cv2.VideoCapture(0)
    print(f"\n--- COLLECTING FOR: {gesture_name} ---")
    print("Prepare your hand... collection starts in 3 seconds.")
    time.sleep(3)

    count = 0
    while count < NUM_IMAGES:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1) # Mirror
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw for visual feedback
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Capture landmarks
                normalized = normalize_landmarks(hand_landmarks)
                
                # Save as NPY
                npy_filename = os.path.join(save_path, f"{count}.npy")
                np.save(npy_filename, normalized)
                count += 1
                
                cv2.putText(frame, f"Collected: {count}/{NUM_IMAGES}", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("SignSpeak - Data Collector (Press Q to quit)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nSuccessfully collected {count} samples for '{gesture_name}'!")

if __name__ == "__main__":
    main()
