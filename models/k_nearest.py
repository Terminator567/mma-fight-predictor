from data.get_data import get_dataframe
from data_processor.calculate_stats import calculate_statistics
from data_processor.data_categorising import categories_columns
from data_processor.data_cleaner import clean_data
from data_processor.fight_stats import finalProcessingForFighter, calculateAverages
from data_processor.data_types_fixes import check_and_process_data_type, drop_col_for_training
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
from sklearn.pipeline import Pipeline
import numpy as np

og_df = get_dataframe('original.csv')
cleaned_df = clean_data(og_df)
cleaned_df["target"] = (cleaned_df["Winner"] == cleaned_df["Fighter 1"]).astype(int)

stats_df = calculate_statistics(cleaned_df)
processed_df = finalProcessingForFighter(stats_df)
processed_df = check_and_process_data_type(processed_df)
avg_df = calculateAverages(processed_df)
cat_df = categories_columns(avg_df)
df_for_training = drop_col_for_training(cat_df)

X = df_for_training.drop(columns=["Target"])
y = df_for_training["Target"]
X = X.select_dtypes(include=[np.number]).fillna(0)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier())
])

param_grid = {
    "knn__n_neighbors": range(1, 51),
    "knn__weights": ["uniform", "distance"],
    "knn__p": [1, 2], 
    "knn__leaf_size": [10, 20, 30, 40, 50],
}

grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    scoring="accuracy",
    n_jobs=-1
)

grid.fit(X_train, y_train)
best_model = grid.best_estimator_

y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

print("Best CV accuracy:", grid.best_score_)
print("Best parameters:", grid.best_params_)

print("\nTest Accuracy:", accuracy_score(y_test, y_pred))
print("ROC-AUC Score:", roc_auc_score(y_test, y_proba))

print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
