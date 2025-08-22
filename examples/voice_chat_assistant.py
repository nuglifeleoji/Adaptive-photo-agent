from utils.voice_interactions import listen_for_command
from utils.speech_utils import SpeechHelper
from utils.dialogue_manager import DialogueManager

def main():
    api_key = "sk-crrrxsgwputbfxhvilcgzafqyrkzevfmcmocyupkbpcivnrh"
    dialogue_manager = DialogueManager(api_key)
    speaker = SpeechHelper(rate=220)

    print("AI语音对话助手已启动，说'关机'即可退出。")
    while True:
        user_text = listen_for_command(timeout=5, phrase_time_limit=8)
        if not user_text:
            print("没有识别到语音，请重试。"); continue
        print(f"你说：{user_text}")
        if "关机" in user_text or "退出" in user_text or "quit" in user_text:
            print("AI助手已关机。再见！")
            speaker.speak("AI助手已关机。再见！")
            break

        ai_reply, _ = dialogue_manager.chat_with_ai(user_text)
        if not ai_reply or len(ai_reply.strip()) == 0:
            ai_reply = "对不起，我没有听清，请再说一遍。"
        print(f"AI：{ai_reply}")
        speaker.engine.say(ai_reply)
        speaker.engine.runAndWait()

    # 等待队列清空
    import time
    while not speaker.speak_queue.empty():
        time.sleep(0.5)

if __name__ == "__main__":
    main() 