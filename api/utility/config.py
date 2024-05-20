import os

DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:password@localhost:3306/db")
MAX_RETRY = os.getenv("MAX_RETRY", "5")
