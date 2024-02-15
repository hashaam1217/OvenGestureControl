import cv2

def get_video(input_id):
    camera = cv2.VideoCapture(input_id)
    while True:
        okay, frame = camera.read()
        if not okay:
            break
        cv2.imshow('video', frame)
        key = cv2.waitKey(1)
        if key == 27:  # Exit on ESC key
            break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    get_video(0)  # Use camera index 0 (default webcam)

