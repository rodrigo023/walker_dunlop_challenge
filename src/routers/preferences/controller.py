from fastapi import HTTPException

from .schemas import PreferenceCreate, PreferenceUpdate
from . import crud
from sqlalchemy.orm import Session


def get_users_preferences(db: Session):
    preferences = crud.get_preferences(db)
    return preferences


def create_user_preferences(db: Session, preferences: PreferenceCreate):
    user_preferences = crud.get_preference(db, user_id=preferences.user_id)
    if user_preferences:
        raise HTTPException(status_code=400, detail="Preference already registered")
    return crud.create_preference(db=db, preference=preferences)


def update_user_preferences(db: Session, user_id: int, preferences: PreferenceUpdate):
    user_preferences = crud.get_preference(db, user_id=user_id)
    if not user_preferences:
        raise HTTPException(
            status_code=400, detail="Preference not found for specified user id"
        )
    return crud.update_preference(
        db=db, user_preferences=user_preferences, new_preferences=preferences
    )


def delete_user_preferences(db: Session, user_id: int):
    user_preferences = crud.get_preference(db, user_id=user_id)
    if not user_preferences:
        raise HTTPException(
            status_code=400, detail="Preference not found for specified user id"
        )
    return crud.delete_preference(db=db, user_preferences=user_preferences)
