from utils.dialogue_manager import DialogueManager

def test_dialogue():
    api_key = "sk-crrrxsgwputbfxhvilcgzafqyrkzevfmcmocyupkbpcivnrh"
    dialogue_manager = DialogueManager(api_key)
    
    # 测试多个对话场景
    test_cases = [
        "我想拍一张侧脸照",
        "换个复古滤镜试试",
        "现在可以拍照了",
        "请让我向左转一点"
    ]
    
    for user_input in test_cases:
        print(f"\n用户: {user_input}")
        ai_response, commands = dialogue_manager.chat_with_ai(user_input)
        print(f"AI: {ai_response}")
        print(f"解析的指令: {commands}")
        print("-" * 50)

if __name__ == "__main__":
    test_dialogue()
