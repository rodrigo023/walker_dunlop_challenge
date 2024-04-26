from sqlalchemy import Column, or_
from ... import models
from sqlalchemy.orm import Session


def publish_notifications_to_sns(db: Session, notification_payload: str, sns_topic):
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
    return _publish_to_sns(notifications_list, notification_payload, sns_topic)


def _publish_to_sns(
    notifications: list[dict[str, Column[str]]], payload: str, sns_topic
):
    response = dict()
    response["message_ids"] = list()
    for notification in notifications:
        if notification["email"] or notification["phone"]:
            messageAttributes = {
                k: {"StringValue": v, "DataType": "String"}
                for k, v in notification.items()
                if v
            }
            sns_response = sns_topic.publish(
                Message=payload,
                MessageStructure="string",
                MessageAttributes=messageAttributes,
            )
            response["message_ids"].append(sns_response["MessageId"])
    return response
