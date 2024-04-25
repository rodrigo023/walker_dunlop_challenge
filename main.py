from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/preferences/", response_model=list[schemas.Preference])
def get_preferences(db: Session = Depends(get_db)):
  preferences = crud.get_preferences(db)
  return preferences

@app.post("/preferences/", response_model=schemas.Preference, status_code=status.HTTP_201_CREATED)
def create_preference(preference: schemas.PreferenceCreate, db: Session = Depends(get_db)):
    user_preferences = crud.get_preference(db, user_id=preference.user_id)
    if user_preferences:
        raise HTTPException(status_code=400, detail="Preference already registered")
    return crud.create_preference(db=db, preference=preference)

@app.patch("/preferences/{user_id}", response_model=schemas.Preference)
def update_preference(user_id: int, preferences: schemas.PreferenceUpdate, db: Session = Depends(get_db)):
    user_preferences = crud.get_preference(db, user_id=user_id)
    if not user_preferences:
        raise HTTPException(status_code=400, detail="Preference not found for specified user id")
    return crud.update_preference(db=db, user_preferences=user_preferences, new_preferences=preferences)

@app.delete("/preferences/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_preference(user_id: int, db: Session = Depends(get_db)):
    user_preferences = crud.get_preference(db, user_id=user_id)
    if not user_preferences:
        raise HTTPException(status_code=400, detail="Preference not found for specified user id")
    return crud.delete_preference(db=db, user_preferences=user_preferences)
