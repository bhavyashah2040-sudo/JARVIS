import cv2
import os
import numpy as np

# Create directory if not exists
os.makedirs('engine/auth/face_data', exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("ERROR: Camera not found!")
    exit()

print("=== FACE CAPTURE ===")
print("Look at the camera...")
print("We will capture 50 photos of your face")
print("Press Q to quit anytime")
print("")

count = 0
total = 50

while count < total:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5
    )

    for (x, y, w, h) in faces:
        count += 1
        face_img = gray[y:y+h, x:x+w]
        # Save face image
        cv2.imwrite(f'engine/auth/face_data/face_{count}.jpg', face_img)
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f'Capturing: {count}/{total}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print(f"Captured {count}/{total}")

    cv2.imshow('Face Capture - Press Q to quit', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

if count >= 10:
    print(f"\nCaptured {count} face images successfully!")
    print("Now run: python train_model.py")
else:
    print(f"\nOnly captured {count} images - need at least 10")
    print("Make sure your face is clearly visible to camera")
