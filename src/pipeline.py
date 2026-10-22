"""
Inference Pipeline Orchestrator (Production-Ready)
Includes latency tracking, request/response logging, and graceful error handling.
"""

from pathlib import Path
import time
import joblib
import pandas as pd
from src.features import build_features
from src.config_loader import ConfigLoader
from src.logger_config import setup_logger

# Initialize logger
logger = setup_logger(name=__name__)

class OlistInferencePipeline:
    def __init__(self):
        """
        Initializes the pipeline by loading pre-fitted artifacts and config settings.
        """
        logger.info("Initializing Olist Inference Pipeline...")
        self.config_loader = ConfigLoader()
        
        self.model_path = self.config_loader.get_path("model_path")
        self.preprocessor_path = self.config_loader.get_path("preprocessor_path")
        self.model_version = "logistic_regression_v1"
        
        if not self.model_path.exists() or not self.preprocessor_path.exists():
            logger.critical("Critical Error: Required model or preprocessor artifacts are missing!")
            raise FileNotFoundError("Artifacts not found.")
            
        self.model = joblib.load(self.model_path)
        self.preprocessor = joblib.load(self.preprocessor_path)
        logger.info(f"Artifacts loaded successfully. Model Version: {self.model_version}")

    def run(self, raw_data: pd.DataFrame) -> dict:
        """
        Executes the inference pipeline with full telemetry (latency, logging, error handling).
        Never crashes on bad inputs; catches exceptions and returns a structured error response.
        """
        start_time = time.time()
        logger.info(f"Received prediction request. Batch size: {len(raw_data)} record(s).")

        try:
            # 1. Feature Engineering
            processed_features = build_features(raw_data)
            
            # 2. Preprocessing (Transform only - no fitting)
            transformed_data = self.preprocessor.transform(processed_features)
            
            # 3. Model Inference
            prediction = int(self.model.predict(transformed_data)[0])
            probability = float(self.model.predict_proba(transformed_data)[0][1])
            
            # Calculate latency in milliseconds
            latency_ms = (time.time() - start_time) * 1000

            # Log prediction request telemetry as required by the task
            logger.info(
                f"Prediction Success | Model Version: {self.model_version} | "
                f"Prediction: {prediction} | Probability: {probability:.4f} | "
                f"Latency: {latency_ms:.2f}ms"
            )

            return {
                "prediction": prediction,
                "probability": probability,
                "model_version": self.model_version,
                "latency_ms": round(latency_ms, 2),
                "status": "success"
            }

        except Exception as e:
            # Handle bad inputs, missing columns, or malformed data gracefully without crashing
            latency_ms = (time.time() - start_time) * 1000
            logger.error(
                f"Prediction failed due to bad input or missing values: {str(e)} | "
                f"Latency: {latency_ms:.2f}ms", 
                exc_info=True
            )
            
            return {
                "prediction": None,
                "probability": None,
                "model_version": self.model_version,
                "latency_ms": round(latency_ms, 2),
                "status": "error",
                "detail": f"Invalid input data: {str(e)}"
            }