import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

tip_ids = [4, 8, 12, 16, 20]

with mp_hands.Hands() as hands:

    while True:
        success, img = cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)

        lm_list = []
        finger_count = 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((cx, cy))

                # Check fingers
                if lm_list:

                    fingers = []

                    # Thumb
                    if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0]-1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    # Other fingers
                    for id in range(1,5):

                        if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id]-2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    finger_count = fingers.count(1)

                mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        cv2.putText(
            img,
            f'Fingers: {finger_count}',
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            3
        )

        cv2.imshow("Finger Counter", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()