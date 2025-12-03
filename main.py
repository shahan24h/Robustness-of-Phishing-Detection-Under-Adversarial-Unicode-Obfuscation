import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
clean_path = r"S:\Adversarial BEC\data\synthetic_emails.csv"
poisoned_path = r"S:\Adversarial BEC\data\synthetic_emails_poisoned.csv"
output_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

# --------------------------------------------------
# Load datasets
# --------------------------------------------------
df_clean = pd.read_csv(clean_path)
df_poisoned = pd.read_csv(poisoned_path)

print("Original CLEAN shape:", df_clean.shape)
print("Original POISONED shape:", df_poisoned.shape)

# --------------------------------------------------
# Drop rows with missing labels (keep only labeled emails)
# --------------------------------------------------
df_clean_valid = df_clean.dropna(subset=["label"]).copy()
df_poisoned_valid = df_poisoned.dropna(subset=["label"]).copy()

df_clean_valid.reset_index(drop=True, inplace=True)
df_poisoned_valid.reset_index(drop=True, inplace=True)

print("\nClean valid shape:", df_clean_valid.shape)
print("Poisoned valid shape:", df_poisoned_valid.shape)

# --------------------------------------------------
# Compare email bodies
# --------------------------------------------------
same_body = df_clean_valid["body"] == df_poisoned_valid["body"]

n_same = same_body.sum()
n_diff = (~same_body).sum()

print(f"\nNumber of identical bodies: {n_same}")
print(f"Number of different bodies: {n_diff}")

# Show a couple of example differences
diff_clean = df_clean_valid.loc[~same_body]
diff_poisoned = df_poisoned_valid.loc[~same_body]

print("\n=== Example of CLEAN vs POISONED email bodies ===")
for i in range(min(2, len(diff_clean))):
    print(f"\n--- Example {i + 1} ---")
    print("\n[CLEAN BODY]\n")
    print(diff_clean.iloc[i]["body"])
    print("\n[POISONED BODY]\n")
    print(diff_poisoned.iloc[i]["body"])
    print("\n" + "-" * 60)

# --------------------------------------------------
# Build combined dataframe
# --------------------------------------------------
combined = pd.DataFrame({
    "subject": df_clean_valid["subject"],
    "body_clean": df_clean_valid["body"],
    "body_poisoned": df_poisoned_valid["body"],
})

combined["is_modified"] = combined["body_clean"] != combined["body_poisoned"]
combined["label"] = 1  # all are BEC phishing emails

print("\nCombined shape:", combined.shape)
print("Modified emails:", combined['is_modified'].sum())
print("Unmodified emails:", (~combined['is_modified']).sum())

print("\n=== Sample combined rows ===")
print(combined.head(3))

# --------------------------------------------------
# Save combined dataset
# --------------------------------------------------
combined.to_csv(output_path, index=False)
print(f"\nSaved combined dataset to: {output_path}")
