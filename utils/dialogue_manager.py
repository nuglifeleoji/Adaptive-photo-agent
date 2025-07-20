import requests
import json
import time
from typing import Dict, List, Tuple, Optional

class DialogueManager:
    def __init__(self, api_key: "sk-crrrxsgwputbfxhvilcgzafqyrkzevfmcmocyupkbpcivnrh", base_url: str = "https://api.siliconflow.cn"):
        self.api_key = api_key
        self.base_url = base_url
        self.conversation_history: List[Dict] = []
        self.system_prompt = """你是一个智能拍照助手，能够帮助用户拍出更好的照片。你的职责包括：

1. 理解用户的拍照需求（如角度、滤镜、风格等）
2. 给出具体的拍照建议（如"请向左转一点"、"保持微笑"等）
3. 根据用户反馈调整拍照策略
4. 在合适的时机建议拍照

请用简洁、友好的语气回复，并明确指出具体的拍照指令。"""

    def add_message(self, role: str, content: str):
        """添加消息到对话历史"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # 保持对话历史在合理长度内（避免token过多）
        if len(self.conversation_history) > 10:
            # 保留system prompt和最近的对话
            self.conversation_history = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history[-8:]

    def chat_with_ai(self, user_message: str) -> Tuple[str, Dict]:
        """
        与AI对话，返回AI回复和解析的指令
        
        Returns:
            Tuple[str, Dict]: (AI回复文本, 解析的指令字典)
        """
        try:
            # 添加用户消息到历史
            self.add_message("user", user_message)
            
            # 准备请求数据
            messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "Qwen/QwQ-32B",
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            # 调用DeepSeek API
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                
                # 添加AI回复到历史
                self.add_message("assistant", ai_response)
                
                # 解析指令
                parsed_commands = self._parse_commands(ai_response)
                
                return ai_response, parsed_commands
            else:
                print(f"[ERROR] API调用失败: {response.status_code} - {response.text}")
                return "抱歉，我现在无法回应，请稍后再试。", {}
                
        except Exception as e:
            print(f"[ERROR] 对话管理错误: {e}")
            return "抱歉，出现了一些问题，请稍后再试。", {}

    def _parse_commands(self, ai_response: str) -> Dict:
        """
        解析AI回复中的拍照指令
        
        Returns:
            Dict: 包含各种指令的字典
        """
        commands = {
            "action": None,  # 主要动作：take_photo, adjust_pose, change_filter, wait
            "pose_adjustment": None,  # 姿势调整：left, right, back, closer, smile
            "filter_change": None,  # 滤镜切换
            "timing": None,  # 时机：now, wait, countdown
            "message": ai_response  # 原始AI回复
        }
        
        # 解析拍照指令
        if any(word in ai_response.lower() for word in ["拍照", "拍一张", "take photo", "capture"]):
            commands["action"] = "take_photo"
            
        # 解析姿势调整
        if any(word in ai_response.lower() for word in ["向左", "left", "往左"]):
            commands["pose_adjustment"] = "left"
        elif any(word in ai_response.lower() for word in ["向右", "right", "往右"]):
            commands["pose_adjustment"] = "right"
        elif any(word in ai_response.lower() for word in ["向后", "back", "往后"]):
            commands["pose_adjustment"] = "back"
        elif any(word in ai_response.lower() for word in ["向前", "closer", "往前"]):
            commands["pose_adjustment"] = "closer"
        elif any(word in ai_response.lower() for word in ["微笑", "smile"]):
            commands["pose_adjustment"] = "smile"
            
        # 解析滤镜切换
        filter_keywords = {
            "natural": ["自然", "natural"],
            "bright": ["明亮", "bright"],
            "vintage": ["复古", "vintage"],
            "bw": ["黑白", "black and white", "bw"],
            "hdr": ["hdr"],
            "lomo": ["lomo"]
        }
        
        for filter_name, keywords in filter_keywords.items():
            if any(keyword in ai_response.lower() for keyword in keywords):
                commands["filter_change"] = filter_name
                break
                
        # 解析时机
        if any(word in ai_response.lower() for word in ["现在", "立即", "now", "立即"]):
            commands["timing"] = "now"
        elif any(word in ai_response.lower() for word in ["等一下", "稍等", "wait"]):
            commands["timing"] = "wait"
        elif any(word in ai_response.lower() for word in ["倒计时", "countdown"]):
            commands["timing"] = "countdown"
            
        return commands

    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []

    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        if not self.conversation_history:
            return "对话历史为空"
        
        summary = "最近的对话：\n"
        for msg in self.conversation_history[-5:]:  # 显示最近5条
            role = "用户" if msg["role"] == "user" else "AI"
            summary += f"{role}: {msg['content'][:50]}...\n"
        return summary

# 使用示例
if __name__ == "__main__":
    # 替换为你的API密钥
    api_key = "sk-crrrxsgwputbfxhvilcgzafqyrkzevfmcmocyupkbpcivnrh"
    
    dialogue_manager = DialogueManager(api_key)
    
    # 测试对话
    user_input = "我想拍一张侧脸照"
    ai_response, commands = dialogue_manager.chat_with_ai(user_input)
    
    print(f"用户: {user_input}")
    print(f"AI: {ai_response}")
    print(f"解析的指令: {commands}") 