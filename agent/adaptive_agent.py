"""
Adaptive Photo Agent - Core Intelligence Module
==============================================

This module contains the main AdaptivePhotoAgent class that coordinates
face detection, pose analysis, and photography advice generation.

The agent integrates multiple components:
- SubjectDetector: Face detection and pose analysis using OpenCV and MediaPipe
- ViewpointAdvisor: Composition and positioning guidance
- Reference bbox computation for personalized advice
"""

import cv2
from detectors.subject_detector import SubjectDetector
from viewpoint.viewpoint_generator import ViewpointAdvisor

class AdaptivePhotoAgent:
    def __init__(self, user_image_dir, target_size='half-body'):
        """
        Initialize the Adaptive Photo Agent.
        
        Args:
            user_image_dir (str): Directory containing user's reference photos
            target_size (str): Target composition size ('full-body', 'half-body', 'portrait')
        """
        self.detector = SubjectDetector()
        self.advisor = ViewpointAdvisor(threshold=0.20, target_size=target_size)
        self.user_reference_bbox = self._compute_reference_bbox(user_image_dir)

    def set_target_size(self, target_size):
        """
        Update the target composition size.
        
        Args:
            target_size (str): New target size ('full-body', 'half-body', 'portrait')
        """
        self.advisor.set_target_size(target_size)

    def _compute_reference_bbox(self, user_image_dir):
        """
        Compute reference bounding box from user's preferred photos.
        
        Args:
            user_image_dir (str): Directory with user's reference images
            
        Returns:
            tuple: Reference bbox (center_x, center_y, width, height) as ratios
            
        Note:
            Currently returns default values. Future implementation could
            analyze user's uploaded photos to learn preferred composition.
        """
        # Placeholder: Extract preferred composition from uploaded images if desired
        return (0.5, 0.5, 0.4, 0.6)

    def generate_advice(self, frame, return_offset_ok=False):
        """
        Generate photography advice based on current frame analysis.
        
        Args:
            frame: Current video frame from camera
            return_offset_ok (bool): Whether to return capture readiness status
            
        Returns:
            str or tuple: Photography advice string, optionally with capture readiness bool
            
        This method analyzes:
        - Face detection status
        - Position and composition
        - Facial expression (smile)
        - Head pose orientation
        - Body positioning
        """
        detection = self.detector.detect(frame)
        current_bbox = detection.get('bbox', None)
        advice_list = []

        # Check for face detection
        if not detection.get('face_detected', False):
            advice_list.append("No face detected, please face the camera")
            if return_offset_ok:
                return ", ".join(advice_list), False
            else:
                return ", ".join(advice_list)

        # Position and composition advice
        advice = self.advisor.compute_offset_advice(self.user_reference_bbox, current_bbox)
        if advice != "Good position, hold":
            advice_list.append(advice)

        # Smile detection and advice
        if not detection.get('smile', False):
            advice_list.append("Please smile")

        # Head pose orientation advice
        head_pose = detection.get('head_pose')
        if head_pose:
            yaw = head_pose.get('yaw', 0)
            pitch = head_pose.get('pitch', 0)
            
            # Yaw (left-right head turn) thresholds
            if yaw > 0.08:
                advice_list.append("Turn your head left")
            elif yaw < -0.08:
                advice_list.append("Turn your head right")
                
            # Pitch (up-down head tilt) thresholds
            if pitch > 0.08:
                advice_list.append("Lower your head")
            elif pitch < -0.08:
                advice_list.append("Raise your head")

        # Body positioning advice
        body_pose = detection.get('body_pose')
        if body_pose == 'left':
            advice_list.append("Turn your body right")
        elif body_pose == 'right':
            advice_list.append("Turn your body left")

        # Default positive feedback
        if not advice_list:
            advice_list.append("Good position, hold")

        # Determine if ready to capture (good position + smile)
        offset_ok = (advice == "Good position, hold") and detection.get('smile', False)
        
        if return_offset_ok:
            return ", ".join(advice_list), offset_ok
        else:
            return ", ".join(advice_list)
