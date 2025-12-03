1. Adversarial obfuscation significantly reduces the effectiveness of keyword-based or naive NLP detectors, despite leaving the human-perceived meaning and urgency intact.
   
2. Adversarial obfuscation removes 70–90% of direct keyword signal for core financial and urgency terms, while preserving human-readable intent.



---

1\. Keyword-based social engineering signals



To approximate classic rule-based email security, I defined a small lexicon of high-risk terms commonly associated with Business Email Compromise (e.g., urgent, immediately, wire, transfer, payment, invoice, account, confirm, confidential, authorization).



On the clean BEC emails, these terms are frequent and strongly present:



Many emails contain at least one urgency or payment-related keyword.



The average “risk score” (number of matched keywords per email) among modified emails is 1.55, compared with 1.50 among unmodified emails.



Emails that are later adversarially modified are slightly more likely to include at least one high-risk keyword in their clean form (73% vs 68%).



This suggests that obfuscation is applied more often to messages that are already linguistically “loud” from a social-engineering perspective.



2\. Impact of adversarial obfuscation on keyword detection



For the subset of adversarially modified emails (N = 1,217), I compared the presence of each keyword in the clean vs poisoned versions of the same message. For several core financial and urgency terms, direct string matches drop dramatically:



“invoice”: 83 → 6 occurrences (93% drop)



“immediately”: 182 → 20 (89% drop)



“payment”: 432 → 81 (81% drop)



“account”: 312 → 62 (80% drop)



“confirm”: 262 → 57 (78% drop)



Even though the semantics and intent remain obvious to a human reader, the surface-form string patterns that keyword systems rely on are largely destroyed.



3\. Evasion of a simple keyword-based detector



I then implemented a minimal “risk score” detector:



Score = number of risk keywords appearing in the email body.



Threshold: score ≥ 2 ⇒ email is flagged as suspicious.



On the clean text of the adversarially modified emails:



519 / 1,217 emails (≈43%) would be flagged by this simple rule.



On the poisoned text:



Only 97 / 1,217 emails (≈8%) remain flagged.



In other words:



422 emails (81.3% of those originally flagged) successfully evade the keyword-based detector after obfuscation is applied.



This demonstrates that Unicode-based adversarial obfuscation can eliminate 70–90% of the detectable keyword signal in high-risk BEC emails, even though the social-engineering content is preserved.



--------------------------------------------------------Measure “authority” vs “politeness” language



Using simple lexicons for authority, role power, politeness, and threat language, I find that adversarially modified BEC emails are tonally very similar to unmodified ones. Around 27% of modified emails and 26.6% of unmodified emails contain explicit authority phrasing (e.g., “you are hereby instructed”, “as per company policy”), while 11.9% vs 10.9% contain threat or consequence-related language. Explicit high-power roles (CEO, CFO, VP, etc.) appear in ≈10% of emails in both groups. Politeness markers such as “please”, “kindly”, or “thank you” appear in the majority of messages (≈59% vs 57%). Overall, adversarial obfuscation preserves the social-engineering tone—authority, mild threat, and politeness—while primarily targeting the literal keyword surface forms and Unicode representation.



--------------obligation/urgency language

To measure how adversarial obfuscation interacts with social-engineering pressure, I constructed a small lexicon of obligation and urgency phrases (e.g., must, need to, required, ASAP, immediately, by end of day, you are required). Among adversarially modified emails (N = 1,217), half of them (50.0%) contained at least one such obligation/urgency marker in their clean form. After poisoning, that proportion drops to 23.6%, and the mean count of obligation/urgency phrases per email falls from 0.74 → 0.29.



Focusing only on emails that originally used obligation/urgency phrasing (609 emails), 322 (52.9%) lose all detectable instances of these markers after poisoning. In other words, over half of the high-pressure BEC emails have their explicit urgency language erased at the string level by obfuscation, even though a human reader would still perceive the message as urgent and action-demanding.



-------------------Modeling results write-up draft

Adversarial obfuscation detection



I framed a binary classification task where the goal is to detect whether a BEC phishing email has been adversarially modified (is\_modified ∈ {0,1}). I first tried to predict this using only the clean email text (before poisoning), with TF–IDF features over words and over characters, and a class-balanced logistic regression classifier. Both variants achieved only modest performance on the modified class (≈0.28–0.29 F1), reflecting the fact that the social-engineering style of modified and unmodified BEC emails is very similar in their clean form.



I then trained a model on the actual text that would be seen in production—the poisoned email bodies, which may contain homoglyph substitutions and injected zero-width characters. Using character n-gram TF–IDF features (3–5-grams) and a class-balanced logistic regression, the model achieved 95.4% accuracy, with precision/recall of 0.96/0.97 for clean emails and 0.93/0.91 for adversarially modified emails. This indicates that adversarial obfuscation leaves a strong footprint at the character level (e.g., unusual Unicode patterns) that can be exploited by a relatively simple linear model.



Taken together with the earlier keyword-based experiments—where 81.3% of previously flagged emails evaded detection after poisoning—this suggests a layered defense strategy: keyword or semantic models for phishing intent, augmented by a dedicated character-level detector specifically trained to identify Unicode-based obfuscation.

