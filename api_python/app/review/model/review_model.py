# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, VARCHAR, Integer, Index, BOOLEAN
from sqlalchemy.dialects.postgresql import TIMESTAMP

from api_python.app.common.sql_alchemy import Base

import json
from typing import List
from datetime import datetime


class ReviewOrm(Base):
    __tablename__ = 'review'

    review_seq = Column(BigInteger, primary_key=True)
    user_seq = Column(BigInteger, nullable=False)
    stay_seq = Column(BigInteger, nullable=False)
    room_seq = Column(BigInteger, nullable=False)
    review_title = Column(VARCHAR(255), nullable=True)
    review_content = Column(VARCHAR(255), nullable=True)
    review_score = Column(Integer, nullable=False)
    review_image_url_list = Column(VARCHAR(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP, nullable=False)
    exposed = Column(BOOLEAN, nullable=False)

    __table_args__ = (
        Index('user_seq_index', 'user_seq'),
        Index('stay_seq_index', 'stay_seq'),
        Index('room_seq_index', 'room_seq'),
    )


class ReviewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    review_seq: int
    user_seq: int
    room_seq: int
    room_name: str
    review_title: str
    review_content: str
    review_score: int
    review_image_url_list: str
    created_at: datetime
    modified_at: datetime


class UserResponseReviewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    review_seq: int
    user_seq: int
    room_seq: int
    room_name: str
    review_title: str
    review_content: str
    review_score: int
    review_image_url_list: List[str]
    created_at: datetime
    modified_at: datetime


def str_to_list(string: str) -> List[str]:
    try:
        return json.loads(string.replace("'", '"'))
    except json.JSONDecodeError:
        return string.split(', ')


def convert_review_model_to_response(review: ReviewModel) -> UserResponseReviewModel:
    return UserResponseReviewModel(
        review_seq=review.review_seq,
        user_seq=review.user_seq,
        room_seq=review.room_seq,
        room_name=review.room_name,
        review_title=review.review_title,
        review_content=review.review_content,
        review_score=review.review_score,
        review_image_url_list=str_to_list(review.review_image_url_list),
        created_at=review.created_at,
        modified_at=review.modified_at
    )
