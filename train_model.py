import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

DATA_DIR = "dataset"
MODEL_PATH = "sign_model.pkl"

def retrain_model():
    print("--- SignSpeak AI: Training Neural Engine ---")
    data = []
    labels = []
    
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] '{DATA_DIR}' directory not found.")
        return

    gesture_folders = [f for f in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, f))]
    
    if not gesture_folders:
        print("[ERROR] No gesture folders found in 'dataset/'. Please add some data first!")
        return

    print(f"Detected Gestures: {', '.join(gesture_folders)}")

    for label in gesture_folders:
        label_path = os.path.join(DATA_DIR, label)
        samples_count = 0
        for file in os.listdir(label_path):
            if file.endswith(".npy"):
                path = os.path.join(label_path, file)
                try:
                    landmarks = np.load(path, allow_pickle=True)
                    # Support only 42 values (flat landmarks)
                    if len(landmarks) == 42:
                        data.append(landmarks)
                        labels.append(label)
                        samples_count += 1
                except Exception as e:
                    print(f" - Error loading {file}: {e}")
        
        print(f" Loaded {samples_count} samples for '{label}'")

    if not data:
        print("[ERROR] No valid data found to train on.")
        return

    X = np.array(data)
    y = np.array(labels)

    # Split: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"\nTraining on {len(X_train)} samples...")
    model = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    score = accuracy_score(y_test, y_pred)

    print(f"\n--- SUCCESS ---")
    print(f"Final Accuracy: {score*100:.2f}%")
    print("\nDetailed Report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to '{MODEL_PATH}'")
    print("Restart your server.py to apply changes!")

if __name__ == "__main__":
    retrain_model()