from pathlib import Path
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import metrics

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "backend" / "data" / "processed.csv"

df = pd.read_csv(DATA_PATH)

features = [
    "Total_KD",
    "Total_STR",
    "Total_TD",
    "Total_SUB",
    "Opp_KD",
    "Opp_STR",
    "Opp_TD",
    "Opp_SUB",
    "Avg_Round_Time",
    "Avg_Round",
    "Opp_Avg_Round_Time",
    "Opp_Avg_Round",
    "Weight_Class_code",
]

target = "Target"

df = df[features + [target]].dropna()

X = df[features]
y = df[target]

x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

pipe = Pipeline([
    ("classifier", RandomForestClassifier(
        n_estimators=500,
        random_state=42,
        class_weight="balanced_subsample",
        max_depth=8,
        min_samples_leaf=8,
        min_samples_split=20,
        bootstrap=True,
        n_jobs=-1,
    ))
])

grid = GridSearchCV(
    pipe,
    param_grid={},
    cv=2,
    scoring="roc_auc",
    n_jobs=-1
)

grid.fit(x_train, y_train)

y_pred = grid.predict(x_test)
y_proba = grid.predict_proba(x_test)[:, 1]

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))
print("ROC-AUC:", metrics.roc_auc_score(y_test, y_proba))

save_dir = PROJECT_ROOT / "saved_models"
save_dir.mkdir(parents=True, exist_ok=True)

model_path = save_dir / "RandomForestClassifierModel.joblib"
joblib.dump(grid, model_path)

print(f"Saved model to: {model_path}")