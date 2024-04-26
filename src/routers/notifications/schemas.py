from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class Notification(BaseModel):
    model_config = SettingsConfigDict(from_attributes=True)
    message_ids: list[str]


class NotificationCreate(BaseModel):
    model_config = SettingsConfigDict(from_attributes=True)
    payload: str
