import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
from PIL import Image
import io

app = Flask(__name__)

# Determine model path dynamically
BASE_DIR = Path(__file__).resolve().parent
MODEL_CANDIDATES = [
    BASE_DIR / "logs" / "Resnet18_results" / "Resnet18_full_model.pt",
    BASE_DIR.parent / "Resnet18_full_model.pt",
    BASE_DIR / "Resnet18_full_model.pt",
    BASE_DIR / "logs" / "Resnet18_results" / "Resnet18.pt",
]

model_path = None
for candidate in MODEL_CANDIDATES:
    if candidate.exists():
        model_path = candidate
        break

if model_path is None:
    raise FileNotFoundError(f"Model file not found. Checked: {[str(p) for p in MODEL_CANDIDATES]}")

print(f"Loading model from: {model_path}")
model = torch.load(
    str(model_path),
    map_location=torch.device("cpu"),
    weights_only=False
)
model.eval()  # Set the model to evaluation mode

# Check if CUDA is available and move model to GPU if possible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Define class names and metadata
CLASS_NAMES = [
    'Bean', 'BitterG', 'BottleG', 'Brinjal', 'Broccoli', 
    'cabbage', 'capsicum', 'carrot', 'cauuliflower', 
    'cucumber', 'papaya', 'potato', 'pumpkin', 'radish', 
    'tomato'
]

DISPLAY_NAMES = {
    'Bean': 'Green Beans',
    'BitterG': 'Bitter Gourd (Karela)',
    'BottleG': 'Bottle Gourd (Lauki)',
    'Brinjal': 'Brinjal / Eggplant',
    'Broccoli': 'Broccoli',
    'cabbage': 'Cabbage',
    'capsicum': 'Capsicum / Bell Pepper',
    'carrot': 'Carrot',
    'cauuliflower': 'Cauliflower',
    'cucumber': 'Cucumber',
    'papaya': 'Papaya',
    'potato': 'Potato',
    'pumpkin': 'Pumpkin',
    'radish': 'Radish',
    'tomato': 'Tomato'
}

VEG_INFO = {
    'Bean': {'emoji': '🌱', 'tag': 'Legume', 'desc': 'Rich in plant-based protein, dietary fiber, Vitamin C, and essential minerals.'},
    'BitterG': {'emoji': '🥒', 'tag': 'Gourd', 'desc': 'Contains charantin and vicine compounds that naturally help regulate blood sugar.'},
    'BottleG': {'emoji': '🫒', 'tag': 'Gourd', 'desc': 'Over 96% water content; ultra-low in calories and helps digestion and hydration.'},
    'Brinjal': {'emoji': '🍆', 'tag': 'Nightshade', 'desc': 'Packed with nasunin antioxidant and anthocyanins that protect brain cell membranes.'},
    'Broccoli': {'emoji': '🥦', 'tag': 'Cruciferous', 'desc': 'Rich in sulforaphane, Vitamin C, Vitamin K, and bio-available calcium for immunity.'},
    'cabbage': {'emoji': '🥬', 'tag': 'Cruciferous', 'desc': 'High in sulfur, Vitamin C, and dietary fiber that support gut microbiota health.'},
    'capsicum': {'emoji': '🫑', 'tag': 'Nightshade', 'desc': 'Provides over 200% of daily Vitamin C intake, along with Vitamin A and folate.'},
    'carrot': {'emoji': '🥕', 'tag': 'Root', 'desc': 'Exceptional source of beta-carotene (provitamin A) and lutein for vision & skin health.'},
    'cauuliflower': {'emoji': '🥦', 'tag': 'Cruciferous', 'desc': 'Packed with choline, Vitamin C, and glucosinolates that assist cellular detox.'},
    'cucumber': {'emoji': '🥒', 'tag': 'Gourd', 'desc': '95% water content, rich in silica and caffeic acid that naturally cool and hydrate.'},
    'papaya': {'emoji': '🍈', 'tag': 'Fruit / Vegetable', 'desc': 'Contains proteolytic enzyme papain, Vitamin A, and Vitamin C for digestive wellness.'},
    'potato': {'emoji': '🥔', 'tag': 'Tuber', 'desc': 'Rich in potassium, Vitamin B6, resistant starches, and essential complex carbs.'},
    'pumpkin': {'emoji': '🎃', 'tag': 'Squash', 'desc': 'High in alpha and beta-carotene, antioxidants, and immune-supporting dietary fiber.'},
    'radish': {'emoji': '🌱', 'tag': 'Root', 'desc': 'Natural source of isothiocyanates and sulfur compounds that support liver function.'},
    'tomato': {'emoji': '🍅', 'tag': 'Nightshade', 'desc': 'Major dietary source of lycopene antioxidant, potassium, Vitamin C, and folate.'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classes', methods=['GET'])
def get_classes():
    classes_list = []
    for raw in CLASS_NAMES:
        info = VEG_INFO.get(raw, {'emoji': '🥗', 'tag': 'Vegetable', 'desc': ''})
        classes_list.append({
            'raw_name': raw,
            'name': DISPLAY_NAMES.get(raw, raw),
            'emoji': info['emoji'],
            'tag': info['tag'],
            'desc': info['desc']
        })
    return jsonify({
        'total': len(CLASS_NAMES),
        'device': str(device),
        'model_name': 'ResNet-18 (PyTorch Transfer Learning)',
        'classes': classes_list
    })

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Read image file and ensure RGB mode
        img = Image.open(io.BytesIO(file.read())).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(device)

        # Predict
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]
            top_prob, top_indices = torch.topk(probabilities, k=min(5, len(CLASS_NAMES)))

        # Format top predictions
        top_predictions = []
        for prob, idx in zip(top_prob.tolist(), top_indices.tolist()):
            raw_name = CLASS_NAMES[idx]
            info = VEG_INFO.get(raw_name, {'emoji': '🥗', 'tag': 'Vegetable', 'desc': ''})
            top_predictions.append({
                'raw_name': raw_name,
                'name': DISPLAY_NAMES.get(raw_name, raw_name),
                'probability': round(prob * 100, 2),
                'emoji': info['emoji'],
                'tag': info['tag']
            })

        best_raw = CLASS_NAMES[top_indices[0].item()]
        best_info = VEG_INFO.get(best_raw, {'emoji': '🥗', 'tag': 'Vegetable', 'desc': ''})

        return jsonify({
            'prediction': DISPLAY_NAMES.get(best_raw, best_raw),
            'raw_prediction': best_raw,
            'confidence': round(top_prob[0].item() * 100, 2),
            'emoji': best_info['emoji'],
            'tag': best_info['tag'],
            'description': best_info['desc'],
            'top_predictions': top_predictions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
