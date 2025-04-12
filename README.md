<div align="center">
# 🌱 Plant Disease Detection System
</div>
![Project Banner](static/examples/paddy.png)  
*An AI-powered solution for detecting diseases in rice plants*

## 🚀 Features

- **Accurate Disease Detection**: Identifies common rice plant diseases with high accuracy
- **Heatmap Visualization**: Grad-CAM heatmaps highlight affected areas
- **Confidence Metrics**: Shows prediction confidence levels
- **Responsive Design**: Works on desktop and mobile devices
- **User-Friendly Interface**: Simple upload and results workflow

## 🛠️ Technologies Used

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey?logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.6+-orange?logo=tensorflow)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1+-purple?logo=bootstrap)
![FontAwesome](https://img.shields.io/badge/Font_Awesome-6.0+-blue?logo=font-awesome)

## 📦 Installation

1. Clone the repository
```bash
git clone https://github.com/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2.git
cd plant-disease-detection
```
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
flask run
```
5. Open your browser at ```http://localhost:5000```

## 🖥️ Usage Demo

<div align="center" style="margin: 30px 0;">
  <div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;">
    <div style="flex: 1; min-width: 300px; max-width: 400px; text-align: center;">
      <h4 style="margin-bottom: 15px; color: #2c3e50;">📤 Upload Interface</h4>
      <a href="static/screenshots/upload.png" target="_blank" style="text-decoration: none;">
        <img src="static/screenshots/upload_thumb.png" alt="Upload Interface" 
             style="width: 100%; max-width: 350px; border-radius: 10px; 
                    box-shadow: 0 6px 12px rgba(0,0,0,0.15); transition: transform 0.3s ease;">
        <p style="font-size: 0.9em; color: #7f8c8d; margin-top: 10px;">
          <i>Click to view full screenshot</i>
        </p>
      </a>
    </div>
    <div style="flex: 1; min-width: 300px; max-width: 400px; text-align: center;">
      <h4 style="margin-bottom: 15px; color: #2c3e50;">📊 Results Page</h4>
      <a href="static/screenshots/results.png" target="_blank" style="text-decoration: none;">
        <img src="static/screenshots/results_thumb.png" alt="Results Page" 
             style="width: 100%; max-width: 350px; border-radius: 10px; 
                    box-shadow: 0 6px 12px rgba(0,0,0,0.15); transition: transform 0.3s ease;">
        <p style="font-size: 0.9em; color: #7f8c8d; margin-top: 10px;">
          <i>Click to view full screenshot</i>
        </p>
      </a>
    </div>
    
  </div>
</div>

### Step-by-Step Guide:
1. **Upload Page**:
   - Click "Choose File" to select plant image
   - Supported formats: JPG, PNG (max 5MB)
   - Click "Predict" to analyze

2. **Results Page**:
   - View original image + heatmap visualization
   - See disease prediction with confidence percentage
   - Options to:
     - View disease details
     - Report incorrect predictions
     - Upload new image


## 🌿 Supported Diseases

<div align="center">

| Disease Name | Example Image | Description | Confidence Threshold |
|--------------|---------------|-------------|----------------------|
| **Hispa** | <img src="static/examples/hispa.jpeg" width="150"> | Caused by leaf miners creating white streaks | >75% |
| **Tungro** | <img src="static/examples/tungro.jpeg" width="150"> | Yellow-orange discoloration of leaves | >70% |
| **Blast Disease** | <img src="static/examples/blast.jpeg" width="150"> | Diamond-shaped lesions with gray centers | >80% |
| **Brown Spot** | <img src="static/examples/brown.jpg" width="150"> | Small brown spots with yellow halos | >65% |
| **Healthy Plant** | <img src="static/examples/healthy.jpg" width="150"> | No disease detected | >90% |

</div>

## 🏗️ Project Architecture

```mermaid
graph TD
    A[Client Browser] -->|HTTP Request| B[Flask Server]
    B --> C[Image Preprocessing]
    C --> D[TensorFlow Model]
    D --> E[Grad-CAM Heatmap]
    E --> F[Result Generation]
    F -->|JSON Response| A
    D --> G[Database]
    G -->|Store Reports| H[(MySQL/PostgreSQL)]
    style A fill:#4CAF50,stroke:#388E3C
    style B fill:#2196F3,stroke:#0D47A1
    style D fill:#FF9800,stroke:#E65100
```
## 📂 Directory Structure
```bash
plant-disease-detector/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── disease_reports.json  # User-submitted disease reports
│
├── static/               # All static assets
│   ├── main.css          # Global styles
│   ├── script.js         # Frontend interactivity
│   ├── examples/         # Sample disease images
│   └── screenshots/      # Application screenshots
│
├── templates/            # Frontend templates
│   ├── index.html        # Main upload interface
│   └── results.html      # Prediction results page
│   └── and other diseases related html files
│
└── models/               # AI Model files
    ├── model.pth         # PyTorch trained weights
    └── model.ipynb       # Jupyter notebooks
```

## 🤝 How to Contribute

We welcome contributions from the community! To help improve this project:

1. **Fork** the repository:  
   [![Fork](https://img.shields.io/github/forks/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2?style=social)](https://github.com/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2/fork)

2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name

3. **Commit** your changes:
   ```bash
   git commit -m "Add: your feature description"

4. **Push** to your branch:
   ```bash
   git push origin feature/your-feature-name

5. **Open** a Pull Request with:
   Description of changes
   Screenshots (if applicable)
   Reference to related issues

## 📜 License

```text
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📬 Contact

**Project Maintainer**:  
[![GitHub Profile](https://img.shields.io/badge/👨💻_GitHub-Profile-181717?style=for-the-badge&logo=github)](https://github.com/MOHAN1665)  
[![Email Contact](https://img.shields.io/badge/📧_Email-Contact%20Me-D14836?style=for-the-badge&logo=gmail)](mailto:pmohankumar854@gmail.com)

**Project Links**:  
[![Repository](https://img.shields.io/badge/📂_Repo-Paddy_Plant_Disease_Prediction-8A2BE2?style=for-the-badge)](https://github.com/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2)  
[![Open Issues](https://img.shields.io/github/issues-raw/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2?color=green&label=🐞%20Issues&style=for-the-badge)](https://github.com/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2/issues)

---

<div align="center" style="margin-top: 20px;">
  <a href="https://github.com/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2/stargazers">
    <img src="https://img.shields.io/github/stars/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2?style=social" alt="Stars">
  </a>
  <a href="https://github.com/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2/network/members">
    <img src="https://img.shields.io/github/forks/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2?style=social" alt="Forks">
  </a>
  <a href="https://github.com/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/MOHAN1665/Paddy_Plant_Disease_Prediction_Using_EfficientNetV2?color=blue" alt="License">
  </a>
</div>
