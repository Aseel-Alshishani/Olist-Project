
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OrderInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_count: int = Field(..., ge=1, description="Number of items in the order")
    unique_product_count: int = Field(..., ge=1)
    unique_seller_count: int = Field(..., ge=1)

    total_item_value: float = Field(..., ge=0)
    mean_item_price: float = Field(..., ge=0)
    total_freight_value: float = Field(..., ge=0)
    mean_product_weight_g: float = Field(..., ge=0)
    mean_product_volume_cm3: float = Field(..., ge=0)
    mean_product_photos_qty: float = Field(..., ge=0)

    payment_count: int = Field(..., ge=1)
    payment_type_count: int = Field(..., ge=1)
    max_payment_installments: int = Field(..., ge=1)
    total_payment_value: float = Field(..., ge=0)

    seller_customer_distance_km: float = Field(..., ge=0)

    order_purchase_timestamp: datetime
    order_estimated_delivery_date: datetime

    customer_state: str = Field(..., min_length=1)
    primary_seller_state: str = Field(..., min_length=1)
    primary_product_category: str = Field(..., min_length=1)
    primary_payment_type: str = Field(..., min_length=1)


class PredictionOutput(BaseModel):
    prediction: Literal[0, 1] = Field(..., description="0 for On time, 1 for Late")
    probability: float = Field(..., ge=0, le=1, description="Probability of being late")
    model_version: str = Field(..., min_length=1)


class BatchPredictionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    orders: list[OrderInput] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of orders to predict (maximum 100 orders)"
    )


class BatchPredictionOutput(BaseModel):
    predictions: list[PredictionOutput]
    total_orders: int = Field(..., ge=0)


class ModelInfoOutput(BaseModel):
    model_name: str
    model_version: str
