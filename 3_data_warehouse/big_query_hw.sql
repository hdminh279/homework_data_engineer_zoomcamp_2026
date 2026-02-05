##Question 1
SELECT COUNT(1) FROM `zoomcamp-kestra-2026.ny_taxi_hw_week3.external_yellow_tripdata`;

##Question 2
#Query of external table
SELECT COUNT(DISTINCT PULocationID) FROM `zoomcamp-kestra-2026.ny_taxi_hw_week3.external_yellow_tripdata`;

#Query of table
SELECT COUNT(DISTINCT PULocationID) FROM `zoomcamp-kestra-2026.ny_taxi_hw_week3.yellow_tripdata_non_partitoned`;

##Question 3
#Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery
SELECT PULocationID FROM `ny_taxi_hw_week3.yellow_tripdata_non_partitoned`;

#Write a query to retrieve the PULocationID and DOLocationID on the same table
SELECT PULocationID, DOLocationID FROM `ny_taxi_hw_week3.yellow_tripdata_non_partitoned`;

##Question 4
SELECT COUNT(1) FROM `ny_taxi_hw_week3.yellow_tripdata_non_partitoned` 
WHERE fare_amount = 0;

##Question 5
CREATE OR REPLACE TABLE `ny_taxi_hw_week3.external_yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM `ny_taxi_hw_week3.external_yellow_tripdata`;

##Question 6
# Partitioned_clustered
SELECT COUNT(DISTINCT VendorID) FROM `ny_taxi_hw_week3.external_yellow_tripdata_partitioned_clustered` 
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';
#Non_partitioned_clustered
SELECT COUNT(DISTINCT VendorID) FROM `ny_taxi_hw_week3.yellow_tripdata_non_partitoned`
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';