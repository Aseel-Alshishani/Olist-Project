# Model results

- Baseline: prior-probability dummy classifier.
- Selected model: class-weighted logistic regression (`C=0.01`).
- Selection metric: validation average precision (appropriate for minority late deliveries).
- Baseline validation AP: **0.053**.
- Model validation AP: **0.150**.
- Final test AP: **0.117**.
- Final test ROC AUC: **0.677**; recall: **0.848**; F1: **0.176**.
- Test was used once, after model and hyperparameter selection.
