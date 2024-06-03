import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
ENV_PATH = "../../.env"

load_dotenv(ENV_PATH)

USR = os.getenv("POSTGRES_USER")
USR_PWD = os.getenv("POSTGRES_PASSWORD")
HST = os.getenv("POSTGRES_HOST")
PRT = os.getenv("POSTGRES_PORT")
DB = os.getenv("POSTGRES_DB")

INGEST_DEST_FILE = "../../data/processed/car_postgres.csv"
INGEST_INDEX_LABEL = "index"
INGEST_SEP = "\t"

URL = f'postgresql://{USR}:{USR_PWD}@{HST}:{PRT}/{DB}'
def main():
    engine = create_engine(URL)

    query = 'SELECT * FROM car'
    data = pd.read_sql_query(query, engine)

    data.to_csv(
        INGEST_DEST_FILE,
        sep = INGEST_SEP,
        index_label= INGEST_INDEX_LABEL
    )

    print("Ingesting data from PostgreSQL success.")

if __name__ == "__main__":
    main()