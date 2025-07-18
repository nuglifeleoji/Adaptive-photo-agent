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

        if current_bbox is None:
            if return_offset_ok:
                return "Adjust position to be visible", False
            else:
                return "Adjust position to be visible"

        advice = self.advisor.compute_offset_advice(self.user_reference_bbox, current_bbox)
        offset_ok = advice == "Good position, hold"

        if offset_ok:
            if detection.get('smile', False):
                if return_offset_ok:
                    return "Good position, hold", True
                else:
                    return "Good position, hold"
            else:
                if return_offset_ok:
                    return "Hold position and smile", True
                else:
                    return "Hold position and smile"
        else:
            if return_offset_ok:
                return advice, False
            else:
                return advice
