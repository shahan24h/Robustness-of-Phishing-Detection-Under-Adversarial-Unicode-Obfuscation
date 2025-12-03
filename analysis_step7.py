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

# Compute risk score on CLEAN bodies for all emails
df["risk_clean"] = df["body_clean"].apply(risk_score)

modified = df[df["is_modified"] == True].copy()
unmodified = df[df["is_modified"] == False].copy()

print("Total emails:", len(df))
print("Modified emails:", len(modified))
print("Unmodified emails:", len(unmodified))

print("\n=== Average risk score (CLEAN text) ===")
print(f"Modified   mean risk_clean: {modified['risk_clean'].mean():.3f}")
print(f"Unmodified mean risk_clean: {unmodified['risk_clean'].mean():.3f}")

# How many emails contain at least one keyword?
modified["has_any_keyword"] = modified["risk_clean"] > 0
unmodified["has_any_keyword"] = unmodified["risk_clean"] > 0

mod_with_kw = modified["has_any_keyword"].mean() * 100
unmod_with_kw = unmodified["has_any_keyword"].mean() * 100

print("\n=== % of emails with at least one keyword (CLEAN text) ===")
print(f"Modified   with >=1 keyword: {mod_with_kw:.2f}%")
print(f"Unmodified with >=1 keyword: {unmod_with_kw:.2f}%")
