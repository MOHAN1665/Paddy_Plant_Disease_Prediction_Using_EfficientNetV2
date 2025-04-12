# 🌱 Plant Disease Detection System

![Project Banner](static/paddy.jpg)  
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

🖥️ Usage Demo
Upload Interface
Upload Screen

Results Page
Results Screen

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
