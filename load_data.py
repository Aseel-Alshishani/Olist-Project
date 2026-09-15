import logging
import os
import pandas as pd
from config import get_engine

# --- Logging Configuration ---
# 1. Define the log message format including timestamp, log level, and message
log_format = "%(asctime)s - %(levelname)s - %(message)s"

# 2. Configure logging to write logs both to a file and the console stream
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(
            "data_pipeline.log", encoding="utf-8"
        ),  # Save logs to a persistent file
        logging.StreamHandler(),  # Stream logs to the console
    ],
)

# 1. Initialize database connection engine from config module
engine = get_engine()

# 2. Define the relative path to the datasets folder
data_folder = "./Olist_Data"

# 3. Validate directory existence before starting the pipeline
if not os.path.exists(data_folder):
  logging.error(f"Target data directory does not exist: {data_folder}")
else:
  # Retrieve list of all CSV files in the directory
  csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

  logging.info("--- Starting Data Ingestion Pipeline ---")

  # 4. Iterate through each CSV file and ingest it into the MySQL database
  for file in csv_files:
    table_name = file.replace(".csv", "")
    file_path = os.path.join(data_folder, file)

    logging.info(f"Loading: {file} -> Target Table: `{table_name}`...")

    try:
      # Read CSV dataset into a Pandas DataFrame
      df = pd.read_csv(file_path)

      # Persist DataFrame into the MySQL database
      df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
      logging.info(
          f"Success: Table `{table_name}` loaded successfully ({len(df)}"
          " rows)."
      )

    except Exception as e:
      # Capture and log any exceptions encountered during ingestion
      logging.error(
          f"Failed to load table `{table_name}` from file `{file}`. Error: {e}"
      )

  logging.info("--- All datasets loaded successfully into MySQL! ---")