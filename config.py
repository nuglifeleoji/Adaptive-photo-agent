"""
Configuration file for Adaptive Photo Assistant
==============================================

This file contains all configuration settings for the application.
API keys are loaded from environment variables for security.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
# Set API_KEY in your .env file or environment variables
API_KEY = os.getenv('API_KEY', '')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.siliconflow.cn')

# Camera and Detection Settings
CAMERA_INDEX = 0  # Default camera (0 for built-in webcam)
TARGET_SIZE_DEFAULT = "half-body"  # Options: "full-body", "half-body", "portrait"
DETECTION_CONFIDENCE = 0.5  # Face detection confidence threshold

# Voice Recognition Settings
VOICE_TIMEOUT = 2  # Seconds to wait for voice input
PHRASE_TIME_LIMIT = 3  # Maximum seconds for a single phrase
VOICE_LANGUAGE = "en-US"  # Language for voice recognition (en-US, zh-CN)
COMMAND_INTERVAL = 5  # Seconds between voice command checks

# Speech Synthesis Settings
SPEECH_RATE = 220  # Words per minute for text-to-speech
SPEECH_VOICE = None  # Specific voice name (None for default)

# Photo Session Settings
MAX_PHOTOS_PER_SESSION = 3  # Maximum photos before auto-exit
PHOTO_OUTPUT_DIR = "captured_photos"
PHOTO_FORMAT = "jpg"  # Output image format

# Filter Settings
DEFAULT_FILTER = "natural"  # Default filter style
AVAILABLE_FILTERS = [
    "natural",
    "bright", 
    "vintage",
    "bw",  # black and white
    "hdr",
    "lomo",
    "cool",
    "warm"
]

# AI Prompt Settings
SMART_PROMPT_INTERVAL = 20  # Seconds between smart prompts
MAX_SUGGESTIONS_PER_SESSION = 2  # Limit AI suggestions to avoid spam
CONVERSATION_HISTORY_LIMIT = 4  # Number of messages to keep in history

# Performance Settings
FRAME_PROCESSING_THREADS = True  # Enable multi-threading for better performance
VIDEO_DISPLAY_SIZE = (640, 480)  # Display window size
FPS_TARGET = 30  # Target frames per second

# UI Settings
ADVICE_TEXT_COLOR = (0, 255, 0)  # Green color for advice text (BGR)
STATUS_TEXT_COLOR = (255, 255, 0)  # Yellow color for status text (BGR)
PROCESSING_TEXT_COLOR = (0, 255, 255)  # Cyan color for processing status (BGR)
FONT_SCALE = 0.8  # Text size scale factor
FONT_THICKNESS = 2  # Text thickness

# Development Settings
DEBUG_MODE = False  # Enable debug output
LOG_LEVEL = "INFO"  # Logging level (DEBUG, INFO, WARNING, ERROR)
ENABLE_PERFORMANCE_MONITORING = False  # Monitor FPS and processing times

# File Paths
USER_PHOTOS_DIR = "user_photos"  # Directory for user reference photos
TEMP_DIR = "temp"  # Temporary files directory
LOGS_DIR = "logs"  # Log files directory

# Validation function
def validate_config():
    """Validate configuration settings and warn about potential issues."""
    issues = []
    
    if not API_KEY or API_KEY == "your-api-key-here" or API_KEY == "":
        issues.append("API_KEY not configured - AI features will not work")
        issues.append("Please set API_KEY in your .env file or environment variables")
    
    if MAX_PHOTOS_PER_SESSION <= 0:
        issues.append("MAX_PHOTOS_PER_SESSION must be positive")
    
    if SMART_PROMPT_INTERVAL < 10:
        issues.append("SMART_PROMPT_INTERVAL should be at least 10 seconds")
    
    if DEFAULT_FILTER not in AVAILABLE_FILTERS:
        issues.append(f"DEFAULT_FILTER '{DEFAULT_FILTER}' not in AVAILABLE_FILTERS")
    
    return issues

if __name__ == "__main__":
    # Test configuration when run directly
    issues = validate_config()
    if issues:
        print("Configuration Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Configuration is valid!")
