import cv2
import mediapipe as mp

# STEP 1: Import the necessary modules.
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# STEP 2: Create a HandLandmarker object.
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# STEP 3: Open the webcam.
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

while cap.isOpened():
    # STEP 4: Read a frame from the webcam.
    ret, frame = cap.read()
    if not ret:
        break

    # STEP 5: Convert BGR frame to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # STEP 6: Detect hand landmarks from the frame.
    results = mp_hands.process(rgb_frame)

    # If hand landmarks are detected.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw lines between hand landmarks to visualize hand shape.
            connections = [(0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                           (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
                           (0, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
                           (0, 13), (13, 14), (14, 15), (15, 16),  # Ring finger
                           (0, 17), (17, 18), (18, 19), (19, 20)]  # Little finger

            for connection in connections:
                landmark1 = hand_landmarks.landmark[connection[0]]
                landmark2 = hand_landmarks.landmark[connection[1]]

                x1, y1 = int(landmark1.x * frame.shape[1]), int(landmark1.y * frame.shape[0])
                x2, y2 = int(landmark2.x * frame.shape[1]), int(landmark2.y * frame.shape[0])

                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw a line between hand landmarks

    # Display the frame.
    cv2.imshow('Hand Landmarks', frame)

    # Break the loop when 'q' is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()

