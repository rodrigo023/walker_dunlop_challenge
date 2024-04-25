from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import models, schemas

def get_preferences(db: Session):
    return db.query(models.Preferences).all()

def get_preference(db: Session, user_id: int):
    return db.query(models.Preferences).filter(models.Preferences.user_id == user_id).first()

def create_preference(db: Session, preference: schemas.PreferenceCreate):
    db_preference = models.Preferences(user_id = preference.user_id, email_enabled = preference.email_enabled, sms_enabled = preference.sms_enabled)
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference

def update_preference(db: Session, user_preferences: schemas.Preference, new_preferences: schemas.PreferenceUpdate):
    stored_item = schemas.Preference(user_id=user_preferences.user_id, email_enabled=user_preferences.email_enabled, sms_enabled=user_preferences.sms_enabled)
    update_data = new_preferences.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=update_data)
    db.query(models.Preferences).filter(models.Preferences.user_id == user_preferences.user_id).update(jsonable_encoder(updated_item))
    db.commit()
    return updated_item

def delete_preference(db: Session, user_preferences: schemas.Preference):
    db.query(models.Preferences).filter(models.Preferences.user_id == user_preferences.user_id).delete()
    db.commit()
    return True
