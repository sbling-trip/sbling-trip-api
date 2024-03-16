# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, VARCHAR, Integer, Index, BOOLEAN
from sqlalchemy.dialects.postgresql import TIMESTAMP

from api_python.app.common.pydantic_validator import str_to_list
from api_python.app.common.sql_alchemy import Base

from typing import List
from datetime import datetime


class ReservationOrm(Base):
    __tablename__ = 'reservations'

    reservation_seq = Column(BigInteger, primary_key=True)
    stay_seq = Column(BigInteger, nullable=False)
    room_seq = Column(BigInteger, nullable=False)
    user_seq = Column(BigInteger, nullable=False)
    check_in_date = Column(TIMESTAMP, nullable=False)
    check_out_date = Column(TIMESTAMP, nullable=False)
    adult_guest_count = Column(Integer, nullable=False)
    child_guest_count = Column(Integer, nullable=False)
    reservation_status = Column(VARCHAR(50), nullable=False)
    booking_date = Column(TIMESTAMP, nullable=False)
    payment_status = Column(VARCHAR(50), nullable=True)
    special_requests = Column(VARCHAR(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    payment_price = Column(BigInteger, nullable=False)


class UserResponseReservationInfoModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    reservation_seq: int
    stay_seq: int
    room_seq: int
    stay_name: str
    room_name: str
    check_in_date: datetime
    check_out_date: datetime
    adult_guest_count: int
    child_guest_count: int
    reservation_status: str
    booking_date: datetime
    payment_status: str | None
    special_requests: str | None
    payment_price: int


class ReservationRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)
    stay_seq: int
    room_seq: int
    check_in_date: datetime
    check_out_date: datetime
    adult_guest_count: int
    child_guest_count: int
    special_requests: str
    payment_price: int


class ReservationSeqModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)
    reservation_seq: int
