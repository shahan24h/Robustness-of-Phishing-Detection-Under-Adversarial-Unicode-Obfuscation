import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# --------------------------------------------------
# Paths
# --------------------------------------------------
combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

# --------------------------------------------------
# Load combined dataset
# --------------------------------------------------
df = pd.read_csv(combined_path)

# Build modeling dataset
# Now we use the *poisoned* body as the text we see in production
df_model = df.dropna(subset=["body_poisoned", "is_modified"]).copy()
df_model["label"] = df_model["is_modified"].astype(int)
df_model["text"] = df_model["body_poisoned"]
df_model = df_model[["text", "label"]]

print("Modeling dataset shape:", df_model.shape)
print(df_model.head(3))

# --------------------------------------------------
# Train / test split
# --------------------------------------------------
X = df_model["text"]
y = df_model["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# --------------------------------------------------
# Char-level TF-IDF
# --------------------------------------------------
char_tfidf = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    lowercase=False,
    max_features=50000,
)

X_train_char = char_tfidf.fit_transform(X_train)
X_test_char = char_tfidf.transform(X_test)

print("Char TF-IDF train shape:", X_train_char.shape)
print("Char TF-IDF test shape:", X_test_char.shape)

# --------------------------------------------------
# Logistic Regression with class_weight="balanced"
# --------------------------------------------------
clf = LogisticRegression(
    max_iter=1000,
    n_jobs=-1,
    class_weight="balanced",
)

clf.fit(X_train_char, y_train)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------
y_pred = clf.predict(X_test_char)

print("\n=== Classification report (CHAR TF-IDF on POISONED text) ===")
print(classification_report(y_test, y_pred, digits=4))

print("=== Confusion matrix ===")
print(confusion_matrix(y_test, y_pred))
