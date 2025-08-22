"""
Setup script for Adaptive Photo Assistant
=========================================

This script helps set up the development environment and install dependencies.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def create_directories():
    """Create necessary directories."""
    dirs = [
        'captured_photos',
        'user_photos', 
        'logs',
        'temp',
        'docs',
        'examples'
    ]
    
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✅ Created directory: {dir_name}")
        else:
            print(f"📁 Directory exists: {dir_name}")

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Try to install from clean requirements first
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements_clean.txt"
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install from requirements_clean.txt")
        print("Trying alternative installation...")
        
        # Fallback: install essential packages individually
        essential_packages = [
            "opencv-python",
            "mediapipe", 
            "numpy",
            "pyttsx3",
            "SpeechRecognition",
            "requests",
            "flask",
            "flask-cors"
        ]
        
        failed_packages = []
        for package in essential_packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
                print(f"✅ Installed: {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install: {package}")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"\n⚠️  Some packages failed to install: {failed_packages}")
            print("You may need to install them manually or check system dependencies.")
            return False
        
        return True

def check_system_dependencies():
    """Check for system-level dependencies."""
    print("\n🔍 Checking system dependencies...")
    
    system = platform.system()
    if system == "Windows":
        print("💡 On Windows, you may need:")
        print("  - Microsoft Visual C++ Redistributable")
        print("  - Windows SDK (for some packages)")
    elif system == "Linux":
        print("💡 On Linux, you may need:")
        print("  - sudo apt-get install portaudio19-dev python3-pyaudio")
        print("  - sudo apt-get install python3-opencv")
    elif system == "Darwin":  # macOS
        print("💡 On macOS, you may need:")
        print("  - brew install portaudio")
        print("  - Xcode command line tools")

def validate_installation():
    """Test if key modules can be imported."""
    print("\n🧪 Validating installation...")
    
    test_imports = [
        ("cv2", "OpenCV"),
        ("mediapipe", "MediaPipe"),
        ("numpy", "NumPy"),
        ("pyttsx3", "pyttsx3"),
        ("speech_recognition", "SpeechRecognition"),
        ("requests", "Requests")
    ]
    
    failed_imports = []
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {name}: {e}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️  Some modules failed to import: {failed_imports}")
        return False
    
    print("\n🎉 All core modules imported successfully!")
    return True

def setup_config():
    """Help user set up configuration."""
    print("\n⚙️  Configuration Setup:")
    print("1. Copy env_template.txt to .env")
    print("2. Edit .env file and add your API key")
    print("3. Adjust camera and voice settings in config.py as needed")
    print("4. Test the configuration with: python config.py")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n💡 Creating .env file from template...")
        try:
            with open('env_template.txt', 'r') as template:
                content = template.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created! Please edit it with your API key.")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            print("Please manually copy env_template.txt to .env")

def main():
    """Main setup function."""
    print("🚀 Adaptive Photo Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Some dependencies failed to install.")
        print("Please check the error messages above and install manually if needed.")
    
    # Check system dependencies
    check_system_dependencies()
    
    # Validate installation
    if validate_installation():
        print("\n🎉 Setup completed successfully!")
        setup_config()
        print("\nYou can now run the application with: python main.py")
    else:
        print("\n❌ Setup completed with errors.")
        print("Please resolve the import errors before running the application.")

if __name__ == "__main__":
    main()
