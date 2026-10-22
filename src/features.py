"""
Feature Engineering Module
Contains transformation logic and feature extraction matching Notebook 5 exactly.
"""

import pandas as pd
from src.logger_config import setup_logger

logger = setup_logger(name=__name__)

NUMERIC_FEATURES = [
    "item_count", "unique_product_count", "unique_seller_count", "total_item_value",
    "mean_item_price", "total_freight_value", "mean_product_weight_g",
    "mean_product_volume_cm3", "mean_product_photos_qty", "payment_count",
    "payment_type_count", "max_payment_installments", "total_payment_value",
    "seller_customer_distance_km", "estimated_lead_days", "purchase_month",
    "purchase_weekday", "purchase_hour",
]

CATEGORICAL_FEATURES = [
    "customer_state", "primary_seller_state", "primary_product_category",
    "primary_payment_type",
]

def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts time-based features and calculates lead days.
    Guarantees exact parity with the training pipeline features.
    """
    logger.info("Starting feature engineering and timestamp parsing...")
    purchase = pd.to_datetime(frame["order_purchase_timestamp"], errors="coerce")
    estimate = pd.to_datetime(frame["order_estimated_delivery_date"], errors="coerce")
    
    features = frame.copy()
    features["estimated_lead_days"] = (estimate - purchase).dt.total_seconds() / 86400
    features["purchase_month"] = purchase.dt.month
    features["purchase_weekday"] = purchase.dt.weekday
    features["purchase_hour"] = purchase.dt.hour
    
    logger.info("Feature engineering completed successfully.")
    return features[NUMERIC_FEATURES + CATEGORICAL_FEATURES]