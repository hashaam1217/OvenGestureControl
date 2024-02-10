import cv2
import mediapipe as mp

def detect_and_print_gestures(frame):
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Detect hand gestures and print to terminal
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(rgb_frame)

    # If hand gestures are detected
    if results.multi_handedness:
        for idx, hand_handedness in enumerate(results.multi_handedness):
            gesture_label = hand_handedness.classification[0].label
            print(f"Hand {idx + 1} gesture: {gesture_label}")

