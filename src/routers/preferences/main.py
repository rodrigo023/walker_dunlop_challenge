from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ...dependencies import get_db
from .controller import (
    get_users_preferences,
    create_user_preferences,
    update_user_preferences,
    delete_user_preferences,
)
from .schemas import Preference, PreferenceCreate, PreferenceUpdate

router = APIRouter()


@router.get("/preferences/", response_model=list[Preference])
def get_preferences(db: Session = Depends(get_db)):
    return get_users_preferences(db)


@router.post(
    "/preferences/",
    response_model=Preference,
    status_code=status.HTTP_201_CREATED,
)
def create_preference(preferences: PreferenceCreate, db: Session = Depends(get_db)):
    return create_user_preferences(db, preferences)


@router.patch("/preferences/{user_id}", response_model=Preference)
def update_preference(
    user_id: int, preferences: PreferenceUpdate, db: Session = Depends(get_db)
):
    return update_user_preferences(db, user_id, preferences)


@router.delete("/preferences/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_preference(user_id: int, db: Session = Depends(get_db)):
    return delete_user_preferences(db, user_id)
