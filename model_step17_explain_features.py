import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# --------------------------------------------------
# Paths
# --------------------------------------------------
combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

# --------------------------------------------------
# Load combined dataset
# --------------------------------------------------
df = pd.read_csv(combined_path)

df_model = df.dropna(subset=["body_poisoned", "is_modified"]).copy()
df_model["label"] = df_model["is_modified"].astype(int)
df_model["text"] = df_model["body_poisoned"]
df_model = df_model[["text", "label"]]

# --------------------------------------------------
# Train / test split
# --------------------------------------------------
X = df_model["text"]
y = df_model["label"]

X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --------------------------------------------------
# Char-level TF-IDF
# --------------------------------------------------
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    lowercase=False,
    max_features=50000,
)

X_train_char = vectorizer.fit_transform(X_train)

# --------------------------------------------------
# Train logistic regression
# --------------------------------------------------
clf = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    n_jobs=-1,
)
clf.fit(X_train_char, y_train)

# --------------------------------------------------
# Extract feature weights
# --------------------------------------------------
feature_names = np.array(vectorizer.get_feature_names_out())
coefficients = clf.coef_[0]

# Top features for modified (label = 1)
top_modified_idx = np.argsort(coefficients)[-30:][::-1]
top_modified = list(zip(feature_names[top_modified_idx], coefficients[top_modified_idx]))

# Top features for clean (label = 0)
top_clean_idx = np.argsort(coefficients)[:30]
top_clean = list(zip(feature_names[top_clean_idx], coefficients[top_clean_idx]))

print("\n=== Top character n-grams indicating MODIFIED emails ===")
for feat, weight in top_modified:
    print(f"{repr(feat):>12}  weight={weight:.4f}")

print("\n=== Top character n-grams indicating CLEAN emails ===")
for feat, weight in top_clean:
    print(f"{repr(feat):>12}  weight={weight:.4f}")
