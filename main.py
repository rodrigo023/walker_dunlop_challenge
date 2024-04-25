from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

import models, schemas, crud
import boto3
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

@app.post("/notifications/", response_model=schemas.Notification)
def schedule_notifications(notification_payload: schemas.NotificationCreate, db: Session = Depends(get_db)):
    # Getting data from mocked Users table. This could be a call to another DB or an API
    users_data = db.query(models.Users).filter(or_(models.Users.email != None, models.Users.phone != None)).all()
    users_data_by_id = {data.user_id: data for data in users_data}
    users_preferences = db.query(models.Preferences).filter(models.Preferences.user_id.in_(users_data_by_id.keys())).all()
    notifications_list = [{"email": users_data_by_id[preferences.user_id].email if preferences.email_enabled else None,
                           "phone": users_data_by_id[preferences.user_id].phone if preferences.sms_enabled else None} 
                           for preferences in users_preferences]
    sns = boto3.resource("sns", region_name="us-east-1")
    topic = sns.Topic("arn:aws:sns:us-east-1:421554845588:WDChallenge")
    response = {}
    response['message_ids'] = []
    for notification in notifications_list:
        messageAttributes = {k: {"StringValue": v, "DataType": "String"} for k, v in notification.items() if v}
        if len(messageAttributes) > 0:
            sns_response = topic.publish(
                Message = notification_payload.payload,
                MessageStructure = 'string',
                MessageAttributes = messageAttributes
                )
            response['message_ids'].append(sns_response["MessageId"])
    return response
