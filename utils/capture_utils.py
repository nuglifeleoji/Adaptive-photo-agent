import cv2
import os
from datetime import datetime

class PhotoCapturer:
    def __init__(self, save_dir="captured_photos", img_format="jpg"):
        self.save_dir = save_dir
        self.img_format = img_format
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def capture_and_save(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.save_dir, f"photo_{timestamp}.{self.img_format}")
        try:
            success = cv2.imwrite(file_path, frame)
            if not success:
                print(f"[ERROR] Failed to save photo at {file_path}")
                return None
            print(f"[INFO] Photo saved at {file_path}")
            return file_path
        except Exception as e:
            print(f"[ERROR] Exception saving photo: {e}")
            return None

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
            if path:
                print(f"Photo saved at {path}")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
