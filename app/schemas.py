from pydantic import BaseModel, Field

class OrderInput(BaseModel):
    item_count: int = Field(..., description="Number of items in the order")
    unique_product_count: int
    unique_seller_count: int
    total_item_value: float
    mean_item_price: float
    total_freight_value: float
    mean_product_weight_g: float
    mean_product_volume_cm3: float
    mean_product_photos_qty: float
    payment_count: int
    payment_type_count: int
    max_payment_installments: int
    total_payment_value: float
    seller_customer_distance_km: float
    estimated_lead_days: float
    purchase_month: int
    purchase_weekday: int
    purchase_hour: int
    customer_state: str
    primary_seller_state: str
    primary_product_category: str
    primary_payment_type: str

class PredictionOutput(BaseModel):
    prediction: int = Field(..., description="0 for On time, 1 for Late")
    probability: float = Field(..., description="Probability of being late")
    model_version: str = Field(..., description="Version or name of the deployed model")