from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class PreferenceBase(BaseModel):
    email_enabled: bool
    sms_enabled: bool


class PreferenceCreate(PreferenceBase):
    user_id: int


class PreferenceUpdate(BaseModel):
    email_enabled: bool | None = True
    sms_enabled: bool | None = True


class Preference(PreferenceBase):
    model_config = SettingsConfigDict(from_attributes=True)
    user_id: int
