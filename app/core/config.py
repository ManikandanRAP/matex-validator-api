from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This is a default, insecure token. 
    # In a production environment, this should be set via an environment variable.
    API_TOKEN: str = "secret-token-for-dev"

    # Pydantic V2 uses model_config
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
