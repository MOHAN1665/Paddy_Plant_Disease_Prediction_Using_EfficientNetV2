import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import time
import torch.serialization
import json
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_PATH = 'models/best_model.pth'
IMAGE_SIZE = 256
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
REPORTS_FILE = 'disease_reports.json'


INVALID_IMAGE_THRESHOLDS = {
    'min_green_ratio': 0.15,  # Minimum green pixels to be considered a plant
    'min_edge_ratio': 0.05,   # Minimum edge density for texture
    'min_dimension': 100      # Minimum image width/height in pixels
}


# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    'high': 0.75,
    'medium': 0.5,
    'low': 0.3
}

# EXACT class order from Colab's label_encoder.classes_
CLASS_NAMES = [
    'bacterial_leaf_blight',    # Index 0
    'bacterial_leaf_streak',    # Index 1
    'bacterial_panicle_blight', # Index 2
    'blast',                    # Index 3
    'brown_spot',               # Index 4
    'dead_heart',               # Index 5
    'downy_mildew',            # Index 6
    'hispa',                    # Index 7
    'normal',                   # Index 8
    'tungro'                    # Index 9
]

# Display names mapping
CLASS_DISPLAY_NAMES = {
    'bacterial_leaf_blight': 'Bacterial Leaf Blight',
    'bacterial_leaf_streak': 'Bacterial Leaf Streak',
    'bacterial_panicle_blight': 'Bacterial Panicle Blight',
    'blast': 'Blast',
    'brown_spot': 'Brown Spot',
    'dead_heart': 'Dead Heart',
    'downy_mildew': 'Downy Mildew',
    'hispa': 'Hispa',
    'normal': 'Healthy',
    'tungro': 'Tungro',
    'unknown': 'Unknown Disease'
}

# Initialize disease reports file if it doesn't exist
if not os.path.exists(REPORTS_FILE):
    with open(REPORTS_FILE, 'w') as f:
        json.dump([], f)
        
# Model Architecture
class EfficientNetV2WithCAM(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.backbone = models.efficientnet_v2_s(weights=None)
        self.features = self.backbone.features
        self.avgpool = self.backbone.avgpool
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(self.backbone.classifier[1].in_features, num_classes)
        )
        
        # Grad-CAM hooks
        self.gradients = None
        self.activations = None
        target_layer = self.features[-1][-1]
        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        self.activations = output
    
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]
    
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)

# Model Loading
def load_model():
    model = EfficientNetV2WithCAM(num_classes=10)
    device = torch.device("cpu")  # Force CPU for consistent behavior
    
    try:
        # Explicitly allow numpy.ndarray for safe loading
        with torch.serialization.safe_globals([torch._utils._rebuild_tensor_v2, np.ndarray]):
            checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=True)
        
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
            
        model.to(device)
        model.eval()
        print("✅ Model loaded safely with weights_only=True")
        return model
    except Exception as e:
        print(f"⚠️ Safe loading failed: {e}")
        # Fallback to unsafe loading with explicit warning
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
        print("⚠️ Attempting unsafe load - ONLY use if you trust the model source")
        checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)
        
        # Handle different checkpoint formats
        state_dict = checkpoint.get('model_state_dict', checkpoint)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        return model
    
# Initialize model
model = load_model()

# Image transformations (MUST match training)
transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_report(report_data):
    """Save unknown disease report to JSON file"""
    try:
        with open(REPORTS_FILE, 'r+') as f:
            reports = json.load(f)
            report_data['timestamp'] = datetime.now().isoformat()
            reports.append(report_data)
            f.seek(0)
            json.dump(reports, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving report: {e}")
        return False

def is_valid_plant_image(img_path):
    """Check if image appears to be a plant leaf"""
    try:
        img = cv2.imread(img_path)
        if img is None:
            return False
            
        h, w = img.shape[:2]
        if min(h, w) < INVALID_IMAGE_THRESHOLDS['min_dimension']:
            return False
            
        # Color analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv, (30, 50, 30), (85, 255, 255))
        green_ratio = cv2.countNonZero(green_mask) / (h * w)
        
        # Texture analysis
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_ratio = cv2.countNonZero(edges) / (h * w)
        
        return (green_ratio > INVALID_IMAGE_THRESHOLDS['min_green_ratio'] or 
                edge_ratio > INVALID_IMAGE_THRESHOLDS['min_edge_ratio'])
    except Exception as e:
        print(f"Image validation error: {e}")
        return False

# Prediction Function
def predict_image(img_path):
    try:
        # First validate it's a plant image
        if not is_valid_plant_image(img_path):
            return "Invalid Image (Not a Plant)", 0.0, "invalid"
            
        img = Image.open(img_path).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            output = model(img_tensor)
            probs = torch.softmax(output, dim=1)
            pred_class = torch.argmax(probs).item()
            confidence = float(probs[0][pred_class].item())
            
            class_name = CLASS_NAMES[pred_class]
            display_name = CLASS_DISPLAY_NAMES.get(class_name, class_name)
            
            if confidence < CONFIDENCE_THRESHOLDS['medium']:
                return "Unknown Disease", confidence, "unknown"
                
        return display_name, confidence, class_name
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error", 0.0, "error"
    
# Grad-CAM Function
def generate_gradcam(img_path):
    try:
        # 1. Load and prepare image
        img = Image.open(img_path).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(DEVICE)
        original_img = np.array(img)
        h, w = original_img.shape[:2]
        
        # 2. Forward pass
        model.zero_grad()
        output = model(img_tensor)
        pred_class = torch.argmax(output).item()
        
        # 3. Backward pass - critical fix for gradient capture
        output[0][pred_class].backward(retain_graph=True)
        
        # 4. Get gradients and activations - ensure they exist
        if model.gradients is None or model.activations is None:
            raise RuntimeError("Failed to capture gradients or activations")
            
        gradients = model.gradients.detach().cpu().numpy()[0]
        activations = model.activations.detach().cpu().numpy()[0]
        
        # 5. Process CAM - improved calculation
        weights = np.mean(gradients, axis=(1, 2), keepdims=True)
        cam = np.sum(weights * activations, axis=0)
        
        # 6. Enhanced normalization
        cam = np.maximum(cam, 0)  # ReLU
        cam = cv2.resize(cam, (w, h))
        cam = cam - np.min(cam)
        cam = cam / (np.max(cam) + 1e-8)  # Avoid division by zero
        
        # 7. Create heatmap with better visibility
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        # 8. Superimpose with optimal blending
        superimposed = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)
        
        # 9. Improved contour detection
        gray_cam = np.uint8(255 * cam)
        _, binary_map = cv2.threshold(gray_cam, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 10. Find and draw contours - more reliable
        contours, _ = cv2.findContours(binary_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw bounding boxes only if significant area found
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(cnt)
                
                # Draw rectangle
                cv2.rectangle(superimposed, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Draw label
                cv2.putText(superimposed, 
                           f"Disease Area ({area}px)", 
                           (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        return Image.fromarray(superimposed), CLASS_NAMES[pred_class]
        
    except Exception as e:
        print(f"Grad-CAM Error: {str(e)}")
        # Create error image with diagnostics
        error_img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(error_img)
        draw.text((10, 40), f"Visualization Failed: {str(e)}", fill='red')
        return error_img, "Error"
          
# Flask Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save file
        filename = f"{int(time.time())}_{secure_filename(file.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)
        
        # Get prediction
        display_name, confidence, class_name = predict_image(filepath)
        
        # Generate Grad-CAM
        gradcam_img, _ = generate_gradcam(filepath)
        gradcam_path = os.path.join(UPLOAD_FOLDER, f"gradcam_{filename}")
        gradcam_img.save(gradcam_path)
        
        return jsonify({
            'prediction': display_name,
            'class_name': class_name,  # Internal class name
            'confidence': round(confidence, 4),
            'image_url': f"/{filepath}",
            'gradcam_url': f"/{gradcam_path}"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/report_unknown', methods=['POST'])
def report_unknown():
    try:
        report_data = {
            'observations': request.form.get('observations', ''),
            'email': request.form.get('email', ''),
            'image_path': request.form.get('image_path', ''),
            'prediction': request.form.get('prediction', ''),
            'confidence': request.form.get('confidence', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        if not report_data['observations']:
            return jsonify({'error': 'Observations are required'}), 400
            
        if save_report(report_data):
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to save report'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/new/<page>')
def disease_pages(page):
    return render_template(f'new/{page}')

if __name__ == '__main__':
    # Verify class order on startup
    print("\n=== Class Indices Verification ===")
    for idx, name in enumerate(CLASS_NAMES):
        print(f"{idx}: {name} (Display: {CLASS_DISPLAY_NAMES.get(name, 'N/A')})")
    
    print("\n=== Confidence Thresholds ===")
    print(f"High: {CONFIDENCE_THRESHOLDS['high']}, Medium: {CONFIDENCE_THRESHOLDS['medium']}, Low: {CONFIDENCE_THRESHOLDS['low']}")
    
    # Run app
    app.run(host='0.0.0.0', port=5000, debug=True)