from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schemas

from .controller import publish_notifications_to_sns
from ...dependencies import get_db, get_sns_topic

router = APIRouter()


@router.post("/notifications/", response_model=schemas.Notification)
def schedule_notifications(
    notification_data: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    sns_topic=Depends(get_sns_topic),
):
    return publish_notifications_to_sns(db, notification_data.payload, sns_topic)
