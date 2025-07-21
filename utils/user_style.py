import os
from PIL import Image
import numpy as np

def extract_simple_style_features(image_path):
    # 这里只做简单色调统计，实际可用CLIP等更强模型
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)
    mean_color = arr.mean(axis=(0, 1))
    return mean_color  # 返回RGB均值

def analyze_user_style(photo_dir):
    features = []
    for fname in os.listdir(photo_dir):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            fpath = os.path.join(photo_dir, fname)
            features.append(extract_simple_style_features(fpath))
    if not features:
        return None
    avg_color = np.mean(features, axis=0)
    # 你可以根据avg_color等特征，生成风格标签
    return {'avg_color': avg_color.tolist()}
