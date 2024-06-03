import os
import urllib3
from minio import Minio
from dotenv import load_dotenv

ENV_PATH = "../../.env"

load_dotenv(ENV_PATH)
urllib3.disable_warnings()

ACCESS_KEY = os.getenv("MINIO_ACCESSKEY")
SECRET_KEY = os.getenv("MINIO_SECRETKEY")
URL = os.getenv("MINIO_URL")
TLS = os.getenv("MINIO_TLS")
BUCKETNAME = os.getenv("MINIO_BUCKETNAME")
SOURCE_FILE = os.getenv("SOURCE_FILE")
INGEST_DEST_FILE = os.getenv("DEST_FILE")

def main():
	client = Minio(
		endpoint = URL,
		access_key = ACCESS_KEY,
		secret_key = SECRET_KEY,
		secure = TLS,
		cert_check = (not TLS)
	)

	found = client.bucket_exists(BUCKETNAME)
	if(not found):
		print("Bucket not found!")
		return
	
	try:
		client.fput_object(
			BUCKETNAME,
			INGEST_DEST_FILE,
			SOURCE_FILE
		)
		print("Successfully uploaded.")
	except Exception as e:
		print(str(e))

if __name__=="__main__":
	main()