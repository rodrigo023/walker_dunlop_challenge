from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..dependencies import get_db
from .. import models, schemas
import boto3

router = APIRouter(dependencies=[Depends(get_db)])


@router.post("/notifications/", response_model=schemas.Notification)
def schedule_notifications(
    notification_payload: schemas.NotificationCreate, db: Session = Depends(get_db)
):
    # Getting data from mocked Users table. This could be a call to another DB or an API
    users_data = (
        db.query(models.Users)
        .filter(or_(models.Users.email != None, models.Users.phone != None))
        .all()
    )
    users_data_by_id = {data.user_id: data for data in users_data}
    users_preferences = (
        db.query(models.Preferences)
        .filter(models.Preferences.user_id.in_(users_data_by_id.keys()))
        .all()
    )
    notifications_list = [
        {
            "email": (
                users_data_by_id[preferences.user_id].email
                if preferences.email_enabled
                else None
            ),
            "phone": (
                users_data_by_id[preferences.user_id].phone
                if preferences.sms_enabled
                else None
            ),
        }
        for preferences in users_preferences
    ]
    sns = boto3.resource("sns", region_name="us-east-1")
    topic = sns.Topic("arn:aws:sns:us-east-1:421554845588:WDChallenge")
    response = {}
    response["message_ids"] = []
    for notification in notifications_list:
        messageAttributes = {
            k: {"StringValue": v, "DataType": "String"}
            for k, v in notification.items()
            if v
        }
        if len(messageAttributes) > 0:
            sns_response = topic.publish(
                Message=notification_payload.payload,
                MessageStructure="string",
                MessageAttributes=messageAttributes,
            )
            response["message_ids"].append(sns_response["MessageId"])
    return response
