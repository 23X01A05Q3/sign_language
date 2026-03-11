import cv2
import mediapipe as mp
import numpy as np
import os

DATASET_DIR = "dataset"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True)

for label in os.listdir(DATASET_DIR):

    label_path = os.path.join(DATASET_DIR, label)

    for img_name in os.listdir(label_path):

        if img_name.endswith(".jpg") or img_name.endswith(".png"):

            img_path = os.path.join(label_path, img_name)

            image = cv2.imread(img_path)

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:

                for hand_landmarks in results.multi_hand_landmarks:

                    base_x = hand_landmarks.landmark[0].x
                    base_y = hand_landmarks.landmark[0].y

                    landmarks = []

                    for lm in hand_landmarks.landmark:

                        landmarks.append(lm.x - base_x)
                        landmarks.append(lm.y - base_y)

                    landmarks = np.array(landmarks)

                    save_path = os.path.join(
                        label_path,
                        img_name.replace(".jpg", ".npy").replace(".png", ".npy")
                    )

                    np.save(save_path, landmarks)

print("Landmark extraction completed with normalization!")