import pyttsx3
import threading
import time
import queue

class SpeechHelper:
    def __init__(self, voice_name=None, rate=220):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        voices = self.engine.getProperty('voices')
        if voice_name:
            for v in voices:
                if voice_name.lower() in v.name.lower():
                    self.engine.setProperty('voice', v.id)
                    break
        else:
            self.engine.setProperty('voice', voices[0].id)
        self.speak_queue = queue.Queue()
        self.speak_thread = threading.Thread(target=self._speak_worker, daemon=True)
        self.speak_thread.start()

    def _speak_worker(self):
        while True:
            text = self.speak_queue.get()
            if text is None:
                break
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[SPEAK ERROR] {e}")

    def speak(self, text):
        print(f"[SPEAK] {text}")
        self.speak_queue.put(text)

    def countdown_and_capture(self, capturer, frame):
        for count in ["3", "2", "1", "茄子"]:
            self.speak(count)
            time.sleep(0.7)
        path = capturer.capture_and_save(frame)
        self.speak(f"照片已保存到 {path}")
        print(f"Photo saved at {path}")

    def list_available_voices(self):
        voices = self.engine.getProperty('voices')
        for v in voices:
            print(v.name)

    def close(self):
        self.speak_queue.put(None)

    def speak_sequence(self, texts, interval=0):
        """依次播报一组文本，每条之间可加间隔（秒）"""
        for text in texts:
            self.speak(text)
            if interval > 0:
                time.sleep(interval)

def speak_non_blocking(text, speaker):
    speaker.speak(text)
def speak_prompt_non_blocking(prompt_key, speaker):
    speaker.speak(prompt_key)
def countdown_and_capture_non_blocking(speaker, capturer, frame):
    threading.Thread(target=speaker.countdown_and_capture, args=(capturer, frame), daemon=True).start()