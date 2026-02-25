"""@bruin

# TODO: Set the asset name (recommended pattern: schema.asset_name).
# - Convention in this module: use an `ingestion.` schema for raw ingestion tables.
name: ingestion.trips

# TODO: Set the asset type.
# Docs: https://getbruin.com/docs/bruin/assets/python
type: python

# TODO: Pick a Python image version (Bruin runs Python in isolated environments).
# Example: python:3.11
image: python:3.11

# TODO: Set the connection.
connection: duckdb-default

# TODO: Choose materialization (optional, but recommended).
# Bruin feature: Python materialization lets you return a DataFrame (or list[dict]) and Bruin loads it into your destination.
# This is usually the easiest way to build ingestion assets in Bruin.
# Alternative (advanced): you can skip Bruin Python materialization and write a "plain" Python asset that manually writes
# into DuckDB (or another destination) using your own client library and SQL. In that case:
# - you typically omit the `materialization:` block
# - you do NOT need a `materialize()` function; you just run Python code
# Docs: https://getbruin.com/docs/bruin/assets/python#materialization
materialization:
  # TODO: choose `table` or `view` (ingestion generally should be a table)
  type: table
  # TODO: pick a strategy.
  # suggested strategy: append
  strategy: append

# TODO: Define output columns (names + types) for metadata, lineage, and quality checks.
# Tip: mark stable identifiers as `primary_key: true` if you plan to use `merge` later.
# Docs: https://getbruin.com/docs/bruin/assets/columns
# columns:
#   - name: TODO_col1
#     type: TODO_type
#     description: TODO

@bruin"""

# TODO: Add imports needed for your ingestion (e.g., pandas, requests).
# - Put dependencies in the nearest `requirements.txt` (this template has one at the pipeline root).
# Docs: https://getbruin.com/docs/bruin/assets/python


# TODO: Only implement `materialize()` if you are using Bruin Python materialization.
# If you choose the manual-write approach (no `materialization:` block), remove this function and implement ingestion
# as a standard Python script instead.

import os, json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def materialize():
    """
    TODO: Implement ingestion using Bruin runtime context.

    Required Bruin concepts to use here:
    - Built-in date window variables:
      - BRUIN_START_DATE / BRUIN_END_DATE (YYYY-MM-DD)
      - BRUIN_START_DATETIME / BRUIN_END_DATETIME (ISO datetime)
      Docs: https://getbruin.com/docs/bruin/assets/python#environment-variables
    - Pipeline variables:
      - Read JSON from BRUIN_VARS, e.g. `taxi_types`
      Docs: https://getbruin.com/docs/bruin/getting-started/pipeline-variables

    Design TODOs (keep logic minimal, focus on architecture):
    - Use start/end dates + `taxi_types` to generate a list of source endpoints for the run window.
    - Fetch data for each endpoint, parse into DataFrames, and concatenate.
    - Add a column like `extracted_at` for lineage/debugging (timestamp of extraction).
    - Prefer append-only in ingestion; handle duplicates in staging.
    """
    START_DATE = os.environ["BRUIN_START_DATE"]

    END_DATE = os.environ["BRUIN_END_DATE"]

    taxi_types = json.loads(os.environ["BRUIN_VARS"])['taxi_types']

    date_start = datetime.strptime(START_DATE, "%Y-%m-%d")

    date_end = datetime.strptime(END_DATE, "%Y-%m-%d")

    all_dfs = []

    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"

    current_date = date_start

    while current_date <= date_end:
        year_month = current_date.strftime("%Y-%m")

        for taxi in taxi_types:

          url = f"{base_url}/{taxi}_tripdata_{year_month}.parquet"

          try:
             df = pd.read_parquet(url)

             df['extracted_at'] = datetime.now()

             all_dfs.append(df)
          except Exception as e:
             print(f"Error: {e}")
        
        current_date += relativedelta(months = 1)

    if not all_dfs:
       
       return pd.DataFrame()
    
    final_dataframe = pd.concat(all_dfs, ignore_index=True)

    return final_dataframe


"""bruin run \
    --start-date 2025-02-02 \
    --end-date 2025-02-02 \
    --environment default \
    "/home/minh/Documents/Docs/data_engineer/05-data-platforms/bruin/zoomcamp/pipeline/assets/ingestion/trips.py"
"""