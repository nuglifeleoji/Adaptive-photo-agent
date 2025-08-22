"""
Adaptive Photo Assistant - Main Application
==========================================

This is an AI-powered intelligent photography assistant that integrates:
- Real-time face detection and pose analysis
- Voice interaction and intelligent dialogue
- Automatic photo suggestions and countdown
- Multiple filter effects
- Smart prompt generation

Key module imports:
- cv2: OpenCV library for computer vision and image processing
- threading: Multi-threading support for concurrent voice and AI dialogue processing
- AdaptivePhotoAgent: Core intelligent photography agent
- SpeechHelper: Text-to-speech assistant
- PhotoCapturer: Photo capture and saving functionality
- DialogueManager: AI dialogue management
- SmartPromptGenerator: Intelligent prompt generator
"""

import cv2
import time
import threading
from agent.adaptive_agent import AdaptivePhotoAgent
from utils.speech_utils import SpeechHelper, speak_prompt_non_blocking
from utils.capture_utils import PhotoCapturer
from filters.beauty_filter import apply_filter_by_style
from utils.voice_interactions import listen_for_command
from utils.dialogue_manager import DialogueManager
from utils.smart_prompt_generator import SmartPromptGenerator
import config

def main():
    """
    Main function that initializes and runs the adaptive photo assistant.
    
    This function sets up all necessary components including:
    - Photo agent for detection and analysis
    - Speech synthesis and recognition
    - AI dialogue management
    - Camera capture and filtering
    
    The main loop handles:
    - Real-time video processing
    - Voice command recognition
    - AI-powered suggestions
    - Automatic photo capture
    """
    # Initialize core parameters from configuration
    target_size = config.TARGET_SIZE_DEFAULT
    style_choice = config.DEFAULT_FILTER
    
    # Initialize core modules
    agent = AdaptivePhotoAgent(user_image_dir=config.USER_PHOTOS_DIR, target_size=target_size)
    speaker = SpeechHelper(rate=config.SPEECH_RATE)
    capturer = PhotoCapturer(save_dir=config.PHOTO_OUTPUT_DIR, img_format=config.PHOTO_FORMAT)
    
    # Initialize AI dialogue and smart prompting
    dialogue_manager = DialogueManager(config.API_KEY, config.API_BASE_URL)
    smart_prompt_generator = SmartPromptGenerator(config.API_KEY)
    
    # Initialize camera capture
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    stable_count = 0
    photo_taken = False
    is_counting_down = False  # Flag to prevent multiple countdown processes
    
    # Voice interaction parameters
    last_command_time = time.time()
    command_interval = config.COMMAND_INTERVAL
    conversation_mode = False # Whether in AI conversation mode
    processing_command = False # Whether currently processing a command
    auto_prompt_mode = True   # Whether smart prompting is enabled
    
    last_smart_prompt = None  # Track last spoken smart prompt to avoid repetition

    print("Adaptive Photo Assistant Started!")
    print("Say 'start conversation' to enter AI dialogue mode")
    print("Say 'disable prompts' to turn off automatic prompts")
    print("Say 'take photo' for immediate capture")
    print("Press 'q' to exit")

    def process_ai_dialogue(command):
        """
        Process AI dialogue in background thread.
        
        Args:
            command (str): Voice command from user
            
        This function handles:
        - AI conversation via DialogueManager
        - Command parsing and execution
        - Filter changes and photo capture
        - Pose adjustment suggestions
        """
        nonlocal conversation_mode, style_choice, photo_taken
        
        try:
            print(f"User: {command}")
            
            # Call AI dialogue system
            ai_reply, parsed_commands = dialogue_manager.chat_with_ai(command)
            if not ai_reply or len(ai_reply.strip()) == 0:
                ai_reply = "Sorry, I didn't catch that. Please try again."
            print(f"AI: {ai_reply}")
            speaker.speak(ai_reply)
            
            # Process parsed commands from AI response
            if parsed_commands.get("action") == "take_photo":
                path = capturer.capture_and_save(frame)
                speaker.speak(f"Photo saved to {path}")
                print(f"[INFO] Photo saved at {path}")
                photo_taken = True
                
            elif parsed_commands.get("filter_change"):
                new_filter = parsed_commands["filter_change"]
                style_choice = new_filter
                speaker.speak(f"Switched to {new_filter} filter")
                print(f"Filter changed to: {new_filter}")
                
            elif parsed_commands.get("pose_adjustment"):
                pose = parsed_commands["pose_adjustment"]
                speaker.speak(f"Please adjust {pose}")
                print(f"Pose adjustment: {pose}")
                
        except Exception as e:
            print(f"[ERROR] AI dialogue processing error: {e}")
        finally:
            processing_command = False

    def process_smart_prompt(detection_result, photo_taken_ref):
        """
        Process smart prompts in background thread.
        
        Args:
            detection_result (dict): Face detection and pose analysis results
            photo_taken_ref (list): Reference to photo_taken flag for thread safety
            
        This function:
        - Generates AI-powered photography suggestions
        - Provides voice feedback on pose and composition
        - Triggers automatic photo capture when conditions are optimal
        """
        nonlocal last_smart_prompt
        try:
            # Generate smart AI prompt based on detection results
            prompt = smart_prompt_generator.generate_smart_prompt(detection_result)
            
            # Only speak if prompt content has changed to avoid repetition
            if prompt and prompt != last_smart_prompt:
                speaker.speak(prompt)  # Speak full AI response
                last_smart_prompt = prompt
                time.sleep(1)  # Wait 1 second after speaking
                
                # Simplify prompt content for key actions
                simplified_prompt = smart_prompt_generator.simplify_prompt(prompt)
                
                # Speak simplified prompt for clarity
                speaker.speak(simplified_prompt)
                
                # Check if prompt suggests taking photo
                photo_keywords = ["ready to capture", "take photo now", "perfect timing", "capture now"]
                if any(keyword in prompt.lower() for keyword in photo_keywords):
                    # Auto-capture after short delay
                    time.sleep(1)  # Reduced from 3 to 1 for faster response
                    if not photo_taken_ref[0]:  # Use list reference for thread safety
                        do_countdown_and_capture(frame)
                        photo_taken_ref[0] = True
                
        except Exception as e:
            print(f"[ERROR] Smart prompt processing error: {e}")

    def do_countdown_and_capture(frame):
        """
        Perform countdown and capture photo.
        
        Args:
            frame: Current video frame to capture
            
        Returns:
            str: Path to saved photo file
        """
        # Countdown sequence
        for count in ["3", "2", "1", "Cheese!"]:
            speaker.speak(count)
            time.sleep(1)  # 1 second between counts
        
        # Capture and save photo
        path = capturer.capture_and_save(frame)
        speaker.speak(f"Photo saved to {path}")
        print(f"[INFO] Photo saved at {path}")
        return path

    # Photo session management
    photo_count = 0
    max_photos = config.MAX_PHOTOS_PER_SESSION
    photo_taken = False
    is_counting_down = False

    # Main application loop
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply selected filter to frame
        frame = apply_filter_by_style(frame, style_choice)
        
        # Get face detection and pose analysis results
        detection_result = agent.detector.detect(frame)
        
        # Generate intelligent photography advice
        advice, ready_to_capture = agent.generate_advice(frame, return_offset_ok=True)
        cv2.putText(frame, advice, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Display current mode status
        if conversation_mode:
            status_text = "Conversation Mode"
        elif auto_prompt_mode:
            status_text = "Smart Prompt Mode"
        else:
            status_text = "Basic Mode"
        cv2.putText(frame, status_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Display processing status
        if processing_command:
            cv2.putText(frame, "Processing...", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("AI Adaptive Photo Agent", frame)

        # Auto-capture logic: only process if not counting down and haven't reached max photos
        if ready_to_capture and not photo_taken and not is_counting_down and photo_count < max_photos:
            is_counting_down = True
            def countdown_and_shoot():
                """Inner function for countdown and photo capture in separate thread"""
                for count in ["3", "2", "1", "Cheese!"]:
                    speaker.speak(count)
                    time.sleep(1)  # 1 second between counts
                path = capturer.capture_and_save(frame)
                speaker.speak(f"Photo saved to {path}")
                print(f"[INFO] Photo saved at {path}")
                nonlocal photo_taken, is_counting_down, photo_count
                photo_taken = True
                is_counting_down = False
                photo_count += 1
            threading.Thread(target=countdown_and_shoot, daemon=True).start()
            continue

        # Reset photo_taken flag when user adjusts pose (ready_to_capture becomes False then True again)
        if not ready_to_capture:
            photo_taken = False

        # Exit after capturing maximum number of photos
        if photo_count >= max_photos:
            print("Captured 3 photos. Application will exit.")
            break

        # Smart active prompting (when not in conversation mode)
        if auto_prompt_mode and not conversation_mode and not processing_command:
            # Process smart prompts in background thread, pass photo_taken reference
            thread = threading.Thread(target=process_smart_prompt, args=(detection_result, [photo_taken]), daemon=True)
            thread.start()

        # Voice command processing
        if not processing_command and time.time() - last_command_time > command_interval:
            command = listen_for_command(timeout=2, phrase_time_limit=3)
            
            if command:
                print(f"Recognized command: {command}")
                processing_command = True
                
                # Check for entering conversation mode
                if "start conversation" in command.lower() or "conversation mode" in command.lower():
                    conversation_mode = True
                    auto_prompt_mode = False  # Disable automatic prompts
                    speaker.speak("Entered intelligent conversation mode. Please tell me your photography needs.")
                    print("Entered conversation mode")
                    processing_command = False
                    
                # Check for exiting conversation mode
                elif "exit conversation" in command.lower() or "basic mode" in command.lower():
                    conversation_mode = False
                    auto_prompt_mode = True  # Re-enable automatic prompts
                    speaker.speak("Exited conversation mode. Smart prompts enabled.")
                    print("Exited conversation mode")
                    processing_command = False
                    
                # Control smart prompting
                elif "disable prompts" in command.lower() or "stop prompts" in command.lower():
                    auto_prompt_mode = False
                    speaker.speak("Smart prompts disabled")
                    print("Smart prompts disabled")
                    processing_command = False
                    
                elif "enable prompts" in command.lower() or "start prompts" in command.lower():
                    auto_prompt_mode = True
                    speaker.speak("Smart prompts enabled")
                    print("Smart prompts enabled")
                    processing_command = False
                    
                # Smart interaction in conversation mode
                elif conversation_mode:
                    # Process AI dialogue in background thread
                    thread = threading.Thread(target=process_ai_dialogue, args=(command,), daemon=True)
                    thread.start()
                
                # Simple commands in basic mode
                else:
                    # Direct photo capture command
                    if "take photo" in command.lower() or "capture" in command.lower():
                        path = capturer.capture_and_save(frame)
                        speaker.speak(f"Photo saved to {path}")
                        print(f"[INFO] Photo saved at {path}")
                        photo_taken = True
                        time.sleep(2)
                        break
                    
                    # Filter switching commands
                    elif "filter" in command.lower():
                        if "natural" in command.lower():
                            style_choice = "natural"
                        elif "bright" in command.lower():
                            style_choice = "bright"
                        elif "vintage" in command.lower():
                            style_choice = "vintage"
                        elif "black and white" in command.lower() or "bw" in command.lower():
                            style_choice = "bw"
                        elif "hdr" in command.lower():
                            style_choice = "hdr"
                        elif "lomo" in command.lower():
                            style_choice = "lomo"
                        speaker.speak(f"{style_choice} filter applied")
                    
                    # Take another photo command
                    elif "one more" in command.lower() or "another photo" in command.lower():
                        smart_prompt_generator.reset_suggestions()
                        do_countdown_and_capture(frame)
                        photo_taken = True
                        time.sleep(2)
                        break
                    
                    processing_command = False
            
            last_command_time = time.time()

        # Voice prompts for user adjustments (only in non-conversation mode and not counting down)
        if not conversation_mode and not is_counting_down:
            if "Move back" in advice:
                speak_prompt_non_blocking("Please move back", speaker)
            elif "Move closer" in advice:
                speak_prompt_non_blocking("Please move closer", speaker)
            elif "Move left" in advice:
                speak_prompt_non_blocking("Please move left", speaker)
            elif "Move right" in advice:
                speak_prompt_non_blocking("Please move right", speaker)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
