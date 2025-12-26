import os

class Settings:
    APP_NAME = os.getenv("APP_NAME", "DeployForge")
    APP_ENV = os.getenv("APP_ENV", "dev")
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")

settings = Settings()
