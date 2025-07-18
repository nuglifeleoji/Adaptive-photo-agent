
import speech_recognition as sr

def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    print("[DEBUG] Available microphones:")
    for idx, name in enumerate(mic_list):
        print(f"  {idx}: {name}")
    return mic_list

def listen_for_command(timeout=5, phrase_time_limit=5, mic_index=None, language="zh-CN"):
    recognizer = sr.Recognizer()
    mic_list = list_microphones()
    if mic_index is None and mic_list:
        mic_index = 0  # 默认用第一个麦克风
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("[INFO] Listening for command... Speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("[INFO] Processing speech...")
            command = recognizer.recognize_google(audio, language=language)
            print(f"[INFO] Recognized command: {command}")
            return command.lower()
    except sr.UnknownValueError:
        print("[WARNING] Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"[ERROR] Could not request results; {e}")
        return ""
    except Exception as e:
        print(f"[ERROR] Speech recognition error: {e}")
        return ""

def parse_command(command):
    """解析语音指令，返回标准化动作和参数"""
    if any(word in command for word in ["拍照", "take photo", "capture", "照相"]):
        return ("take_photo", None)
    if any(word in command for word in ["滤镜", "filter"]):
        # 识别滤镜类型
        for style in ["natural", "bright", "vintage", "black and white", "bw", "hdr", "lomo", "自然", "明亮", "复古", "黑白"]:
            if style in command:
                return ("set_filter", style)
        return ("set_filter", None)
    return (None, None)

def select_filter_by_voice(speaker):
    from utils.speech_utils import speak_non_blocking
    speak_non_blocking("Please say your preferred filter: natural, bright, vintage, black and white, HDR, or lomo.", speaker)
    style_choice = "natural"
    while True:
        command = listen_for_command()
        action, style = parse_command(command)
        if action == "set_filter" and style:
            speak_non_blocking(f"{style} filter selected. Say 'take photo' to capture when ready.", speaker)
            return style
