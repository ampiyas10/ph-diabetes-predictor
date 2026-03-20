
# 🇵🇭 Philippine Diabetes Risk Predictor
### by Ampiyas Ⓣ

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-purple.svg)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<div align="center">
  <img src="https://via.placeholder.com/800x400/0038a8/ffffff?text=Philippine+Diabetes+Risk+Predictor" alt="App Banner" width="80%">
  <br>
  <em>Matalinong Solusyon para sa Kalusugan ng Pilipino</em>
</div>

## 📋 **Project Overview**

An AI-powered web application that predicts diabetes risk using machine learning. Built with PyTorch and deployed as a user-friendly web interface, this tool is designed specifically with the Filipino population in mind.

### **Why This Matters for the Philippines**
- 🇵🇭 Diabetes is the **5th leading cause of death** in the Philippines
- 📈 **4.3 million** Filipinos affected (as of 2021)
- 🔍 An estimated **2.8 million cases remain undiagnosed**
- 🎯 Projected to reach **7.5 million by 2045**

## ✨ **Features**

- ✅ **AI-Powered Predictions** - Uses a trained PyTorch neural network
- ✅ **Instant Results** - Get your risk assessment in seconds
- ✅ **User-Friendly Interface** - Simple form for health data entry
- ✅ **Bilingual Support** - Results shown in English and Filipino
- ✅ **Risk Factor Analysis** - Identifies specific health concerns
- ✅ **Mobile Responsive** - Works on phones, tablets, and desktop

## 🏗️ **Project Structure**

```
ph-diabetes-predictor/
├── app/
│   ├── app.py                 # Flask web application
│   └── templates/
│       ├── index.html          # Home page with form
│       └── result.html         # Results page
├── src/
│   ├── model.py                # PyTorch neural network
│   ├── data_loader.py          # Data preprocessing
│   └── train.py                # Training script
├── saved_models/
│   └── diabetes_model.pth      # Trained model weights
├── data/
│   └── diabetes.csv            # Dataset
├── notebooks/                   # Jupyter notebooks for EDA
├── tests/                       # Unit tests
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render deployment config
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 🚀 **Live Demo**

🌐 **Try it yourself:** [https://ph-diabetes-predictor.onrender.com](https://ph-diabetes-predictor.onrender.com)

## 📊 **Model Performance**

| Metric | Score | Interpretation |
|--------|-------|----------------|
| **Accuracy** | ~78% | Overall correct predictions |
| **Sensitivity** | ~75% | Correctly identifies diabetes cases |
| **Specificity** | ~80% | Correctly identifies non-diabetes cases |

### **Features Used**
The model uses 8 medical features:
1. **Pregnancies** - Number of times pregnant
2. **Glucose** - Plasma glucose concentration (mg/dL)
3. **BloodPressure** - Diastolic blood pressure (mmHg)
4. **SkinThickness** - Triceps skin fold thickness (mm)
5. **Insulin** - 2-Hour serum insulin (μU/mL)
6. **BMI** - Body Mass Index (kg/m²)
7. **DiabetesPedigreeFunction** - Family history score
8. **Age** - Patient's age (years)

## 💻 **Local Installation**

### **Prerequisites**
- Python 3.8 or higher
- Git
- pip (Python package manager)

### **Step-by-Step Setup**

```bash
# 1. Clone the repository
git clone https://github.com/ampiyas10/ph-diabetes-predictor.git
cd ph-diabetes-predictor

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download dataset
python download_data.py

# 6. Train the model
python -c "from src.train import train_model; train_model()"

# 7. Run the web app
python app/app.py
```

Open your browser and go to **http://localhost:5000**

## 🧪 **Running Tests**

```bash
pytest tests/ -v
```

## 🌐 **Deployment**

This app is configured for easy deployment on Render:

1. Fork/clone this repository
2. Create an account on [render.com](https://render.com)
3. Click "New Blueprint" and connect your GitHub repo
4. Render automatically detects the `render.yaml` configuration
5. Your app will be live in minutes!

## 🎯 **Usage Guide**

1. **Enter your health metrics** in the form
2. **Click "Predict Risk"** to get your assessment
3. **Review your results** showing:
   - Risk percentage
   - Risk category (Low/Moderate/High)
   - Personalized recommendations
   - Identified risk factors

### **Risk Categories**
- 🟢 **Low Risk (<40%)**: Maintain healthy habits
- 🟡 **Moderate Risk (40-70%)**: Consider lifestyle changes
- 🔴 **High Risk (>70%)**: Consult healthcare provider immediately

## 📈 **Future Enhancements**

- [ ] Train on Philippine-specific clinical data
- [ ] Add support for regional languages (Tagalog, Cebuano, Ilocano)
- [ ] Integrate with local health information systems
- [ ] Add PDF report generation
- [ ] Create mobile app version
- [ ] Add user accounts to track history
- [ ] Include dietary recommendations based on Filipino cuisine

## 🤝 **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 **Medical Disclaimer**

> **⚠️ IMPORTANT**: This tool is for **educational and informational purposes only**. It is not a medical device and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for proper evaluation and management of diabetes or any other health condition.

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Ampiyas Ⓣ**
- GitHub: [@ampiyas10](https://github.com/ampiyas10)
- Project Link: [https://github.com/ampiyas10/ph-diabetes-predictor](https://github.com/ampiyas10/ph-diabetes-predictor)

## 🙏 **Acknowledgments**

- Pima Indians Diabetes Dataset
- Philippine Department of Health for health statistics
- PyTorch community for excellent documentation
- Render.com for free hosting

## 📊 **Stats**

![GitHub stars](https://img.shields.io/github/stars/ampiyas10/ph-diabetes-predictor?style=social)
![GitHub forks](https://img.shields.io/github/forks/ampiyas10/ph-diabetes-predictor?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/ampiyas10/ph-diabetes-predictor?style=social)

---

<div align="center">
  <strong>Matalinong Solusyon para sa Kalusugan ng Pilipino</strong>
  <br>
  Ⓣ Ampiyas 2024 | All Rights Reserved
  <br>
  <sub>Made with ❤️ for the Filipino people</sub>
</div>
```

## 📸 **Add a Screenshot (Optional but Recommended)**

To make your README even better, add a screenshot of your app:

1. Run your app locally: `python app/app.py`
2. Go to http://localhost:5000
3. Take a screenshot (Windows key + Shift + S)
4. Save it as `screenshot.png` in your project folder
5. Update the README to show the real screenshot:


Go to: `https://github.com/ampiyas10/ph-diabetes-predictor`

