from pydantic import BaseModel


class PreferenceBase(BaseModel):
    email_enabled: bool
    sms_enabled: bool


class PreferenceCreate(PreferenceBase):
    user_id: int


class PreferenceUpdate(BaseModel):
    email_enabled: bool | None = True
    sms_enabled: bool | None = True


class Preference(PreferenceBase):
    user_id: int

    class Config:
        from_attributes = True


class Notification(BaseModel):
    message_ids: list[str]

    class Config:
        from_attributes = True


class NotificationCreate(BaseModel):
    payload: str

    class Config:
        from_attributes = True
