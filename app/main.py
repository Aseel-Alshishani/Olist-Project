
import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import OrderInput, PredictionOutput
from src.pipeline import OlistInferencePipeline
from src.logger_config import setup_logger

logger = setup_logger(name=__name__)

app = FastAPI(
    title="Olist Delivery Prediction API",
    description="Predict whether an Olist order will be delivered late.",
    version="1.0.0",
)

# Initialize the inference pipeline once when the application starts.
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


@app.post("/predict", response_model=PredictionOutput)
def predict(order: OrderInput):
    try:
        # Convert validated input into a DataFrame.
        input_data = pd.DataFrame([order.model_dump()])

        # Run the inference pipeline.
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

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error during prediction.")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction.",
        )
