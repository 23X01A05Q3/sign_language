import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Finger tip indices
tip_ids = [4, 8, 12, 16, 20]

def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        success, img = cap.read()
        if not success:
            break
            
        h, w, c = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        gesture = "UNKNOWN"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((cx, cy))

                if lm_list:
                    fingers = []

                    # Thumb state (complex because it moves horizontally)
                    # Check if thumb is open (distance from thumb tip to pinky base is large)
                    if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0]-1][0] if lm_list[tip_ids[0]][0] > lm_list[0][0] else lm_list[tip_ids[0]][0] < lm_list[tip_ids[0]-1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    # Other 4 fingers
                    for id in range(1, 5):
                        if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id]-2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    finger_count = fingers.count(1)

                    # 1. OK Gesture (Thumb and Index tips close, others up)
                    dist_ok = get_distance(lm_list[4], lm_list[8])
                    if dist_ok < 30 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                        gesture = "OK"
                    
                    # 2. I LOVE YOU Gesture (🤟 - Thumb, Index, Pinky up)
                    elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                        gesture = "I LOVE YOU"
                        
                    # 3. ROCK Gesture (🤘 - Index and Pinky up)
                    elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                        gesture = "ROCK"
                    
                    # 4. CALL ME (🤙 - Thumb, Pinky)
                    elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                        gesture = "CALL ME"
                    
                    # 5. L-SHAPE (Index and Thumb)
                    elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                        gesture = "L-SHAPE"

                    # 6. THUMBS UP
                    elif fingers[0] == 1 and finger_count == 1 and lm_list[4][1] < lm_list[3][1]:
                        gesture = "THUMBS UP"
                        
                    # 7. THUMBS DOWN
                    elif fingers[0] == 1 and finger_count == 1 and lm_list[4][1] > lm_list[3][1]:
                        gesture = "THUMBS DOWN"

                    # 8. PEACE (✌️) vs U-SHAPE (Together)
                    elif fingers[1] == 1 and fingers[2] == 1 and finger_count == 2:
                        dist_im = get_distance(lm_list[8], lm_list[12])
                        if dist_im > 40:
                            gesture = "PEACE"
                        else:
                            gesture = "U-SHAPE"

                    # 9. THREE / W-SHAPE
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and finger_count == 3:
                        gesture = "W-SHAPE"
                    
                    # 10. FOUR
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and finger_count == 4:
                        gesture = "FOUR"

                    # 11. HELLO (5)
                    elif finger_count == 5:
                        gesture = "HELLO"

                    # 12. STOP / FIST
                    elif finger_count == 0:
                        gesture = "STOP"
                    
                    # 13. YES / POINT
                    elif fingers[1] == 1 and finger_count == 1:
                        gesture = "YES"
                    
                    else:
                        gesture = "UNKNOWN"

                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # UI Overlay
        cv2.rectangle(img, (0, 0), (400, 100), (0, 0, 0), -1)
        cv2.putText(img, f'SIGN: {gesture}', (20, 70), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 0), 2)

        cv2.imshow("Sign Language recognition Pro", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
