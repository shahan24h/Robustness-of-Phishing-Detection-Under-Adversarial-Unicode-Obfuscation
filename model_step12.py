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
df_model = df.dropna(subset=["body_clean", "is_modified"]).copy()
df_model["label"] = df_model["is_modified"].astype(int)
df_model["text"] = df_model["body_clean"]
df_model = df_model[["text", "label"]]

print("Modeling dataset shape:", df_model.shape)

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
# TF-IDF vectorization
# --------------------------------------------------
tfidf = TfidfVectorizer(
    lowercase=True,
    stop_words="english",   # you can experiment with this later
    max_features=20000,     # limit vocab size
    ngram_range=(1, 2),     # unigrams + bigrams
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print("TF-IDF train shape:", X_train_tfidf.shape)
print("TF-IDF test shape:", X_test_tfidf.shape)

# --------------------------------------------------
# Logistic Regression classifier (baseline)
# --------------------------------------------------
clf = LogisticRegression(
    max_iter=1000,
    n_jobs=-1,
)

clf.fit(X_train_tfidf, y_train)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------
y_pred = clf.predict(X_test_tfidf)

print("\n=== Classification report (Logistic Regression, TF-IDF) ===")
print(classification_report(y_test, y_pred, digits=4))

print("=== Confusion matrix ===")
print(confusion_matrix(y_test, y_pred))
