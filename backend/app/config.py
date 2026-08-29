import os
from pydantic_settings import BaseSettings

class Settings:
    PROJECT_NAME: str = "SIH Thermal Anomaly Attribution API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
settings = Settings()
