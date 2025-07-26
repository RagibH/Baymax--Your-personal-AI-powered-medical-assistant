"""
Train‑and‑save a Liver Disease prediction model.

USAGE
=====
python liver_disease_training.py  # expects Liver_disease_data.csv in same folder
"""

# ───────────────────────────────────────────────────────────────────────────────
# 1. Imports
# ───────────────────────────────────────────────────────────────────────────────
import os
import joblib
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    RocCurveDisplay,
)

# ───────────────────────────────────────────────────────────────────────────────
# 2. Parameters (tweak as you like)
# ───────────────────────────────────────────────────────────────────────────────
CSV_PATH      = "Liver_disease_data.csv"   # ← Rename if your file is elsewhere
MODEL_OUTFILE = "liver_disease_model.joblib"
TEST_SIZE     = 0.20
RANDOM_SEED   = 42

# ───────────────────────────────────────────────────────────────────────────────
# 3. Load & inspect data
# ───────────────────────────────────────────────────────────────────────────────
print("Loading dataset …")
df = pd.read_csv(CSV_PATH)

print("\n▶ Shape:", df.shape)
print("\n▶ Head:")
print(df.head())

print("\n▶ Description:")
print(df.describe())

print("\n▶ Missing‑value count:")
print(df.isnull().sum())

# If any NaNs exist, you can handle them here. Example:
# df.fillna(df.median(numeric_only=True), inplace=True)

# ───────────────────────────────────────────────────────────────────────────────
# 4. (Optional) quick correlation heat‑map
# ───────────────────────────────────────────────────────────────────────────────
sns.set(style="ticks", font_scale=0.9)
plt.figure(figsize=(10, 7))
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Feature correlation matrix")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")   # Saved for later viewing
plt.close()

# ───────────────────────────────────────────────────────────────────────────────
# 5. Feature / target split
# ───────────────────────────────────────────────────────────────────────────────
X = df.drop("Diagnosis", axis=1)
y = df["Diagnosis"]

# ───────────────────────────────────────────────────────────────────────────────
# 6. Train / validation split
# ───────────────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_SEED
)

# ───────────────────────────────────────────────────────────────────────────────
# 7. Build a pipeline (scaling → gradient boosting)
#    GradientBoosting usually works very well on tabular data.
# ───────────────────────────────────────────────────────────────────────────────
pipe = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("clf", GradientBoostingClassifier(random_state=RANDOM_SEED)),
    ]
)

# ───────────────────────────────────────────────────────────────────────────────
# 8. Hyper‑parameter search (quick grid – expand if you want)
# ───────────────────────────────────────────────────────────────────────────────
param_grid = {
    "clf__n_estimators": [100, 200],
    "clf__learning_rate": [0.05, 0.1],
    "clf__max_depth": [2, 3],
}

print("\nSearching best hyper‑parameters …")
grid = GridSearchCV(
    pipe,
    param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    verbose=1,
)

grid.fit(X_train, y_train)
print("Best params:", grid.best_params_)
model = grid.best_estimator_

# ───────────────────────────────────────────────────────────────────────────────
# 9. Evaluation
# ───────────────────────────────────────────────────────────────────────────────
def evaluate(split_name, y_true, y_pred, proba=None):
    acc = accuracy_score(y_true, y_pred)
    print(f"\n🎯 {split_name} accuracy: {acc:.4f}")
    print("\nClassification report:")
    print(classification_report(y_true, y_pred))
    print("Confusion matrix:\n", confusion_matrix(y_true, y_pred))
    if proba is not None:
        auc = roc_auc_score(y_true, proba[:, 1])
        print(f"ROC‑AUC: {auc:.4f}")

# Training metrics
y_train_pred = model.predict(X_train)
y_train_proba = model.predict_proba(X_train)
evaluate("TRAIN", y_train, y_train_pred, y_train_proba)

# Test metrics
y_test_pred = model.predict(X_test)
y_test_proba = model.predict_proba(X_test)
evaluate("TEST", y_test, y_test_pred, y_test_proba)

# Plot ROC curve for the test set
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title("ROC curve – Test set")
plt.savefig("roc_curve.png")
plt.close()

# ───────────────────────────────────────────────────────────────────────────────
# 10. Persist model
# ───────────────────────────────────────────────────────────────────────────────
joblib.dump(model, MODEL_OUTFILE)
print(f"\n✅ Model saved to {MODEL_OUTFILE}")

# ───────────────────────────────────────────────────────────────────────────────
# 11. Quick smoke test – load model & predict a single synthetic sample
# ───────────────────────────────────────────────────────────────────────────────
print("\nLoading model back for sanity check …")
loaded_model = joblib.load(MODEL_OUTFILE)

sample = pd.DataFrame(
    {
        "Age": [45],
        "Gender": [1],
        "BMI": [27.3],
        "Alcohol Consumption": [5],
        "Smoking": [0],
        "Genetic Risk": [1],
        "Physical Activity": [3],
        "Diabetes": [0],
        "Hypertension": [1],
        "Liver Function Test": [55],
    }
)
pred = loaded_model.predict(sample)[0]
print("Sample prediction (1 = disease, 0 = healthy):", pred)

# ───────────────────────────────────────────────────────────────────────────────
# 12. Next steps (not executed) – using the model in Baymax
# ───────────────────────────────────────────────────────────────────────────────
"""
# In your Baymax prediction module (e.g., liver_pred.py):

import joblib
import pandas as pd

model = joblib.load("liver_disease_model.joblib")

def predict_liver_disease(sample_dict):
    df = pd.DataFrame([sample_dict])
    return int(model.predict(df)[0])
"""
