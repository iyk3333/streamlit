from pydantic import BaseModel


class locationInfoModel(BaseModel):
    latitude: str
    longitude: str



