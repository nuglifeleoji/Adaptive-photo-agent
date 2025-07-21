from utils.voice_interactions import listen_for_command
from utils.speech_utils import SpeechHelper
from utils.dialogue_manager import DialogueManager

def main():
    api_key =  "sk-crrrxsgwputbfxhvilcgzafqyrkzevfmcmocyupkbpcivnrh"
    dialogue_manager = DialogueManager(api_key)
    speaker = SpeechHelper()

    print("语音对话助手已启动，说'退出'结束对话。")
    while True:
        # 1. 语音识别
        user_text = listen_for_command(timeout=5, phrase_time_limit=8)
        if not user_text:
            print("没有识别到语音，请重试。")
            continue
        print(f"你说：{user_text}")
        if "退出" in user_text or "quit" in user_text:
            print("对话结束。")
            break

        # 2. AI对话
        ai_reply, _ = dialogue_manager.chat_with_ai(user_text)
        print(f"AI：{ai_reply}")

        # 3. 语音播报
        speaker.speak(ai_reply)

if __name__ == "__main__":
    main()
