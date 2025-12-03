import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv(combined_path)

# Focus on adversarially modified emails (where poisoning actually happened)
modified = df[df["is_modified"] == True].copy()

print("Total emails:", len(df))
print("Modified emails:", len(modified))

# --------------------------------------------------
# Obligation / urgency lexicon
# --------------------------------------------------
OBLIGATION_URGENCY = [
    "must",
    "need to",
    "needed to",
    "required",
    "require you to",
    "you are required",
    "you are instructed",
    "you are hereby",
    "asap",
    "as soon as possible",
    "immediately",
    "by end of day",
    "by the end of day",
    "by close of business",
    "without delay",
    "no delay",
    "urgent",
    "urgently",
    "at once",
]

def count_lexicon(text: str, lexicon):
    if not isinstance(text, str):
        return 0
    t = text.lower()
    return sum(t.count(w) for w in lexicon)

# --------------------------------------------------
# Compute counts on CLEAN vs POISONED bodies
# --------------------------------------------------
modified["obligation_clean"] = modified["body_clean"].apply(lambda t: count_lexicon(t, OBLIGATION_URGENCY))
modified["obligation_poisoned"] = modified["body_poisoned"].apply(lambda t: count_lexicon(t, OBLIGATION_URGENCY))

# Binary flags: has any obligation/urgency phrasing
modified["has_obligation_clean"] = modified["obligation_clean"] > 0
modified["has_obligation_poisoned"] = modified["obligation_poisoned"] > 0

print("\n=== Obligation / urgency stats (MODIFIED emails only) ===")
print("Mean obligation_clean:", modified["obligation_clean"].mean())
print("Mean obligation_poisoned:", modified["obligation_poisoned"].mean())

pct_clean = modified["has_obligation_clean"].mean() * 100
pct_poisoned = modified["has_obligation_poisoned"].mean() * 100

print(f"% with any obligation/urgency phrase (CLEAN): {pct_clean:.2f}%")
print(f"% with any obligation/urgency phrase (POISONED): {pct_poisoned:.2f}%")

# --------------------------------------------------
# How many emails lose all explicit obligation/urgency signals?
# --------------------------------------------------
lost_all = ((modified["has_obligation_clean"] == True) & (modified["has_obligation_poisoned"] == False)).sum()
kept_any = ((modified["has_obligation_clean"] == True) & (modified["has_obligation_poisoned"] == True)).sum()

print(f"\nModified emails with obligation in CLEAN: {modified['has_obligation_clean'].sum()}")
print(f"  → of those, lost all in POISONED: {lost_all}")
print(f"  → of those, kept some in POISONED: {kept_any}")

if modified["has_obligation_clean"].sum() > 0:
    lost_pct = lost_all / modified["has_obligation_clean"].sum() * 100
    print(f"Percent that lose all explicit obligation/urgency phrasing after poisoning: {lost_pct:.2f}%")

# --------------------------------------------------
# Show a few example emails where obligation/urgency disappears
# --------------------------------------------------
print("\n=== Examples where obligation/urgency disappears after poisoning ===")
lost_examples = modified[(modified["has_obligation_clean"] == True) & (modified["has_obligation_poisoned"] == False)].head(3)

for i, row in lost_examples.iterrows():
    print(f"\n--- Example {i} ---")
    print("[CLEAN body]\n")
    print(row["body_clean"])
    print("\n[POISONED body]\n")
    print(row["body_poisoned"])
    print("\n" + "-" * 60)
