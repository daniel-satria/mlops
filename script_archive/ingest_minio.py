import os
import copy
import urllib3
import pandas as pd
from minio import Minio
from dotenv import load_dotenv

ENV_PATH = "../../.env"

load_dotenv(ENV_PATH)
urllib3.disable_warnings()

ACCESS_KEY = os.getenv("MINIO_ACCESSKEY")
SECRET_KEY = os.getenv("MINIO_SECRETKEY")
URL = os.getenv("MINIO_URL")
TLS = os.getenv("MINIO_TLS")

BUCKET_NAME = os.getenv("MINIO_BUCKETNAME")
INGEST_SOURCE_FILE = "car.data"
INGEST_DEST_FILE = "../../data/processed/car.csv"
INGEST_INDEX_LABEL = "index"
INGEST_SEP = "\t"

def main():
    client = Minio(
            endpoint = URL,
            access_key = ACCESS_KEY,
            secret_key = SECRET_KEY,
            secure = TLS,
            cert_check = (not TLS)
    )

    found = client.bucket_exists(BUCKET_NAME)
    if(not found):
        raise RuntimeError("Bucket not found!")

    try:
        res = client.get_object(
            bucket_name = BUCKET_NAME,
            object_name = INGEST_SOURCE_FILE
        )
        data = copy.deepcopy(res.data.decode())
        data = pd.DataFrame([row.split(',') for row in data.splitlines()])
        data.to_csv(
            INGEST_DEST_FILE,
            sep = INGEST_SEP,
            index_label= INGEST_INDEX_LABEL
        )

    except Exception as e:
        print(str(e))

    finally:
        res.close()
        res.release_conn()
        del res
        print("Ingesting data from MinIO success.")

if __name__ == "__main__":
    main()