import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

# --------------------------------------------------
# Load combined dataset
# --------------------------------------------------
df = pd.read_csv(combined_path)

print("Original combined shape:", df.shape)
print(df.head(3))

# --------------------------------------------------
# Build modeling dataset
# Task: predict whether an email is adversarially modified (is_modified)
# Input text: CLEAN body (body_clean)
# Label: is_modified (0 = clean, 1 = poisoned)
# --------------------------------------------------
# Drop any rows where body_clean is missing (just in case)
df_model = df.dropna(subset=["body_clean", "is_modified"]).copy()

# Ensure label is integer 0/1
df_model["label"] = df_model["is_modified"].astype(int)

# Rename text column for clarity
df_model["text"] = df_model["body_clean"]

# Keep only what we need for modeling (you can keep more later if needed)
df_model = df_model[["text", "label"]]

print("\nModeling dataset shape:", df_model.shape)
print(df_model.head(3))

# Class balance
label_counts = df_model["label"].value_counts()
print("\nLabel distribution (0 = clean, 1 = modified):")
print(label_counts)

n_total = len(df_model)
for value, count in label_counts.items():
    pct = count / n_total * 100
    print(f"Label {value}: {count} emails ({pct:.2f}%)")
