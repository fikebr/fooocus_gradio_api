import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


class AppConfig(BaseModel):
    """Application configuration loaded from environment."""

    fooocus_url: str = Field(default=os.getenv("FOOOCUS_URL", "http://127.0.0.1:7865/"))
    logfile: str = Field(default=os.getenv("LOG_FILE", "logs/app.log"))
    request_timeout_seconds: int = Field(default=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "300")))


config = AppConfig()


