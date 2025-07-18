import cv2
import numpy as np
import mediapipe as mp
import os

class SubjectDetector:
    def __init__(self):
        # OpenCV人脸和微笑检测
        try:
            haar_dir = cv2.data.haarcascades
        except AttributeError:
            haar_dir = os.path.join(os.path.dirname(cv2.__file__), 'data', '')
        self.face_cascade = cv2.CascadeClassifier(os.path.join(haar_dir, 'haarcascade_frontalface_default.xml'))
        self.smile_cascade = cv2.CascadeClassifier(os.path.join(haar_dir, 'haarcascade_smile.xml'))
        self.body_cascade = cv2.CascadeClassifier(os.path.join(haar_dir, 'haarcascade_upperbody.xml'))
        # mediapipe人脸mesh用于头部姿态估计
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = {
            'face_detected': False,
            'smile': False,
            'head_pose': None,  # (pitch, yaw, roll)
            'body_pose': None,  # left/right/center
            'bbox': None
        }

        # 人脸检测
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            x, y, w, h = faces[0]
            center_x, center_y = x + w / 2, y + h / 2
            results['face_detected'] = True
            results['bbox'] = (center_x / frame.shape[1], center_y / frame.shape[0], w / frame.shape[1], h / frame.shape[0])

            # 微笑检测（在人脸区域内）
            roi_gray = gray[y:y+h, x:x+w]
            smiles = self.smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=22, minSize=(25, 25))
            if len(smiles) > 0:
                results['smile'] = True

            # mediapipe头部姿态估计
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_results = self.face_mesh.process(rgb_frame)
            if mp_results.multi_face_landmarks:
                # 取第一个人脸
                face_landmarks = mp_results.multi_face_landmarks[0]
                # 取关键点用于头部姿态估计（如鼻尖、眼角、嘴角等）
                # 这里只做简单示例，实际可用solvePnP精确估计
                nose_tip = face_landmarks.landmark[1]
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]
                mouth_left = face_landmarks.landmark[61]
                mouth_right = face_landmarks.landmark[291]
                # 简单估算yaw（左右转头）
                eye_dx = right_eye.x - left_eye.x
                mouth_dx = mouth_right.x - mouth_left.x
                yaw = (eye_dx + mouth_dx) / 2
                # pitch/roll可用y坐标差估算
                pitch = (nose_tip.y - (left_eye.y + right_eye.y) / 2)
                roll = (left_eye.y - right_eye.y)
                results['head_pose'] = {'pitch': pitch, 'yaw': yaw, 'roll': roll}

        # 上半身检测模拟身体姿势
        bodies = self.body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 100))
        if len(bodies) > 0:
            x, y, w, h = bodies[0]
            if x < frame.shape[1] / 3:
                results['body_pose'] = 'left'
            elif x + w > frame.shape[1] * 2 / 3:
                results['body_pose'] = 'right'
            else:
                results['body_pose'] = 'center'

        return results

