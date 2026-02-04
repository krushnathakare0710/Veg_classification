from flask import Flask, request, jsonify, render_template
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
from PIL import Image
import io

app = Flask(__name__)

# Load the entire model, including architecture and weights

model = torch.load(
    r"C:\Users\Lenovo\OneDrive\Desktop\Academics\FY_project\DL\Veg_project\logs\Resnet18_results\Resnet18_full_model.pt",
    map_location=torch.device("cpu"),
    weights_only=False
)
# model = torch.load(r"C:\Users\Lenovo\OneDrive\Desktop\Academics\FY_project\DL\Veg_project\logs\Resnet18_results\Resnet18_full_model.pt", weights_only=False)
model.eval()  # Set the model to evaluation mode

# Check if CUDA is available and move model to GPU if possible
device = torch.device("cpu")
#  if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Use standard ImageNet normalization
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read image file
    img = Image.open(io.BytesIO(file.read()))
    img = transform(img).unsqueeze(0)  # Add batch dimension

    # Move image tensor to the same device as the model
    img = img.to(device)

    # Predict
    with torch.no_grad():
        outputs = model(img)
        _, predicted = torch.max(outputs, 1)

    class_index = predicted.item()
    class_names = ['Bean', 'BitterG', 'BottleG', 'Brinjal', 'Broccoli', 
                   'cabbage', 'capsicum', 'carrot', 'cauuliflower', 
                   'cucumber', 'papaya', 'potato', 'pumpkin', 'radish', 
                   'tomato']
    predicted_class = class_names[class_index]

    return jsonify({'prediction': predicted_class})

if __name__ == '__main__':
    app.run(debug=True)
