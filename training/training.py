import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Step 1: Load and preprocess the dataset
df0 = pd.read_csv('./training/data/clothing_items.csv', sep=",")
df1 = pd.read_csv('./training/data/clothing_items_new_500.csv', sep=",")
df2 = pd.read_csv('./training/data/clothing_items_new2_1000.csv', sep=",")

df = pd.concat([df0, df1, df2], ignore_index=True)

# One-hot encode categorical columns
df_encoded = pd.get_dummies(df, columns=['type', 'brand', 'material', 'style', 'color', 'state'])

mode_values = df.mode().iloc[0]

# Split into features and target variable
X = df_encoded.drop('price', axis=1).values
y = df_encoded['price'].values

# Step 2: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Random Forest
rf_model = RandomForestRegressor()
rf_model.fit(X_train_scaled, y_train)
y_pred_rf = rf_model.predict(X_test_scaled)

mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest MAE: {mae_rf:.2f}, R2 Score: {r2_rf:.2f}")

# Exporting RandomForest model
model_filename = 'random_forest_model.pkl'
joblib.dump(rf_model, model_filename)

# Exporting scalar
joblib.dump(scaler, 'scaler.pkl')

# Export encoded columns
joblib.dump(df_encoded.columns, 'model_columns.pkl')