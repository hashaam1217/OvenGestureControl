import cv2
import mediapipe as mp
from gesture_recognition import GestureRecognizer

def main():
    # Initialize MediaPipe Gesture Recognizer
    recognizer = GestureRecognizer()

    # OpenCV Video Capture
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert OpenCV frame to MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Call the recognizer to perform gesture recognition asynchronously
        recognizer.recognize_async(mp_image, cap.get(cv2.CAP_PROP_POS_MSEC))

        # Display the frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

