
import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import (
    OrderInput,
    PredictionOutput,
    BatchPredictionInput,
    BatchPredictionOutput,
    ModelInfoOutput,
)
from src.pipeline import OlistInferencePipeline
from src.logger_config import setup_logger

logger = setup_logger(name=__name__)

app = FastAPI(
    title="Olist Delivery Prediction API",
    description="Predict whether Olist orders will be delivered late.",
    version="1.0.0",
)

try:
    pipeline = OlistInferencePipeline()
    logger.info("FastAPI application initialized successfully.")
except Exception:
    logger.exception("Failed to initialize inference pipeline.")
    raise


@app.get("/")
def home():
    return {
        "message": "Olist Delivery Prediction API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_version": pipeline.model_version,
    }


@app.get("/model-info", response_model=ModelInfoOutput)
def model_info():
    return ModelInfoOutput(
        model_name="Olist Delivery Prediction",
        model_version=pipeline.model_version,
    )


@app.post("/predict", response_model=PredictionOutput)
def predict(order: OrderInput):
    input_data = pd.DataFrame([order.model_dump()])
    result = pipeline.run(input_data)

    if result["status"] != "success":
        logger.warning("Prediction failed: %s", result.get("detail"))
        raise HTTPException(
            status_code=422,
            detail=result.get("detail", "Invalid input data"),
        )

    return PredictionOutput(
        prediction=result["prediction"],
        probability=result["probability"],
        model_version=result["model_version"],
    )


@app.post("/predict/batch", response_model=BatchPredictionOutput)
def predict_batch(batch: BatchPredictionInput):
    input_data = pd.DataFrame(
        [order.model_dump() for order in batch.orders]
    )

    result = pipeline.run_batch(input_data)

    if result["status"] != "success":
        logger.warning("Batch prediction failed: %s", result.get("detail"))
        raise HTTPException(
            status_code=422,
            detail=result.get("detail", "Invalid batch input"),
        )

    return BatchPredictionOutput(
        predictions=result["predictions"],
        total_orders=result["total_orders"],
    )
