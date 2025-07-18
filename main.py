import cv2
import time
from agent.adaptive_agent import AdaptivePhotoAgent
from utils.speech_utils import SpeechHelper, speak_prompt_non_blocking
from utils.capture_utils import PhotoCapturer
from filters.beauty_filter import apply_filter_by_style
from utils.voice_interactions import listen_for_command, parse_command  # 语音识别

def main():
    # 初始参数
    target_size = "half-body"
    style_choice = "natural"
    agent = AdaptivePhotoAgent(user_image_dir="user_photos", target_size=target_size)
    speaker = SpeechHelper()
    capturer = PhotoCapturer()
    cap = cv2.VideoCapture(0)
    stable_count = 0
    photo_taken = False

    last_command_time = time.time()
    command_interval = 3  # 每3秒监听一次语音指令

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 应用滤镜
        frame = apply_filter_by_style(frame, style_choice)
        # 智能建议
        advice, ready_to_capture = agent.generate_advice(frame, return_offset_ok=True)
        cv2.putText(frame, advice, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("AI Adaptive Photo Agent", frame)

        # 语音提示
        if ready_to_capture and not photo_taken:
            stable_count += 1
            if stable_count >= 3:
                speak_prompt_non_blocking("ready_photo", speaker)
                time.sleep(0.5)
                path = capturer.capture_and_save(frame)
                speaker.speak(f"Photo captured and saved at {path}.")
                print(f"[INFO] Photo saved at {path}")
                photo_taken = True
                time.sleep(2)
                break
        else:
            stable_count = 0
            # 语音提示用户调整
            if "Move back" in advice:
                speak_prompt_non_blocking("move_back", speaker)
            elif "Move closer" in advice:
                speak_prompt_non_blocking("move_closer", speaker)
            elif "Move left" in advice:
                speak_prompt_non_blocking("move_left", speaker)
            elif "Move right" in advice:
                speak_prompt_non_blocking("move_right", speaker)

        # 实时语音指令（每隔几秒监听一次）
        if time.time() - last_command_time > command_interval:
            command = listen_for_command(timeout=3, phrase_time_limit=3)
            action, param = parse_command(command)
            if action == "take_photo":
                # 拍照逻辑
                path = capturer.capture_and_save(frame)
                speaker.speak(f"Photo captured and saved at {path}.")
                print(f"[INFO] Photo saved at {path}")
                photo_taken = True
                time.sleep(2)
                break
            elif action == "set_filter" and param:
                # 切换滤镜逻辑
                if "自然" in param or "natural" in param:
                    style_choice = "natural"
                elif "明亮" in param or "bright" in param:
                    style_choice = "bright"
                elif "复古" in param or "vintage" in param:
                    style_choice = "vintage"
                elif "黑白" in param or "bw" in param:
                    style_choice = "bw"
                elif "hdr" in param:
                    style_choice = "hdr"
                elif "lomo" in param:
                    style_choice = "lomo"
                speaker.speak(f"{style_choice} 滤镜已切换")
            last_command_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
