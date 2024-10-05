import streamlit as st
import pandas as pd
import joblib

# Load the trained RandomForest model and preprocessing components
rf_model = joblib.load('./model/random_forest_model.pkl')
scaler = joblib.load('./model/scaler.pkl')  # Load the scaler if it was used during training
feature_columns = joblib.load('./model/model_columns.pkl')  # Load saved feature columns

modes = {
    'type': 'jacket',
    'brand': 'h&m',
    'material': 'cotton',
    'style': 'casual',
    'color': 'black',
    'state': 'new'
}

# Example Usage
input_features = ['jeans', 'h&m', 'polyester', 'casual', 'white', 'new']  # Replace with your values

# Assume that the order of features in the list is consistent with the order used during training
column_names = ['type', 'brand', 'material', 'style', 'color', 'state']  # Define the column names

for i in range(len(input_features)):
    if f'{column_names[i]}_{input_features[i]}' not in feature_columns:
        input_features[i] = modes[column_names[i]]

# Converting input features to dataframe
input_data = pd.DataFrame([input_features], columns=column_names)

# encode the input data
input_data_encoded = pd.get_dummies(input_data)
print(input_data_encoded)

# align the encoded input DataFrame with the feature columns used during training
aligned_input_data = pd.DataFrame(columns=feature_columns)  # Create an empty DataFrame with the feature columns
aligned_input_data = pd.concat([aligned_input_data, input_data_encoded], ignore_index=True)  # Append the encoded input data as a new row
aligned_input_data = aligned_input_data.fillna(0)  # Fill missing columns with 0

# Step 4: Scale the aligned input data (if a scaler was used during training)
aligned_input_data_scaled = scaler.transform(aligned_input_data.values)

print(aligned_input_data)

# Step 5: Make the prediction
predicted_price = rf_model.predict(aligned_input_data_scaled)

print(f"Predicted Price: {predicted_price[0]:.2f}")