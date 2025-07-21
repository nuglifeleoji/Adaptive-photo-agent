from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils.dialogue_manager import DialogueManager
import base64
import os
import datetime
from utils.user_style import analyze_user_style

app = Flask(__name__)
CORS(app)  # 允许跨域

dialogue_manager = DialogueManager(api_key="你的API_KEY")
PHOTO_DIR = "captured_photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

@app.route('/ai_suggestion', methods=['POST'])
def ai_suggestion():
    data = request.get_json()
    user_text = data.get('user_text', '') if data else ''
    ai_reply, _ = dialogue_manager.chat_with_ai(user_text)
    return jsonify({'ai_reply': ai_reply})

@app.route('/take_photo', methods=['POST'])
def take_photo():
    data = request.get_json()
    img_b64 = data.get('img_b64') if data else None
    if not img_b64:
        return jsonify({'error': 'No image data'}), 400
    img_data = base64.b64decode(img_b64.split(',')[1])
    filename = f"photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(PHOTO_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(img_data)
    return jsonify({'photo_url': f'/photo/{filename}'})

@app.route('/photo/<filename>')
def get_photo(filename):
    return send_from_directory(PHOTO_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
