import cv2
import numpy as np

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
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
    return output

def apply_filter_by_style(frame, style_choice):
    if style_choice == "natural":
        return apply_beauty_filter(frame, smoothing=10, brightness=10, contrast=10)
    elif style_choice == "bright":
        return apply_beauty_filter(frame, smoothing=20, brightness=30, contrast=20)
    elif style_choice == "vintage":
        return apply_vintage_filter(frame)
    elif style_choice == "bw":
        return apply_bw_filter(frame)
    elif style_choice == "hdr":
        return apply_hdr_filter(frame)
    elif style_choice == "lomo":
        return apply_lomo_filter(frame)
    else:
        return apply_beauty_filter(frame, smoothing=15, brightness=15, contrast=15)