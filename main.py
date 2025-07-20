import cv2
import time
import threading
from agent.adaptive_agent import AdaptivePhotoAgent
from utils.speech_utils import SpeechHelper, speak_prompt_non_blocking
from utils.capture_utils import PhotoCapturer
from filters.beauty_filter import apply_filter_by_style
from utils.voice_interactions import listen_for_command
from utils.dialogue_manager import DialogueManager

def main():
    # 初始化参数
    target_size = "half-body"
    style_choice = "natural"
    
    # 初始化各个模块
    agent = AdaptivePhotoAgent(user_image_dir="user_photos", target_size=target_size)
    speaker = SpeechHelper()
    capturer = PhotoCapturer()
    
    # 初始化对话管理
    api_key = "sk-crrrxsgwputbfxhvilcgzafqyrkzevfmcmocyupkbpcivnrh"
    dialogue_manager = DialogueManager(api_key)
    
    # 启动摄像头
    cap = cv2.VideoCapture(0)
    stable_count = 0
    photo_taken = False
    
    # 对话相关参数
    last_command_time = time.time()
    command_interval = 5  # 增加间隔到5秒，减少卡顿
    conversation_mode = False  # 是否处于对话模式
    processing_command = False  # 是否正在处理指令
    
    print("智能拍照助手已启动！")
    print("说'开始对话'进入智能对话模式")
    print("说'拍照'直接拍照")
    print("按 'q' 退出")

    def process_ai_dialogue(command):
        """在后台线程中处理AI对话"""
        nonlocal conversation_mode, style_choice, photo_taken
        
        try:
            print(f"用户: {command}")
            
            # 调用AI对话
            ai_response, parsed_commands = dialogue_manager.chat_with_ai(command)
            print(f"AI: {ai_response}")
            
            # 语音播报AI回复
            speaker.speak(ai_response)
            
            # 处理解析的指令
            if parsed_commands.get("action") == "take_photo":
                path = capturer.capture_and_save(frame)
                speaker.speak(f"照片已保存到 {path}")
                print(f"[INFO] Photo saved at {path}")
                photo_taken = True
                
            elif parsed_commands.get("filter_change"):
                new_filter = parsed_commands["filter_change"]
                style_choice = new_filter
                speaker.speak(f"已切换到{new_filter}滤镜")
                print(f"滤镜切换为: {new_filter}")
                
            elif parsed_commands.get("pose_adjustment"):
                pose = parsed_commands["pose_adjustment"]
                speaker.speak(f"请{pose}调整")
                print(f"姿势调整: {pose}")
                
        except Exception as e:
            print(f"[ERROR] AI对话处理错误: {e}")
        finally:
            processing_command = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 应用滤镜
        frame = apply_filter_by_style(frame, style_choice)
        
        # 智能建议
        advice, ready_to_capture = agent.generate_advice(frame, return_offset_ok=True)
        cv2.putText(frame, advice, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # 显示对话状态
        status_text = "对话模式" if conversation_mode else "普通模式"
        cv2.putText(frame, status_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # 显示处理状态
        if processing_command:
            cv2.putText(frame, "处理中...", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("AI Adaptive Photo Agent", frame)

        # 语音指令处理（减少频率，避免卡顿）
        if not processing_command and time.time() - last_command_time > command_interval:
            command = listen_for_command(timeout=2, phrase_time_limit=3)  # 减少超时时间
            
            if command:
                print(f"识别到指令: {command}")
                processing_command = True
                
                # 检查是否进入对话模式
                if "开始对话" in command or "对话模式" in command:
                    conversation_mode = True
                    speaker.speak("已进入智能对话模式，请告诉我你的拍照需求")
                    print("进入对话模式")
                    processing_command = False
                    
                # 检查是否退出对话模式
                elif "退出对话" in command or "普通模式" in command:
                    conversation_mode = False
                    speaker.speak("已退出对话模式")
                    print("退出对话模式")
                    processing_command = False
                    
                # 对话模式下的智能交互（使用后台线程）
                elif conversation_mode:
                    # 在后台线程中处理AI对话
                    thread = threading.Thread(target=process_ai_dialogue, args=(command,), daemon=True)
                    thread.start()
                
                # 普通模式下的简单指令
                else:
                    # 直接拍照指令
                    if "拍照" in command or "take photo" in command:
                        path = capturer.capture_and_save(frame)
                        speaker.speak(f"照片已保存到 {path}")
                        print(f"[INFO] Photo saved at {path}")
                        photo_taken = True
                        time.sleep(2)
                        break
                    
                    # 滤镜切换指令
                    elif "滤镜" in command or "filter" in command:
                        if "自然" in command or "natural" in command:
                            style_choice = "natural"
                        elif "明亮" in command or "bright" in command:
                            style_choice = "bright"
                        elif "复古" in command or "vintage" in command:
                            style_choice = "vintage"
                        elif "黑白" in command or "bw" in command:
                            style_choice = "bw"
                        elif "hdr" in command:
                            style_choice = "hdr"
                        elif "lomo" in command:
                            style_choice = "lomo"
                        speaker.speak(f"{style_choice} 滤镜已切换")
                    
                    processing_command = False
            
            last_command_time = time.time()

        # 自动拍照逻辑（当满足条件时）
        if ready_to_capture and not photo_taken and not conversation_mode:
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
            # 语音提示用户调整（仅在非对话模式下）
            if not conversation_mode:
                if "Move back" in advice:
                    speak_prompt_non_blocking("move_back", speaker)
                elif "Move closer" in advice:
                    speak_prompt_non_blocking("move_closer", speaker)
                elif "Move left" in advice:
                    speak_prompt_non_blocking("move_left", speaker)
                elif "Move right" in advice:
                    speak_prompt_non_blocking("move_right", speaker)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
