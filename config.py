from pydantic import BaseSettings

# TODO move to env
class Settings(BaseSettings):
    user_session_id: str = 'user_session_id'
    google_maps_api_key: str = 'AIzaSyA4H4fchv-OtoenPkJepoMhx3cSzLK2-TM'
    ipinfo_access_token = 'c32a74d8cb473b'


settings = Settings()
