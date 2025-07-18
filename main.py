import cv2
import time
from agent.adaptive_agent import AdaptivePhotoAgent
from utils.speech_utils import SpeechHelper, speak_prompt_non_blocking, countdown_and_capture_non_blocking
from utils.capture_utils import PhotoCapturer
from filters.beauty_filter import apply_filter_by_style

def main():
    target_size = input("Select photo type (full-body / half-body / portrait): ").strip().lower()
    style_choice = input("Select filter style (natural / bright / vintage / bw / hdr / lomo): ").strip().lower()

    agent = AdaptivePhotoAgent(user_image_dir="user_photos", target_size=target_size)
    speaker = SpeechHelper()
    capturer = PhotoCapturer()

    cap = cv2.VideoCapture(0)
    stable_count = 0
    photo_taken = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = apply_filter_by_style(frame, style_choice)
        advice, ready_to_capture = agent.generate_advice(frame, return_offset_ok=True)

        cv2.putText(frame, advice, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("AI Adaptive Photo Agent", frame)

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
