import os
import requests
import pandas as pd
from google.cloud import storage

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/minh/Documents/Docs/data_engineer/homework_2026/3_data_warehouse/zoomcamp-kestra-2026-c1b656de45db.json"
BUCKET = os.environ.get("GCP_GCS_BUCKET", "minh-hd-zoomcamp-bucket")

init_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


def web_to_gcs(year, month, service):
    for i in range (month):

        m = '0' + str(i + 1)
        m = m[-2:]

        file_name = f"{service}_tripdata_{year}-{m}.parquet"

        request_url = f"{init_url}{service}_tripdata_{year}-{m}.parquet"

        response = requests.get(request_url)
        response.raise_for_status()

        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

        print(f"Local: {file_name}")

        upload_blob(BUCKET, file_name, f"{service}/{file_name}")


web_to_gcs('2024', 6, 'yellow')