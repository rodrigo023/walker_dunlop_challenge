from .config import SnsConfig
from .database import SessionLocal
import boto3


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sns_topic():
    sns = boto3.resource("sns", region_name=SnsConfig.region)
    return sns.Topic(SnsConfig.topic_arn)
