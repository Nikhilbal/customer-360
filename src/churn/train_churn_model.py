import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib

# Paths
DATA_PATH = "data/feature_store/churn_dataset.csv"
MODEL_PATH = "models/churn_model.pkl"
SCALER_PATH = "models/scaler.pkl"

print("\n🚀 Training Churn Prediction Model...")

# Load dataset
df = pd.read_csv(DATA_PATH)
print(f"📥 Loaded churn dataset: {df.shape}")

# ---- FIX: Remove non-numeric columns ----
drop_cols = ["customer_unique_id", "last_purchase_date", "first_purchase_date"]
df = df.drop(columns=drop_cols, errors="ignore")

# Separate features & label
X = df.drop(columns=["is_churn"])
y = df["is_churn"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🔍 Scaling numerical features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

# Evaluation
print("\n📊 Model Evaluation:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model & scaler
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print(f"\n💾 Model saved to: {MODEL_PATH}")
print(f"💾 Scaler saved to: {SCALER_PATH}")
print("\n🎯 Training complete!")
