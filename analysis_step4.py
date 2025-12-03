import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

# --------------------------------------------------
# Load combined dataset
# --------------------------------------------------
df = pd.read_csv(combined_path)

print("Combined shape:", df.shape)
print(df.head(3))

# --------------------------------------------------
# 1) Basic length statistics
# --------------------------------------------------
df["len_clean_chars"] = df["body_clean"].str.len()
df["len_poisoned_chars"] = df["body_poisoned"].str.len()

df["len_clean_words"] = df["body_clean"].str.split().str.len()
df["len_poisoned_words"] = df["body_poisoned"].str.split().str.len()

print("\n=== Length statistics (characters) ===")
print(df[["len_clean_chars", "len_poisoned_chars"]].describe())

print("\n=== Length statistics (words) ===")
print(df[["len_clean_words", "len_poisoned_words"]].describe())

# --------------------------------------------------
# 2) Keyword frequency analysis (clean vs poisoned)
# --------------------------------------------------
# Keywords that are typical of BEC / social engineering
keywords = [
    "urgent",
    "immediately",
    "wire",
    "transfer",
    "payment",
    "invoice",
    "account",
    "confirm",
    "confidential",
    "authorization",
]

def keyword_counts(series, keyword):
    # simple lowercase contains check
    return series.str.lower().str.contains(keyword).sum()

print("\n=== Keyword frequencies in CLEAN vs POISONED bodies ===")
for kw in keywords:
    clean_count = keyword_counts(df["body_clean"], kw)
    poisoned_count = keyword_counts(df["body_poisoned"], kw)
    print(f"\nKeyword: '{kw}'")
    print(f"  CLEAN   contains: {clean_count}")
    print(f"  POISONED contains: {poisoned_count}")

# --------------------------------------------------
# 3) Same keyword analysis restricted to MODIFIED emails only
# --------------------------------------------------
modified_df = df[df["is_modified"] == True].copy()

print("\nNumber of modified emails:", len(modified_df))

print("\n=== Keyword frequencies in MODIFIED emails only ===")
for kw in keywords:
    clean_count_mod = keyword_counts(modified_df["body_clean"], kw)
    poisoned_count_mod = keyword_counts(modified_df["body_poisoned"], kw)
    print(f"\nKeyword: '{kw}' (modified subset)")
    print(f"  CLEAN   contains: {clean_count_mod}")
    print(f"  POISONED contains: {poisoned_count_mod}")

import pandas as pd

combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

df = pd.read_csv(combined_path)

df["len_clean_chars"] = df["body_clean"].str.len()
df["len_poisoned_chars"] = df["body_poisoned"].str.len()
df["len_clean_words"] = df["body_clean"].str.split().str.len()
df["len_poisoned_words"] = df["body_poisoned"].str.split().str.len()

keywords = [
    "urgent",
    "immediately",
    "wire",
    "transfer",
    "payment",
    "invoice",
    "account",
    "confirm",
    "confidential",
    "authorization",
]

def keyword_counts(series, keyword):
    return series.str.lower().str.contains(keyword).sum()

modified_df = df[df["is_modified"] == True].copy()

# --------------------------------------------------
# Compute % drop per keyword for MODIFIED emails
# --------------------------------------------------
rows = []
for kw in keywords:
    clean_count_mod = keyword_counts(modified_df["body_clean"], kw)
    poisoned_count_mod = keyword_counts(modified_df["body_poisoned"], kw)
    if clean_count_mod > 0:
        drop_abs = clean_count_mod - poisoned_count_mod
        drop_pct = drop_abs / clean_count_mod * 100.0
    else:
        drop_abs = 0
        drop_pct = 0.0
    rows.append({
        "keyword": kw,
        "clean_count_modified": clean_count_mod,
        "poisoned_count_modified": poisoned_count_mod,
        "absolute_drop": drop_abs,
        "percent_drop": drop_pct,
    })

drop_df = pd.DataFrame(rows)

print("\n=== Keyword robustness in MODIFIED emails (clean → poisoned) ===")
print(drop_df.sort_values("percent_drop", ascending=False).to_string(index=False))


import pandas as pd

combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

df = pd.read_csv(combined_path)

keywords = [
    "urgent",
    "immediately",
    "wire",
    "transfer",
    "payment",
    "invoice",
    "account",
    "confirm",
    "confidential",
    "authorization",
]

def keyword_present(text, keyword):
    if not isinstance(text, str):
        return False
    return keyword in text.lower()

def risk_score(text):
    if not isinstance(text, str):
        return 0
    t = text.lower()
    return sum(keyword_present(t, kw) for kw in keywords)

# Only look at adversarially MODIFIED emails
modified_df = df[df["is_modified"] == True].copy()

# Compute risk scores for clean vs poisoned bodies
modified_df["risk_clean"] = modified_df["body_clean"].apply(risk_score)
modified_df["risk_poisoned"] = modified_df["body_poisoned"].apply(risk_score)

print("\n=== Risk score summary (modified emails only) ===")
print(modified_df[["risk_clean", "risk_poisoned"]].describe())

# Choose a simple threshold: score >= 2 → suspicious
threshold = 2

modified_df["flag_clean"] = modified_df["risk_clean"] >= threshold
modified_df["flag_poisoned"] = modified_df["risk_poisoned"] >= threshold

n_modified = len(modified_df)
n_flag_clean = modified_df["flag_clean"].sum()
n_flag_poisoned = modified_df["flag_poisoned"].sum()

# Emails that were flagged when clean, but NOT flagged when poisoned
evaded = ((modified_df["flag_clean"] == True) & (modified_df["flag_poisoned"] == False)).sum()

print(f"\nTotal modified emails: {n_modified}")
print(f"Flagged (CLEAN body): {n_flag_clean}")
print(f"Flagged (POISONED body): {n_flag_poisoned}")
print(f"Emails that evaded detection after poisoning: {evaded}")

if n_flag_clean > 0:
    evasion_rate = evaded / n_flag_clean * 100.0
    print(f"Evasion rate among originally flagged emails: {evasion_rate:.2f}%")

print("\n=== Sample of emails that evaded detection ===")
evaded_examples = modified_df[(modified_df["flag_clean"] == True) & (modified_df["flag_poisoned"] == False)].head(3)

for i, row in evaded_examples.iterrows():
    print(f"\n--- Example {i} ---")
    print(f"risk_clean = {row['risk_clean']}, risk_poisoned = {row['risk_poisoned']}")
    print("\n[CLEAN BODY]\n")
    print(row["body_clean"])
    print("\n[POISONED BODY]\n")
    print(row["body_poisoned"])
    print("\n" + "-" * 60)
