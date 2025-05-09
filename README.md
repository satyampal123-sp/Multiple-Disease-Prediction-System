# Multiple Disease Prediction Streamlit App

A Streamlit web application that uses machine learning models to predict multiple diseases based on the user's health data. This app allows users to input their health parameters and receive predictions for diseases such as **Heart Disease**, **Diabetes**, **Parkinson’s Disease**, **Liver Disease**, and **Kidney Disease**.

## Features

* **Heart Disease Prediction**: Predict whether the user is at risk of heart disease.
* **Diabetes Prediction**: Predict whether the user is likely to have diabetes.
* **Parkinson’s Disease Prediction**: Predict the likelihood of Parkinson's disease based on speech-related features.
* **Liver Disease Prediction**: Predict the likelihood of liver disease based on user-provided medical test results.
* **Kidney Disease Prediction**: Predict the likelihood of kidney disease based on health indicators.
* **Interactive Web Interface**: The app is built with Streamlit to offer an intuitive and simple interface for users to input their data and get results.

## Technologies Used

* **Python**: The main programming language.
* **Streamlit**: For creating the interactive web application.
* **Scikit-learn**: Machine learning library used to train models and make predictions.
* **Pandas**: For data manipulation and preprocessing.
* **NumPy**: For handling numerical data and array operations.
* **Joblib**: For saving and loading trained models.
* **Matplotlib** (optional): For visualizing results and plots.
* streamlit_option_menu: This allows the user to select between different prediction models, such as Heart Disease, Diabetes, and Kidney Disease.

## Installation

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/multiple-disease-prediction-streamlit-app.git
cd multiple-disease-prediction-streamlit-app
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

You can create a virtual environment to avoid conflicts with other projects.

```bash
python -m venv venv
```

Activate the virtual environment:

* On Windows:

  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies

Install the required libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Alternatively, you can install the libraries manually:

```bash
pip install streamlit scikit-learn streamlit_option_menu pandas numpy joblib matplotlib
```

### 4. Run the Application

Run the app using Streamlit:

```bash
streamlit run app.py
```

Your app will open in your default web browser at `http://localhost:8501`.

## How It Works

1. **Input Data**: Users input their health information through the app's user interface, such as age, cholesterol levels, BMI, glucose levels, etc., depending on which disease they want to predict.

2. **Machine Learning Models**: Based on the user's inputs, the system uses pre-trained machine learning models to make predictions. The models have been trained using datasets relevant to each disease.

   * **Heart Disease Prediction**: Logistic Regression or Random Forest Classifier.
   * **Diabetes Prediction**: Support Vector Machine (SVM) or Decision Trees.
   * **Parkinson’s Disease Prediction**: Random Forest or SVM.
   * **Liver Disease Prediction**: Logistic Regression or Random Forest Classifier.
   * **Kidney Disease Prediction**: Logistic Regression, Decision Trees, or Random Forest.

3. **Prediction Results**: The system displays the prediction results, showing whether the user is at risk for a given disease or not.

## Prediction Models

The system uses different machine learning models for each type of disease prediction:

### Heart Disease Prediction Model

* **Input Parameters**: Age, gender, cholesterol level, blood pressure, etc.
* **Model**: Logistic Regression / Random Forest Classifier
* **Prediction Output**: `1` (heart disease) or `0` (no heart disease)

### Diabetes Prediction Model

* **Input Parameters**: Glucose level, BMI, number of pregnancies, insulin, age, etc.
* **Model**: Support Vector Machine (SVM)
* **Prediction Output**: `1` (diabetic) or `0` (not diabetic)

### Parkinson’s Disease Prediction Model

* **Input Parameters**: Various voice-related features (e.g., mean pitch, jitter).
* **Model**: Random Forest Classifier or SVM
* **Prediction Output**: `1` (Parkinson's disease) or `0` (no Parkinson's disease)

### Liver Disease Prediction Model

* **Input Parameters**: Age, bilirubin levels, albumin, total protein, etc.
* **Model**: Logistic Regression / Random Forest Classifier
* **Prediction Output**: `1` (liver disease) or `2` (no liver disease)

### Kidney Disease Prediction Model

* **Input Parameters**: Age, blood pressure, specific gravity, albumin, blood glucose, etc.
* **Model**: Logistic Regression, Decision Trees, or Random Forest
* **Prediction Output**: `1` (kidney disease) or `0` (no kidney disease)

## Example Screenshots

Here are some examples of how the app looks:
![image](https://github.com/user-attachments/assets/e73df9ba-5118-4d8e-adff-0bc9e40ccaad)
![image](https://github.com/user-attachments/assets/47d63e90-1acf-4756-b0b9-e6cd5e638b77)
![image](https://github.com/user-attachments/assets/b3e2b4ea-9846-4614-ac37-579462cc0c07)
![image](https://github.com/user-attachments/assets/6d1c1559-954e-4b0f-afd8-b7ef7e4e3d81)
![image](https://github.com/user-attachments/assets/2667f28d-7746-44e8-a1d6-d24307f4c465)
![image](https://github.com/user-attachments/assets/f9027f75-ac81-419c-9a4c-eba40628ed26)
![image](https://github.com/user-attachments/assets/356fa4f7-83c4-4f64-a4a7-3c975553affc)






