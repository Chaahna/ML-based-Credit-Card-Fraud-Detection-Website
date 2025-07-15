# ML-based-Credit-Card-Fraud-Detection-Website
A machine learning-powered web application that detects fraudulent transactions in real-time. The app uses three trained models k-Nearest Neighbors, Logistic Regression, and Naive Bayes to classify input features and flag anomalies. Built with a simple UI and a backend pipeline that consolidates model predictions for improved accuracy.

## 🔍 Project Overview

Financial fraud detection is a critical application of machine learning. In this project, we simulate a real-world use case where user-input transaction features are passed to trained ML models to assess risk in real-time.

Each model returns a prediction, and the final classification is determined based on majority voting or a selected strategy.

## 🚀 Features

- Real-time fraud detection through a web interface
- Trained and deployed multiple models for prediction
- Simple UI for user interaction
- Scikit-learn used for model development and integration

## 🧠 ML Models Used

- **k-Nearest Neighbors (k-NN)**
- **Logistic Regression**
- **Naive Bayes**

All models were trained on a credit card dataset, preprocessed with feature selection, scaling, and balancing techniques (if applicable).

## 🖥️ Tech Stack

- **Frontend:** HTML, CSS (basic interface)
- **Backend:** Python (Flask)
- **ML Framework:** scikit-learn
- **Other Libraries:** NumPy, Pandas, Matplotlib, joblib

## 🛠️ Installation
**Clone the repository**
   ```bash
   git clone https://github.com/Chaahna/ML-based-Credit-Card-Fraud-Detection-Website.git
   cd ML-based-Credit-Card-Fraud-Detection-Website


## 📈 Future Improvements
-Add model evaluation dashboards (ROC curves, confusion matrices)
-Use ensemble voting strategies or stacking
-Improve UI design and form validations
-Deploy to a cloud platform (e.g., Heroku or Render)
