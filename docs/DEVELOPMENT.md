# Development Guide

## Project Overview

This document provides technical details for developers working on the Adaptive Photo Assistant project.

## Architecture

### Core Components

1. **AdaptivePhotoAgent** (`agent/adaptive_agent.py`)
   - Main coordinator for detection and advice generation
   - Integrates SubjectDetector and ViewpointAdvisor
   - Manages user reference preferences

2. **SubjectDetector** (`detectors/subject_detector.py`)
   - Face detection using OpenCV Haar cascades
   - Head pose estimation using MediaPipe
   - Body positioning classification
   - Smile detection for optimal timing

3. **DialogueManager** (`utils/dialogue_manager.py`)
   - AI conversation handling via external LLM API
   - Command parsing and execution
   - Conversation history management

4. **SmartPromptGenerator** (`utils/smart_prompt_generator.py`)
   - Context-aware photography suggestions
   - AI-powered scene analysis
   - Intelligent prompt caching

## API Configuration

### External LLM Integration

The project uses SiliconFlow API for AI dialogue. Configure your API key in:
- `utils/dialogue_manager.py` (line 7)
- `utils/smart_prompt_generator.py` (line 235)

```python
api_key = "your-api-key-here"
```

### Voice Recognition

Uses Google Speech Recognition API through the `speech_recognition` library:
- Requires internet connection
- Supports multiple languages (default: Chinese and English)
- Configurable timeout and phrase limits

## Performance Considerations

### Multi-threading

The application uses threading for:
- Voice command processing (non-blocking)
- AI dialogue generation (background)
- Smart prompt generation (concurrent)

### Memory Management

- MediaPipe models are initialized once and reused
- Conversation history is limited to recent messages
- Detection results are processed in real-time without caching

## Testing

### Manual Testing

Run individual components:
```bash
# Test dialogue system
python test_dialogue.py

# Test voice chat only
python voice_chat_demo.py

# Test voice assistant
python voice_chat_assistant.py
```

### Web Interface

Alternative web-based interface available:
```bash
python app.py
# Access at http://localhost:5000
```

## Code Style

- All comments and documentation in English
- Function docstrings follow Google style
- Type hints recommended for new code
- Error handling with try-catch blocks

## Future Development

### Planned Features

1. **Advanced Style Learning**
   - CLIP-based feature extraction
   - User preference clustering
   - Personalized filter recommendations

2. **Enhanced Detection**
   - Multi-person support
   - Gesture recognition
   - Emotion detection

3. **Mobile Integration**
   - React Native app
   - Camera API integration
   - Cloud synchronization

### Contributing

1. Fork the repository
2. Create feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit pull request

### Code Review Checklist

- [ ] English comments and docstrings
- [ ] Error handling implemented
- [ ] Performance impact considered
- [ ] Threading safety verified
- [ ] API keys not hardcoded
