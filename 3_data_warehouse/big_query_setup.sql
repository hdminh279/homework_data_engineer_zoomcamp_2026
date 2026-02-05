
# Create an external table using the Yellow Taxi Trip Records.
CREATE OR REPLACE EXTERNAL TABLE `ny_taxi_hw_week3.external_yellow_tripdata`
OPTIONS(
  format = 'PARQUET',
  uris = ['gs://minh-hd-zoomcamp-bucket/yellow/yellow_tripdata_2024-*.parquet']
);

# Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).

CREATE OR REPLACE TABLE `ny_taxi_hw_week3.yellow_tripdata_non_partitoned` AS
SELECT * FROM `ny_taxi_hw_week3.external_yellow_tripdata`;