# Social Engineering & Adversarial Obfuscation  
### in Business Email Compromise (BEC) Attacks

> **Analysis of how Unicode-based adversarial techniques undermine NLP-driven email security — and how character-level models recover lost signal.**

---

##  Project Motivation

Business Email Compromise (BEC) remains one of the most costly forms of cybercrime.  
Modern email security systems rely heavily on **machine learning and natural language processing**, yet sophisticated attackers increasingly exploit **Unicode-based obfuscation** to evade detection.

This project investigates:
- how **social-engineering language** (urgency, authority, obligation) is encoded in BEC emails,
- how adversarial Unicode manipulation **breaks keyword- and token-based detectors**, and
- how **character-level models** can reliably detect these attacks without relying on semantics.

---

##  Key Contributions

✅ Quantified linguistic patterns used in BEC social engineering  
✅ Measured **70–90% signal loss** in keyword-based detectors under Unicode obfuscation  
✅ Demonstrated **81% evasion rate** against naive rule-based systems  
✅ Built a **95%+ accuracy adversarial obfuscation detector** using character n-grams  
✅ Interpreted model features to expose homoglyph and zero-width Unicode artifacts  

---

## Threat Model (At a Glance)

| Actor | Capability |
|-----|------------|
| Attacker | Unicode-aware adversarial manipulation |
| Target | ML-based email security systems |
| Technique | Homoglyph substitution & zero-width injection |
| Constraint | Preserve human readability |
| Goal | Evade automated phishing detection |

---
Thank you and appriciate for the dataset. 
Data_credit: https://doi.org/10.34740/kaggle/ds/5074342
