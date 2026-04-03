# Crop Recommendation ML Project

This project predicts the most suitable crop to plant based on soil and weather parameters using machine learning models. It includes data exploration, preprocessing, model training, evaluation, and saving the best model.

---

## Dataset
The dataset `Crop_recommendation.csv` contains the following features:

| Feature      | Description                          |
|--------------|--------------------------------------|
| N            | Nitrogen content in soil              |
| P            | Phosphorus content in soil            |
| K            | Potassium content in soil             |
| temperature  | Temperature in °C                     |
| humidity     | Relative humidity (%)                 |
| ph           | pH value of soil                      |
| rainfall     | Rainfall in mm                        |
| label        | Crop name (target variable)           |

---

## Project Steps

1. **Exploratory Data Analysis (EDA)**  
   - Checked for missing values and duplicates.  
   - Analyzed data types, unique values, and basic statistics.  
   - Visualized crop distribution using bar charts.

2. **Data Preprocessing**  
   - Split data into training and testing sets (80-20 split).  
   - Standardized numerical features for KNN, Logistic Regression, and SVM.

3. **Model Training & Evaluation**  
   - Models used:
     - Random Forest
     - Decision Tree
     - K-Nearest Neighbors (KNN)
     - Logistic Regression
     - Support Vector Machine (SVM with RBF kernel)
   - Evaluated models using **accuracy score**.  
   - **Random Forest** performed the best.

4. **Model Saving**  
   - Saved the trained Random Forest model as `Crop_recommendation_RF.pkl` using `pickle`.

5. **Prediction Example**
```python
sample = {'N':90, 'P':40, 'K':40, 'temperature':20, 'humidity':80, 'ph':7, 'rainfall':200}
X = [[sample[c] for c in b["feature_cols"]]]
predicted_crop = b["model"].predict(X)[0]
print("Predicted Crop:", predicted_crop)

```
Requirements
Python 3.x
pandas
numpy
matplotlib
scikit-learn

You can install dependencies via:

pip install pandas numpy matplotlib scikit-learn

How to Run
1.Clone the repository:
git clone https://github.com/YOUR_USERNAME/Crop-Recommendation-ML.git
2.Open Crop_Recommendation_ML.ipynb in Jupyter Notebook or Google Colab.
3.Run each cell to explore the data, train models, and make predictions.
