class ViewpointAdvisor:
    def __init__(self, threshold=0.20, target_size='half-body'):
        self.x_threshold = threshold  # For backward compatibility
        self.y_threshold = 0.36       # Fixed as per user calibration
        self.target_size = target_size

    def compute_offset_advice(self, reference_bbox, current_bbox):
        ref_x, ref_y, ref_w, ref_h = reference_bbox
        cur_x, cur_y, cur_w, cur_h = current_bbox

        advice = []

        x_offset = cur_x - ref_x
        y_offset = cur_y - ref_y

        if abs(x_offset) > self.x_threshold:
            if x_offset > 0:
                advice.append("Move left")
            else:
                advice.append("Move right")

        if abs(y_offset) > self.y_threshold:
            if y_offset > 0:
                advice.append("Move back")
            else:
                advice.append("Move closer")

        size_tolerance = 0.15
        target_ratios = {
            'full-body': 0.3,
            'half-body': 0.5,
            'portrait': 0.7
        }
        target_ratio = target_ratios.get(self.target_size, 0.5)
        current_ratio = cur_h

        if abs(current_ratio - target_ratio) > size_tolerance:
            if current_ratio < target_ratio:
                advice.append("Move closer to fill the frame")
            else:
                advice.append("Move back to adjust size")

        if not advice:
            return "Good position, hold"
        else:
            return ", ".join(advice)
