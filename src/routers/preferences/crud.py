from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ...models import Preferences
from .schemas import Preference, PreferenceCreate, PreferenceUpdate


def get_preferences(db: Session):
    return db.query(Preferences).all()


def get_preference(db: Session, user_id: int):
    return db.query(Preferences).filter(Preferences.user_id == user_id).first()


def create_preference(db: Session, preference: PreferenceCreate):
    db_preference = Preferences(
        user_id=preference.user_id,
        email_enabled=preference.email_enabled,
        sms_enabled=preference.sms_enabled,
    )
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference


def update_preference(
    db: Session,
    user_preferences: Preference,
    new_preferences: PreferenceUpdate,
):
    stored_item = Preference(
        user_id=user_preferences.user_id,
        email_enabled=user_preferences.email_enabled,
        sms_enabled=user_preferences.sms_enabled,
    )
    update_data = new_preferences.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=update_data)
    db.query(Preferences).filter(
        Preferences.user_id == user_preferences.user_id
    ).update(jsonable_encoder(updated_item))
    db.commit()
    return updated_item


def delete_preference(db: Session, user_preferences: Preference):
    db.query(Preferences).filter(
        Preferences.user_id == user_preferences.user_id
    ).delete()
    db.commit()
    return True
