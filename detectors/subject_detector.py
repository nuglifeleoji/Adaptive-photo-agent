"""
Subject Detector - Face Detection and Pose Analysis Module
=========================================================

This module provides comprehensive face detection and pose analysis using:
- OpenCV Haar Cascades for face, smile, and body detection
- MediaPipe Face Mesh for detailed head pose estimation
- Multi-modal analysis combining facial expressions and body positioning

Key features:
- Real-time face detection with bounding box coordinates
- Smile detection for optimal capture timing
- Head pose estimation (pitch, yaw, roll)
- Body pose classification (left, right, center)
"""

import cv2
import numpy as np
import mediapipe as mp
import os

class SubjectDetector:
    def __init__(self):
        """
        Initialize the Subject Detector with OpenCV cascades and MediaPipe.
        
        Sets up:
        - Haar cascade classifiers for face, smile, and upper body detection
        - MediaPipe Face Mesh for detailed facial landmark detection
        - Configuration for real-time processing
        """
        # Initialize OpenCV Haar cascade classifiers
        try:
            haar_dir = cv2.data.haarcascades
        except AttributeError:
            # Fallback path for older OpenCV versions
            haar_dir = os.path.join(os.path.dirname(cv2.__file__), 'data', '')
            
        self.face_cascade = cv2.CascadeClassifier(os.path.join(haar_dir, 'haarcascade_frontalface_default.xml'))
        self.smile_cascade = cv2.CascadeClassifier(os.path.join(haar_dir, 'haarcascade_smile.xml'))
        self.body_cascade = cv2.CascadeClassifier(os.path.join(haar_dir, 'haarcascade_upperbody.xml'))
        
        # Initialize MediaPipe Face Mesh for head pose estimation
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

    def detect(self, frame):
        """
        Perform comprehensive detection on input frame.
        
        Args:
            frame: Input BGR image from camera
            
        Returns:
            dict: Detection results containing:
                - face_detected (bool): Whether a face was found
                - smile (bool): Whether person is smiling
                - head_pose (dict): Head orientation {yaw, pitch, roll}
                - body_pose (str): Body position ('left', 'right', 'center')
                - bbox (tuple): Face bounding box (center_x, center_y, width, height) as ratios
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = {
            'face_detected': False,
            'smile': False,
            'head_pose': None,  # Head orientation angles
            'body_pose': None,  # Body position classification
            'bbox': None        # Face bounding box coordinates
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

            # MediaPipe head pose estimation
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_results = self.face_mesh.process(rgb_frame)
            if mp_results.multi_face_landmarks:
                # Use first detected face landmarks
                face_landmarks = mp_results.multi_face_landmarks[0]
                
                # Extract key landmarks for head pose estimation
                # Note: This is a simplified approach. More accurate estimation
                # could use solvePnP with 3D model points
                nose_tip = face_landmarks.landmark[1]      # Nose tip
                left_eye = face_landmarks.landmark[33]     # Left eye corner
                right_eye = face_landmarks.landmark[263]   # Right eye corner
                mouth_left = face_landmarks.landmark[61]   # Left mouth corner
                mouth_right = face_landmarks.landmark[291] # Right mouth corner
                
                # Estimate yaw (left-right head rotation)
                eye_dx = right_eye.x - left_eye.x
                mouth_dx = mouth_right.x - mouth_left.x
                yaw = (eye_dx + mouth_dx) / 2
                
                # Estimate pitch (up-down head tilt) and roll (head rotation)
                pitch = (nose_tip.y - (left_eye.y + right_eye.y) / 2)
                roll = (left_eye.y - right_eye.y)
                
                results['head_pose'] = {'pitch': pitch, 'yaw': yaw, 'roll': roll}

        # Upper body detection for body pose classification
        bodies = self.body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 100))
        if len(bodies) > 0:
            x, y, w, h = bodies[0]  # Take first detected body
            
            # Classify body position based on horizontal placement
            if x < frame.shape[1] / 3:
                results['body_pose'] = 'left'    # Body positioned in left third
            elif x + w > frame.shape[1] * 2 / 3:
                results['body_pose'] = 'right'   # Body positioned in right third
            else:
                results['body_pose'] = 'center'  # Body centered

        return results

