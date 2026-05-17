import cv2
import numpy as np
import os

print("=== TRAINING FACE MODEL ===")

face_data_dir = 'engine/auth/face_data'

if not os.path.exists(face_data_dir):
    print("ERROR: No face data found!")
    print("Please run train_face.py first")
    exit()

images = []
labels = []

for filename in os.listdir(face_data_dir):
    if filename.endswith('.jpg'):
        img_path = os.path.join(face_data_dir, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
            labels.append(1)  # Label 1 = authorized user (you)

if len(images) == 0:
    print("ERROR: No face images found in", face_data_dir)
    exit()

print(f"Training with {len(images)} face images...")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, np.array(labels))
recognizer.save('engine/auth/face_data.yml')

print("Model trained and saved to engine/auth/face_data.yml")
print("\nFace authentication is now ready!")
print("Update engine/auth/recoganize.py to enable it")
