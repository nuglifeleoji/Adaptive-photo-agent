import torch
from PIL import Image
from torchvision import transforms
import numpy as np
import os
import clip  # 路径根据你的实际情况调整

def extract_clip_features(image_path, model, preprocess, device):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
    return image_features.cpu().numpy().flatten()

def analyze_user_style_clip(photo_dir):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    features = []
    for fname in os.listdir(photo_dir):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            fpath = os.path.join(photo_dir, fname)
            features.append(extract_clip_features(fpath, model, preprocess, device))
    if not features:
        return None
    avg_feature = np.mean(features, axis=0)
    # 你可以用 avg_feature 与一组风格文本做相似度，得到风格标签
    return {'clip_feature': avg_feature.tolist()}
