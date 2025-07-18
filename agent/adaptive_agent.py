import cv2
from detectors.subject_detector import SubjectDetector
from viewpoint.viewpoint_generator import ViewpointAdvisor

class AdaptivePhotoAgent:
    def __init__(self, user_image_dir, target_size='half-body'):
        self.detector = SubjectDetector()
        self.advisor = ViewpointAdvisor(threshold=0.20, target_size=target_size)
        self.user_reference_bbox = self._compute_reference_bbox(user_image_dir)

    def set_target_size(self, target_size):
        self.advisor.set_target_size(target_size)

    def _compute_reference_bbox(self, user_image_dir):
        # Placeholder: Extract preferred composition from uploaded images if desired
        return (0.5, 0.5, 0.4, 0.6)

    def generate_advice(self, frame, return_offset_ok=False):
        detection = self.detector.detect(frame)
        current_bbox = detection.get('bbox', None)
        advice_list = []

        if not detection.get('face_detected', False):
            advice_list.append("No face detected, please face the camera")
            if return_offset_ok:
                return ", ".join(advice_list), False
            else:
                return ", ".join(advice_list)

        # 位置建议
        advice = self.advisor.compute_offset_advice(self.user_reference_bbox, current_bbox)
        if advice != "Good position, hold":
            advice_list.append(advice)

        # 微笑建议
        if not detection.get('smile', False):
            advice_list.append("Please smile")

        # 头部朝向建议
        head_pose = detection.get('head_pose')
        if head_pose:
            yaw = head_pose.get('yaw', 0)
            pitch = head_pose.get('pitch', 0)
            # 简单阈值判断
            if yaw > 0.08:
                advice_list.append("Turn your head left")
            elif yaw < -0.08:
                advice_list.append("Turn your head right")
            if pitch > 0.08:
                advice_list.append("Lower your head")
            elif pitch < -0.08:
                advice_list.append("Raise your head")

        # 身体朝向建议
        body_pose = detection.get('body_pose')
        if body_pose == 'left':
            advice_list.append("Turn your body right")
        elif body_pose == 'right':
            advice_list.append("Turn your body left")

        if not advice_list:
            advice_list.append("Good position, hold")

        offset_ok = (advice == "Good position, hold") and detection.get('smile', False)
        if return_offset_ok:
            return ", ".join(advice_list), offset_ok
        else:
            return ", ".join(advice_list)
