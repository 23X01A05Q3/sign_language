import cv2
import os

gesture_name = "hello"
save_path = f"dataset/{gesture_name}"

os.makedirs(save_path, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break

    cv2.imshow("Capture Gesture", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        img_name = f"{save_path}/{count}.jpg"
        cv2.imwrite(img_name, frame)
        print("Saved:", img_name)
        count += 1

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()