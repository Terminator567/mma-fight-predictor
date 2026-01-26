from data.get_data import get_dataframe
from data_processor.calculate_stats import calculate_statistics
from data_processor.data_categorising import categories_columns
from data_processor.data_cleaner import clean_data
from data_processor.fight_stats import finalProcessingForFighter, calculateAverages
from data_processor.data_types_fixes import check_and_process_data_type, drop_col_for_training
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
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

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

best_k = None
best_acc = -1.0

k_range = range(1, 51)  
for k in k_range:
    model = KNeighborsClassifier(n_neighbors=k, weights="distance")
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, pred)

    if acc > best_acc:
        best_acc = acc
        best_k = k

best_model = KNeighborsClassifier(n_neighbors=best_k, weights="distance")
best_model.fit(X_train_scaled, y_train)
best_pred = best_model.predict(X_test_scaled)

print(f"\nBest k: {best_k} with accuracy: {best_acc}")
print("\nConfusion Matrix:\n", confusion_matrix(y_test, best_pred))
print("\nClassification Report:\n", classification_report(y_test, best_pred))
