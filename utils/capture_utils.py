import cv2
import os
from datetime import datetime

class PhotoCapturer:
    def __init__(self, save_dir="captured_photos"):
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def capture_and_save(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.save_dir, f"photo_{timestamp}.jpg")
        cv2.imwrite(file_path, frame)
        return file_path

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    capturer = PhotoCapturer()

    print("Press SPACE to capture, press q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Photo Capture Test", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # 空格键拍照
            path = capturer.capture_and_save(frame)
            print(f"Photo saved at {path}")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
