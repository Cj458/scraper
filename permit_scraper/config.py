import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)



class Config(BaseSettings):

    API_URL: str = os.environ.get("API_URL", "https://data.boston.gov/api/3/action/datastore_search?resource_id=6ddcd912-32a0-43df-9908-63574f8c7e77&limit=100")


@lru_cache(1)
def get_config() -> Config:
    return Config()