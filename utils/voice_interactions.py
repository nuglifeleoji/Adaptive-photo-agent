
import speech_recognition as sr

def listen_for_command(timeout=5, phrase_time_limit=5, mic_index=None):
    recognizer = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()
    print("[DEBUG] Available microphones:")
    for idx, name in enumerate(mic_list):
        print(f"  {idx}: {name}")
    
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("[INFO] Listening for command... Speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("[INFO] Processing speech...")
            command = recognizer.recognize_google(audio)
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


def select_filter_by_voice(speaker):
    """Interactively ask the user to choose a filter via voice."""
    from utils.speech_utils import speak_non_blocking
    speak_non_blocking("Please say your preferred filter: natural, bright, vintage, black and white, HDR, or lomo.", speaker)
    style_choice = "natural"
    while True:
        command = listen_for_command()
        if any(style in command for style in ["natural", "bright", "vintage", "black and white", "bw", "hdr", "lomo"]):
            if "bright" in command:
                style_choice = "bright"
            elif "vintage" in command:
                style_choice = "vintage"
            elif "black and white" in command or "bw" in command:
                style_choice = "bw"
            elif "hdr" in command:
                style_choice = "hdr"
            elif "lomo" in command:
                style_choice = "lomo"
            else:
                style_choice = "natural"
            speak_non_blocking(f"{style_choice} filter selected. Say 'take photo' to capture when ready.", speaker)
            return style_choice
