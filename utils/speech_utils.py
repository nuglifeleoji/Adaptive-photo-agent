import pyttsx3
import random
import threading
import time
import queue

class SpeechHelper:
    def __init__(self, voice_name=None, rate=150, prompt_pool=None):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        voices = self.engine.getProperty('voices')
        # 自动选择voice
        if voice_name:
            for v in voices:
                if voice_name.lower() in v.name.lower():
                    self.engine.setProperty('voice', v.id)
                    break
        else:
            self.engine.setProperty('voice', voices[0].id)
        # 支持自定义提示池
        self.prompt_pool = prompt_pool or {
            "move_up": ["Please lift your head.", "Tilt your head up a bit.", "Look up slightly."],
            "move_left": ["Please turn your body to the left.", "Turn left slightly.", "Rotate a bit left."],
            "move_right": ["Please turn your body to the right.", "Turn right slightly.", "Rotate a bit right."],
            "move_back": ["Please move back.", "Step back a little.", "Move backward slightly."],
            "move_closer": ["Please move closer.", "Step forward a bit.", "Come a bit closer to the camera."],
            "ready_photo": ["Nice smile detected, hold still for the photo."]
        }
        self.lock = threading.Lock()
        self.speak_queue = queue.Queue()
        self.speak_thread = threading.Thread(target=self._speak_worker, daemon=True)
        self.speak_thread.start()

    def _speak_worker(self):
        while True:
            text = self.speak_queue.get()
            if text is None:
                break
            try:
                with self.lock:
                    self.engine.say(text)
                    self.engine.runAndWait()
            except Exception as e:
                print(f"[SPEAK ERROR] {e}")

    def speak(self, text):
        print(f"[SPEAK] {text}")
        self.speak_queue.put(text)

    def speak_prompt(self, prompt_key):
        if prompt_key in self.prompt_pool:
            text = random.choice(self.prompt_pool[prompt_key])
            self.speak(text)
        else:
            self.speak(prompt_key)  # 兜底直接播报key

    def countdown_and_capture(self, capturer, frame):
        try:
            with self.lock:
                for count in ["Three", "Two", "One"]:
                    print(f"[SPEAK] {count}")
                    self.engine.say(count)
                    self.engine.runAndWait()
                    time.sleep(0.4)
                self.engine.say("Photo captured and saved.")
                self.engine.runAndWait()
            path = capturer.capture_and_save(frame)
            print(f"Photo saved at {path}")
        except Exception as e:
            print(f"[COUNTDOWN ERROR] {e}")

    def list_available_voices(self):
        voices = self.engine.getProperty('voices')
        for v in voices:
            print(v.name)

    def close(self):
        self.speak_queue.put(None)

def speak_non_blocking(text, speaker):
    threading.Thread(target=speaker.speak, args=(text,), daemon=True).start()

def speak_prompt_non_blocking(prompt_key, speaker):
    threading.Thread(target=speaker.speak_prompt, args=(prompt_key,), daemon=True).start()

def countdown_and_capture_non_blocking(speaker, capturer, frame):
    threading.Thread(target=speaker.countdown_and_capture, args=(capturer, frame), daemon=True).start()