# Training EDA findings

- Training rows: **67,529**; late share: **9.03%**. This imbalance requires average precision, recall, and F1—not accuracy alone.
- Monetary, distance, weight, and volume fields are right-skewed; robust linear preprocessing and imputation are appropriate.
- Highest late-rate customer states among states with at least 100 orders: **AL, MA, CE, SE, PI**.
- IDs and free-text city names have high cardinality and will not be direct model features.
- Missing geolocation/product attributes will be median-imputed; missing categories get an explicit token.
- Date features will use purchase-time components and promised lead time. Actual delivery, carrier, approval, and review fields are excluded as future leakage.
- Candidate model: class-weighted logistic regression. It is interpretable, handles sparse one-hot features, and provides a strong first model without needless complexity.
