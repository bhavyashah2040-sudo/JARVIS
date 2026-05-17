import cv2

def AuthenticateFace():
    print("[FaceAuth] Starting face authentication...")

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    try:
        recognizer.read('engine/auth/face_data.yml')
    except:
        print("[FaceAuth] No trained model found! Run train_face.py and train_model.py first")
        return 0

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("[FaceAuth] Camera not found!")
        return 0

    authenticated = 0
    attempts = 0
    max_attempts = 50  # ~5 seconds

    print("[FaceAuth] Look at the camera...")

    while attempts < max_attempts:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5
        )

        for (x, y, w, h) in faces:
            face_region = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face_region)
            print(f"[FaceAuth] Confidence: {confidence:.1f} (lower is better, <70 = match)")

            if confidence < 70:
                authenticated = 1
                print("[FaceAuth] Face matched!")
                break

        if authenticated:
            break

        attempts += 1

    cam.release()
    cv2.destroyAllWindows()

    if not authenticated:
        print("[FaceAuth] Face not recognized!")

    return authenticated
