# 📸 Adaptive Photo Assistant

> **Your friendly AI-powered assistant for taking better photos in real-time.**

## 🚀 Introduction

**Adaptive Photo Assistant** is an intelligent, interactive, real-time photography helper powered by computer vision and AI. It helps users capture satisfying photos through friendly voice interactions, real-time feedback, and AI-driven aesthetic analysis.

Whether you are struggling to find the best angle, chasing your personal photography style, or simply looking for a smoother photo-taking experience, this assistant is here to help — like having a patient and insightful photographer friend guiding you.

## 🏗️ Architecture Overview

The system consists of several key components working together:

- **Core Agent** (`agent/adaptive_agent.py`): Orchestrates detection and advice generation
- **Subject Detection** (`detectors/subject_detector.py`): Face detection and pose analysis using OpenCV + MediaPipe
- **Viewpoint Advisor** (`viewpoint/viewpoint_generator.py`): Composition and positioning guidance
- **AI Dialogue** (`utils/dialogue_manager.py`): Natural language interaction with LLM
- **Smart Prompting** (`utils/smart_prompt_generator.py`): Context-aware photography suggestions
- **Voice Interface** (`utils/speech_utils.py`): Text-to-speech and voice command processing
- **Filter System** (`filters/beauty_filter.py`): Real-time image enhancement and styling

## ✨ Core Features

### 🎙️ Conversational Guidance
- **Voice Interaction**: Talk to your camera! The assistant supports natural language interaction for composition, lighting, and timing advice
- **AI Dialogue Mode**: Enter conversation mode for personalized photography guidance
- **Command Recognition**: Simple voice commands for photo capture and filter switching

### 🎨 Smart Detection & Analysis
- **Face Detection**: Real-time face detection with bounding box tracking
- **Pose Analysis**: Head pose estimation (yaw, pitch, roll) using MediaPipe
- **Expression Recognition**: Smile detection for optimal capture timing
- **Body Positioning**: Upper body pose classification (left, right, center)

### 🚦 Real-Time Feedback & Guidance
- **Live Positioning Advice**: "Move closer", "Turn left", "Good position, hold"
- **Smart Prompts**: AI-generated contextual photography suggestions
- **Visual Overlays**: On-screen guidance text and status indicators
- **Automatic Capture**: Countdown and capture when conditions are optimal

### 📷 Advanced Photography Features
- **Multiple Filter Modes**: Natural, bright, vintage, black & white, HDR, Lomo
- **Composition Guidance**: Target sizing (full-body, half-body, portrait)
- **Session Management**: Automatic photo counting and session limits
- **Personalized Advice**: Learns from user preferences and reference photos

## 🔍 Example Use Cases

| Scenario | What It Helps With |
|--------------------|----------------------------------|
| **Portrait Selfies** | Guides posing, face angles, and expression timing |
| **Travel Photography** | Recommends composition, positioning, and lighting |
| **Professional Headshots** | Ensures consistent framing and optimal pose |
| **Social Media Content** | Applies trendy filters and suggests engaging poses |
| **Family Photos** | Manages group positioning and timing coordination |

## 🛠️ How It Works (Technical Flow)

1. **🎥 Camera Capture**: Initializes webcam feed with OpenCV
2. **👁️ Real-time Detection**: Analyzes faces, poses, and expressions using computer vision
3. **🧠 AI Analysis**: Processes detection results through intelligent advisory system
4. **🗣️ Voice Interaction**: Provides spoken guidance and responds to voice commands
5. **🎨 Filter Application**: Applies real-time visual enhancements based on user preferences
6. **📸 Smart Capture**: Automatically triggers photo capture when conditions are optimal
7. **💾 Photo Management**: Saves captured photos with timestamp organization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam/Camera device
- Microphone for voice commands
- Speaker/Headphones for audio feedback

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/adaptive-photo-agent.git
cd adaptive-photo-agent

# Setup environment and install dependencies
python setup.py

# Configure your API key
# Edit the .env file created by setup.py and add your API key

# Run the application
python main.py
```

### Manual Installation
```bash
# Install dependencies
pip install -r requirements_clean.txt

# Set up environment variables
cp env_template.txt .env
# Edit .env file and add your API key

# Test configuration
python config.py

# Run the application
python main.py
```

### Basic Usage
1. **Start the application**: Run `python main.py`
2. **Voice Commands**:
   - Say "start conversation" to enter AI dialogue mode
   - Say "take photo" for immediate capture
   - Say "enable prompts" for smart suggestions
   - Say "natural filter" / "vintage filter" etc. to change styles
3. **Follow on-screen guidance** for positioning and pose adjustments
4. **Photos are automatically saved** to `captured_photos/` directory

## 📁 Project Structure

```
adaptive-photo-agent/
├── agent/                          # Core intelligence module
│   └── adaptive_agent.py          # Main photo agent coordinator
├── detectors/                      # Computer vision detection
│   └── subject_detector.py        # Face & pose detection
├── filters/                        # Image processing & filters
│   └── beauty_filter.py          # Real-time filter effects
├── utils/                          # Utility modules
│   ├── capture_utils.py           # Photo capture & saving
│   ├── dialogue_manager.py        # AI conversation handling
│   ├── smart_prompt_generator.py  # Context-aware suggestions
│   ├── speech_utils.py            # Text-to-speech interface
│   ├── user_style.py              # User preference analysis
│   └── voice_interactions.py      # Voice command processing
├── viewpoint/                      # Composition guidance
│   └── viewpoint_generator.py     # Positioning advice
├── captured_photos/                # Output directory for photos
├── user_photos/                    # Reference photos for learning
├── main.py                         # Main application entry point
├── app.py                          # Flask web interface
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🔧 Technical Details

### Key Dependencies
- **OpenCV**: Computer vision and image processing
- **MediaPipe**: Advanced facial landmark detection
- **pyttsx3**: Text-to-speech synthesis
- **SpeechRecognition**: Voice command processing
- **Flask**: Web interface (optional)
- **requests**: API communication for AI dialogue

### AI Integration
- Uses external LLM API (SiliconFlow) for natural language processing
- Supports conversation history and context awareness
- Generates intelligent photography suggestions based on scene analysis

### Performance Optimizations
- Multi-threaded processing for voice and AI operations
- Efficient frame processing to minimize latency
- Smart prompt caching to avoid repetitive suggestions

## 🤝 Why This Matters

Photography isn't just technical; it's personal. This assistant aims to bridge **machine perception and human aesthetics**, making your camera smarter about what *you* love.

Instead of replacing photographers, this project enhances the user's **self-expression, confidence, and enjoyment** in the creative process through:
- Reducing technical barriers to good photography
- Providing personalized, contextual guidance
- Making photo sessions more interactive and fun

## 🚧 Future Enhancements

- **Advanced Style Learning**: Analyze user's photo library to learn personal aesthetic preferences
- **Multi-person Detection**: Handle group photos with multiple subjects
- **Gesture Recognition**: Support hand gesture commands in addition to voice
- **Cloud Integration**: Sync photos across devices and backup to cloud storage
- **Mobile App**: Native smartphone application with camera integration
- **Social Features**: Share photos directly to social media with optimized settings

## 🐛 Troubleshooting

### Common Issues
- **Camera not detected**: Ensure webcam is connected and not used by other applications
- **Voice commands not working**: Check microphone permissions and audio input levels
- **AI responses slow**: Verify internet connection and API key configuration
- **Filter effects not applying**: Update OpenCV and check video codec support

### Configuration
- **API Key**: Set your API key in the `.env` file (never commit this file!)
- **Settings**: Adjust camera, voice, and other settings in `config.py`
- **Voice Recognition**: Timeout and language settings configurable in `config.py`
- **Filters**: Customize filter styles and parameters in `filters/beauty_filter.py`

### Security Notes
- ✅ API keys are stored in environment variables (`.env` file)
- ✅ Sensitive files are excluded from git via `.gitignore`
- ✅ Template file provided for easy setup (`env_template.txt`)

## 📢 Contributing

Your ideas, issues, and pull requests are very welcome! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

Let's make photography more enjoyable and accessible together!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Built with ❤️ for photography enthusiasts and AI explorers*
