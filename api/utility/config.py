import os


class GlobalConfig:
    # auth
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    TOKEN_URL = os.getenv("TOKEN_URL", "/api/v1/auth/token")
    LOGIN_MAX_RETRY = os.getenv("LOGIN_MAX_RETRY", 5)

    # db
    DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:password@localhost:3306/db")
