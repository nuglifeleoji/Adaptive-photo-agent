import cv2
import numpy as np

class SubjectDetector:
    def __init__(self):
        # 加载OpenCV预训练的人脸检测模型
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # 若需要进行姿势估计，可以自行处理这里的简单实现，或者使用手动方式计算位置
        # 使用 cv2 进行简单的头部和身体检测可以采用其它方法，但 OpenCV 自身并不提供姿势估计
        self.body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = {}

        # 使用人脸检测
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            x, y, w, h = faces[0]  # 只使用第一个检测到的面
            center_x, center_y = x + w / 2, y + h / 2
            results['bbox'] = (center_x / frame.shape[1], center_y / frame.shape[0], w / frame.shape[1], h / frame.shape[0])

        # 使用上半身检测模拟身体姿势
        bodies = self.body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 100))
        if len(bodies) > 0:
            x, y, w, h = bodies[0]  # 只使用第一个检测到的身体
            results['turn_body_left'] = x < frame.shape[1] / 3  # 模拟简单的姿势判断（靠左即为向左转）
            results['turn_body_right'] = x + w > frame.shape[1] * 2 / 3  # 向右转的情况

        # 返回面部和身体信息（简单模拟）
        return results

