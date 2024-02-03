# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, TIMESTAMP, CHAR

from api_python.app.common.sql_alchemy import Base


class WishOrm(Base):
    __tablename__ = 'wish'

    wish_seq = Column(BigInteger, primary_key=True)
    user_seq = Column(BigInteger, nullable=False)
    stay_seq = Column(BigInteger, nullable=False)
    state = Column(CHAR(1), nullable=False)
    wished_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP, nullable=False)


class WishModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    wish_seq: int
    user_seq: int
    stay_seq: int
    state: str
    wished_at: datetime
    modified_at: datetime
