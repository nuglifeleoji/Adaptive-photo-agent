import cv2
import numpy as np
import os
from datetime import datetime

def apply_beauty_filter(image, smoothing=30, brightness=30, contrast=30):
    blurred = cv2.GaussianBlur(image, (0, 0), smoothing / 10)
    smooth_image = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
    img_float = np.float32(smooth_image)
    img_float = img_float * (1 + contrast / 100.0)
    img_float = img_float + brightness
    img_float = np.clip(img_float, 0, 255)
    beautified = np.uint8(img_float)
    return beautified

def apply_vintage_filter(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = hsv[..., 1] * 0.3
    vintage = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return vintage

def apply_bw_filter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 保证输出3通道
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def apply_hdr_filter(image):
    hdr = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)
    return hdr

def apply_lomo_filter(image):
    rows, cols = image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols / 2)
    kernel_y = cv2.getGaussianKernel(rows, rows / 2)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    output = np.copy(image)
    for i in range(3):
        output[:, :, i] = output[:, :, i] * mask
    output = np.clip(output, 0, 255).astype(np.uint8)
    return output

# 可选：增加冷色调和暖色调滤镜
def apply_cool_filter(image):
    cool = cv2.addWeighted(image, 0.7, np.full_like(image, (255, 255, 255)), 0.3, 0)
    return cool

def apply_warm_filter(image):
    warm = cv2.addWeighted(image, 0.7, np.full_like(image, (0, 128, 255)), 0.3, 0)
    return warm

def apply_filter_by_style(frame, style_choice):
    try:
        if style_choice == "natural":
            return apply_beauty_filter(frame, smoothing=10, brightness=10, contrast=10)
        elif style_choice == "bright":
            return apply_beauty_filter(frame, smoothing=20, brightness=30, contrast=20)
        elif style_choice == "vintage":
            return apply_vintage_filter(frame)
        elif style_choice == "bw" or style_choice == "black and white" or style_choice == "黑白":
            return apply_bw_filter(frame)
        elif style_choice == "hdr":
            return apply_hdr_filter(frame)
        elif style_choice == "lomo":
            return apply_lomo_filter(frame)
        elif style_choice == "cool":
            return apply_cool_filter(frame)
        elif style_choice == "warm":
            return apply_warm_filter(frame)
        else:
            return apply_beauty_filter(frame, smoothing=15, brightness=15, contrast=15)
    except Exception as e:
        print(f"[FILTER ERROR] {e}")
        return frame

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