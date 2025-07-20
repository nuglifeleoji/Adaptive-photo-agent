import time
from typing import Dict, List, Optional
from utils.dialogue_manager import DialogueManager

class SmartPromptGenerator:
    def __init__(self, api_key: str):
        self.dialogue_manager = DialogueManager(api_key)
        self.last_prompt_time = 0
        self.prompt_interval = 15  # 增加间隔到15秒，减少过于频繁的提示
        self.last_detection_state = {}
        self.prompt_history = []
        self.consecutive_similar_prompts = 0  # 连续相似提示计数
        
    def generate_smart_prompt(self, detection_result: Dict, frame_info: Dict = None) -> Optional[str]:
        """
        根据检测结果生成智能提示
        
        Args:
            detection_result: 来自SubjectDetector的检测结果
            frame_info: 可选的帧信息（如分辨率等）
            
        Returns:
            Optional[str]: 智能提示文本，如果没有新提示则返回None
        """
        current_time = time.time()
        
        # 检查是否需要生成新提示
        if current_time - self.last_prompt_time < self.prompt_interval:
            return None
            
        # 检查检测状态是否有显著变化
        if not self._has_significant_change(detection_result):
            return None
            
        # 构建分析提示
        analysis_prompt = self._build_analysis_prompt(detection_result, frame_info)
        
        try:
            # 调用AI生成智能提示
            ai_response, _ = self.dialogue_manager.chat_with_ai(analysis_prompt)
            
            # 记录提示历史
            self.prompt_history.append({
                'time': current_time,
                'detection': detection_result.copy(),
                'prompt': ai_response
            })
            
            # 保持历史记录在合理长度
            if len(self.prompt_history) > 10:
                self.prompt_history = self.prompt_history[-10:]
                
            self.last_prompt_time = current_time
            self.last_detection_state = detection_result.copy()
            
            return ai_response
            
        except Exception as e:
            print(f"[ERROR] 智能提示生成失败: {e}")
            return None
    
    def _has_significant_change(self, current_detection: Dict) -> bool:
        """检查检测结果是否有显著变化"""
        if not self.last_detection_state:
            return True
            
        # 检查人脸检测状态变化
        if current_detection.get('face_detected') != self.last_detection_state.get('face_detected'):
            return True
            
        # 检查微笑状态变化
        if current_detection.get('smile') != self.last_detection_state.get('smile'):
            return True
            
        # 检查身体姿势变化
        if current_detection.get('body_pose') != self.last_detection_state.get('body_pose'):
            return True
            
        # 检查头部姿态变化（如果变化超过阈值）
        current_head = current_detection.get('head_pose', {})
        last_head = self.last_detection_state.get('head_pose', {})
        
        if current_head and last_head:
            yaw_diff = abs(current_head.get('yaw', 0) - last_head.get('yaw', 0))
            pitch_diff = abs(current_head.get('pitch', 0) - last_head.get('pitch', 0))
            
            if yaw_diff > 0.1 or pitch_diff > 0.1:  # 头部转动超过阈值
                return True
                
        return False
    
    def _build_analysis_prompt(self, detection_result: Dict, frame_info: Dict = None) -> str:
        """构建分析提示"""
        
        # 基础状态描述
        status_parts = []
        
        if detection_result.get('face_detected'):
            status_parts.append("检测到人脸")
        else:
            status_parts.append("未检测到人脸")
            
        if detection_result.get('smile'):
            status_parts.append("正在微笑")
        else:
            status_parts.append("没有微笑")
            
        # 身体姿势
        body_pose = detection_result.get('body_pose')
        if body_pose:
            if body_pose == 'left':
                status_parts.append("身体偏左")
            elif body_pose == 'right':
                status_parts.append("身体偏右")
            elif body_pose == 'center':
                status_parts.append("身体居中")
                
        # 头部姿态
        head_pose = detection_result.get('head_pose')
        if head_pose:
            yaw = head_pose.get('yaw', 0)
            pitch = head_pose.get('pitch', 0)
            
            if abs(yaw) > 0.08:
                if yaw > 0:
                    status_parts.append("头部偏左")
                else:
                    status_parts.append("头部偏右")
                    
            if abs(pitch) > 0.08:
                if pitch > 0:
                    status_parts.append("头部偏低")
                else:
                    status_parts.append("头部偏高")
        
        # 位置信息
        bbox = detection_result.get('bbox')
        if bbox:
            center_x, center_y = bbox[0], bbox[1]
            if center_x < 0.4:
                status_parts.append("位置偏左")
            elif center_x > 0.6:
                status_parts.append("位置偏右")
            else:
                status_parts.append("位置适中")
                
            if center_y < 0.4:
                status_parts.append("位置偏上")
            elif center_y > 0.6:
                status_parts.append("位置偏下")
            else:
                status_parts.append("位置适中")
        
        status_text = "，".join(status_parts)
        
        # 构建AI分析提示
        analysis_prompt = f"""作为专业的拍照助手，请分析当前用户的拍照状态并给出简洁的改进建议。

当前状态：{status_text}

请根据以上状态，给出：
1. 具体的调整建议（如"请向左转一点"、"请保持微笑"等）
2. 拍照时机建议（如"现在可以拍照了"、"再调整一下"等）
3. 构图建议（如"距离再近一点"、"角度再偏一点"等）

请用简洁、直接的语气回复，不要冗长。如果用户状态已经很好了，请直接说"现在可以拍照了"或"保持这个姿势，准备拍照"等。"""
        
        return analysis_prompt
    
    def simplify_prompt(self, full_prompt: str) -> str:
        """简化提示内容，提取关键信息"""
        
        # 提取关键动作词
        key_actions = []
        
        # 位置调整
        if "向左" in full_prompt or "left" in full_prompt.lower():
            key_actions.append("请向右转")
        elif "向右" in full_prompt or "right" in full_prompt.lower():
            key_actions.append("请向左转")
        elif "向后" in full_prompt or "back" in full_prompt.lower():
            key_actions.append("请向前")
        elif "向前" in full_prompt or "closer" in full_prompt.lower():
            key_actions.append("请向后")
            
        # 微笑提示
        if "微笑" in full_prompt or "smile" in full_prompt.lower():
            key_actions.append("请保持微笑")
            
        # 拍照建议
        if any(keyword in full_prompt for keyword in ["现在可以拍照", "准备拍照", "可以拍照了", "拍照时机"]):
            key_actions.append("现在可以拍照了")
            
        # 头部调整
        if "头部偏左" in full_prompt:
            key_actions.append("请向右转头")
        elif "头部偏右" in full_prompt:
            key_actions.append("请向左转头")
        elif "头部偏低" in full_prompt:
            key_actions.append("请抬头")
        elif "头部偏高" in full_prompt:
            key_actions.append("请低头")
            
        # 如果没有具体动作，给出状态反馈
        if not key_actions:
            if "检测到人脸" in full_prompt and "微笑" in full_prompt:
                key_actions.append("状态很好，保持微笑")
            elif "检测到人脸" in full_prompt:
                key_actions.append("请保持微笑")
            else:
                key_actions.append("请面向摄像头")
                
        # 返回简化的提示
        return "，".join(key_actions) if key_actions else "请调整姿势"

    def get_recent_prompts(self, count: int = 5) -> List[Dict]:
        """获取最近的提示历史"""
        return self.prompt_history[-count:] if self.prompt_history else []
    
    def reset_prompt_history(self):
        """重置提示历史"""
        self.prompt_history = []
        self.last_detection_state = {}
        self.last_prompt_time = 0

# 使用示例
if __name__ == "__main__":
    api_key = "sk-crrrxsgwputbfxhvilcgzafqyrkzevfmcmocyupkbpcivnrh"
    prompt_generator = SmartPromptGenerator(api_key)
    
    # 模拟检测结果
    test_detection = {
        'face_detected': True,
        'smile': False,
        'body_pose': 'left',
        'head_pose': {'yaw': 0.1, 'pitch': 0.05, 'roll': 0.02},
        'bbox': (0.3, 0.5, 0.4, 0.6)
    }
    
    prompt = prompt_generator.generate_smart_prompt(test_detection)
    if prompt:
        print(f"智能提示: {prompt}")
    else:
        print("暂无新提示") 