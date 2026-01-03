import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Load data
df = pd.read_csv("../data/debt_data.csv")

X = df[["amount", "days_overdue", "past_history_score"]]
y = df["recovered"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Advanced AI Model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluation
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"✅ Advanced AI Model Accuracy: {accuracy:.2f}")

# Save model
joblib.dump(model, "model.pkl")
print("💾 Advanced model saved as model.pkl")
