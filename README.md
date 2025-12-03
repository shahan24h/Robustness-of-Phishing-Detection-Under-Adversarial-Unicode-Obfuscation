#  Robustness of Phishing Detection  
## Under Adversarial Unicode Obfuscation

> **An empirical study of whether modern ML-based phishing detectors remain effective when phishing emails are deliberately obfuscated using Unicode homoglyphs and zero-width characters.**

---

##  Overview

Unicode-based adversarial obfuscation techniques—such as homoglyph substitution and zero-width character injection—are increasingly used to evade NLP-based security systems.  
In **Social-Engineering-Adversarial-Obfuscation-in-BEC-Emails (path: https://github.com/shahan24h/Social-Engineering-Adversarial-Obfuscation-in-BEC-Emails.git) 
I showed that such attacks devastate keyword- and rule-based detectors.

This project investigates a follow-up question:

> **Are modern ML-based phishing classifiers robust to these Unicode obfuscation attacks?**

Rather than assuming failure, this project explicitly **measures robustness** under controlled conditions.

---

##  Research Question

**Does adversarial Unicode obfuscation significantly degrade the performance of a phishing vs benign email classifier trained on clean text?**

---

##  Datasets
###  Benign Emails
- Non-spam, non-phishing emails
- Extracted from a **public Hugging Face email spam classification dataset**
  - Dataset: `UniqueData/email-spam-classification`
- Only `"not spam"` emails were used as benign samples
- Represents legitimate communication such as:
  - transactional updates
  - informational messages
  - normal professional emails

###  Phishing Emails (BEC)
- 4,151 synthetic **Business Email Compromise (BEC)** phishing emails
- Each email has two aligned versions:
  - `body_clean`: original text
  - `body_poisoned`: adversarially obfuscated text
- ~29% of emails contain Unicode attacks:
  - Latin–Cyrillic homoglyph substitution
  - Zero-width Unicode injection
- Covers realistic fraud scenarios:
  - invoice fraud
  - wire transfer requests
  - executive impersonation

---

###  Benign Emails
- Non-spam, non-phishing emails
- Extracted from a modern public email classification dataset
- Only `"not spam"` emails used
- Represents legitimate communication such as:
  - transactional updates
  - informational messages
  - normal professional emails

---

##  Experimental Setup

### Task
Binary classification:
- `0` → benign email  
- `1` → phishing email  

### Model
- **Word-level TF-IDF**
  - unigrams + bigrams
- **Logistic Regression**
  - class-weighted to handle imbalance

### Training
- Trained **only on clean emails**
- No exposure to adversarial text during training

### Evaluation Strategy
The same trained model is evaluated on:
1. **Clean test set**  
2. **Poisoned test set**  
   - phishing emails replaced with adversarially obfuscated versions
   - benign emails unchanged  

Additionally, a focused evaluation is performed on **only those phishing emails that were actually adversarially modified**.

---

## Results

###  Baseline Performance (All Test Emails)

| Metric | Clean Test | Poisoned Test |
|-----|-----------|---------------|
| Accuracy | ~99.8% | ~99.8% |
| Phishing recall | ~100% | ~100% |
| Benign recall | ~83% | ~83% |

**Observation:**  
Replacing phishing emails with their obfuscated versions does **not** change overall performance.

---

###  Focused Robustness Evaluation  
**(Adversarially Modified Phishing Emails Only)**

- 230 adversarially modified phishing emails in the test set

| Input Version | Phishing Recall |
|--------------|-----------------|
| Clean text   | 100% |
| Poisoned text | 100% |

**All adversarially modified phishing emails were still detected correctly.**

---

##  Interpretation

Why does obfuscation *not* hurt performance here?

- The model relies on a **rich distribution of features**, not just a few sensitive keywords.
- Even when terms like *payment* or *invoice* are obfuscated, many other signals remain:
  - overall language patterns
  - sentence structure
  - stylistic repetition
- The phishing vs benign boundary is **highly separable** in this experimental setup.

This highlights an important distinction:

> Unicode attacks cripple surface-level keyword systems, but are less effective against richer ML representations when the class boundary is strong.

---

##  Relationship to Project #1

| Aspect | Project #1 | Project #2 |
|-----|-----------|------------|
| Detector | Rule / keyword-based | ML-based |
| Attack impact | 81% evasion | No measurable drop |
| Feature level | Surface tokens | Distributional text features |
| Insight | Extremely brittle | Robust in this setting |

Together, the two projects illustrate **both sides of the defense spectrum**.

---

## Limitations

- Benign dataset is relatively small
- Domain mismatch between enterprise BEC emails and general benign emails
- Synthetic phishing content
- Linear model only (no deep contextual embeddings)

These limitations are acknowledged explicitly.

---

##  Security Implications

- Keyword-driven defenses alone are unsafe against Unicode adversarial attacks
- ML-based detectors can be robust—but robustness depends on:
  - feature richness
  - dataset balance
- Best practice:
  - layered defense
  - semantic phishing detection
  - adversarial obfuscation monitoring (Project #1)

---

## Key Takeaway

> Unicode-based adversarial attacks severely degrade keyword-driven defenses, but in this controlled setting they **do not significantly reduce the effectiveness of a modern ML-based phishing classifier**, underscoring the value of richer textual representations and defense-in-depth.

---

## 🚀 Future Extensions
*(Not required, but natural next steps)*

- Balance benign and phishing samples
- Restrict features to simulate weaker detectors
- Compare word-level vs character-level phishing models
- Integrate adversarial obfuscation detection into the pipeline

---

