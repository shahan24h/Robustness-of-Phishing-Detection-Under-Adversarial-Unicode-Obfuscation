import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
combined_path = r"S:\Adversarial BEC\data\bec_combined_clean_poisoned.csv"

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv(combined_path)

# We focus on CLEAN bodies for tone / social engineering
texts = df["body_clean"].fillna("")

# --------------------------------------------------
# Lexicons for social-engineering tone
# --------------------------------------------------
AUTHORITY_WORDS = [
    "directive",
    "instruction",
    "instructed",
    "mandate",
    "mandatory",
    "required",
    "you are required",
    "you are hereby",
    "under my authority",
    "per our policy",
    "per company policy",
    "as per policy",
    "authorized",
    "you are instructed",
]

ROLE_POWER_WORDS = [
    "ceo",
    "cfo",
    "coo",
    "vp",
    "vice president",
    "director",
    "executive",
    "chairman",
    "board",
    "owner",
]

POLITENESS_WORDS = [
    "please",
    "kindly",
    "would you",
    "could you",
    "appreciate",
    "thank you",
    "thanks",
    "your cooperation",
]

THREAT_WORDS = [
    "failure to",
    "consequences",
    "disciplinary",
    "non-compliance",
    "breach",
    "jeopardizing",
    "jeopardizing the deal",
    "jeopardizing the company",
    "ramifications",
]

def count_lexicon(text: str, lexicon):
    """Count how many lexicon phrases appear in text (case-insensitive)."""
    t = text.lower()
    return sum(t.count(w) for w in lexicon)

# --------------------------------------------------
# Compute counts on CLEAN text
# --------------------------------------------------
df["authority_count"] = texts.apply(lambda t: count_lexicon(t, AUTHORITY_WORDS))
df["role_power_count"] = texts.apply(lambda t: count_lexicon(t, ROLE_POWER_WORDS))
df["politeness_count"] = texts.apply(lambda t: count_lexicon(t, POLITENESS_WORDS))
df["threat_count"] = texts.apply(lambda t: count_lexicon(t, THREAT_WORDS))

# Binary flags
df["has_authority"] = df["authority_count"] > 0
df["has_role_power"] = df["role_power_count"] > 0
df["has_politeness"] = df["politeness_count"] > 0
df["has_threat"] = df["threat_count"] > 0

modified = df[df["is_modified"] == True].copy()
unmodified = df[df["is_modified"] == False].copy()

print("Total emails:", len(df))
print("Modified emails:", len(modified))
print("Unmodified emails:", len(unmodified))

def summarize_group(name, group):
    print(f"\n=== Tone summary: {name} ===")
    print(f"Mean authority_count: {group['authority_count'].mean():.3f}")
    print(f"Mean role_power_count: {group['role_power_count'].mean():.3f}")
    print(f"Mean politeness_count: {group['politeness_count'].mean():.3f}")
    print(f"Mean threat_count: {group['threat_count'].mean():.3f}")

    print(f"\n% with any authority phrase: {group['has_authority'].mean() * 100:.2f}%")
    print(f"% with any power-role term: {group['has_role_power'].mean() * 100:.2f}%")
    print(f"% with any politeness phrase: {group['has_politeness'].mean() * 100:.2f}%")
    print(f"% with any threat phrase: {group['has_threat'].mean() * 100:.2f}%")

summarize_group("MODIFIED (clean text)", modified)
summarize_group("UNMODIFIED (clean text)", unmodified)

# --------------------------------------------------
# Show a few examples of high-authority / low-politeness vs high-politeness
# --------------------------------------------------
print("\n=== Example: high authority, low politeness ===")
high_auth = df[(df["authority_count"] > 0) & (df["politeness_count"] == 0)].head(2)
for i, row in high_auth.iterrows():
    print(f"\n--- Email {i} ---")
    print(row["body_clean"])
    print("\n" + "-" * 60)

print("\n=== Example: high politeness, low authority ===")
high_polite = df[(df["politeness_count"] > 0) & (df["authority_count"] == 0)].head(2)
for i, row in high_polite.iterrows():
    print(f"\n--- Email {i} ---")
    print(row["body_clean"])
    print("\n" + "-" * 60)
