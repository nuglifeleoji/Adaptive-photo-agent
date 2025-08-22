# Demo Files Information

This directory contains demonstration and testing files for the Adaptive Photo Assistant project.

## Files Overview

### Web Interface Demo
- **PhotoAgentDemo.jsx**: React component for web-based photo assistant
  - Uses webcam API for browser-based photo capture
  - Integrates with Flask backend (app.py)
  - Supports voice commands through Web Speech API
  - Chinese language interface

### Voice Chat Demos
- **voice_chat_demo.py**: Standalone voice conversation demo
  - Tests voice recognition and AI dialogue
  - No camera or photo capture functionality
  - Good for testing speech components

- **voice_chat_assistant.py**: Alternative voice assistant implementation
  - Similar to voice_chat_demo.py but with different configuration
  - Includes shutdown commands

### Testing Scripts
- **test_dialogue.py**: Unit tests for dialogue management
  - Tests various conversation scenarios
  - Validates command parsing
  - Useful for debugging AI responses

## Usage

### Running Web Demo
1. Start Flask backend: `python app.py`
2. Set up React frontend with PhotoAgentDemo.jsx
3. Access web interface at http://localhost:5000

### Running Voice Demos
```bash
# Basic voice chat
python voice_chat_demo.py

# Voice assistant with shutdown
python voice_chat_assistant.py

# Test dialogue system
python test_dialogue.py
```

## Integration with Main App

These demo files are separate from the main application (`main.py`) but share common utilities:
- `utils/dialogue_manager.py`
- `utils/speech_utils.py`
- `utils/voice_interactions.py`

## Notes

- Web demo requires additional React dependencies
- Voice demos need microphone access
- All demos use the same API key configuration
- Chinese language support in JSX demo
- English language support in Python demos
