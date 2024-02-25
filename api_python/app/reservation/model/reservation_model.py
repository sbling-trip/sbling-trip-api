# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, VARCHAR, Integer, Index, BOOLEAN
from sqlalchemy.dialects.postgresql import TIMESTAMP

from api_python.app.common.pydantic_validator import str_to_list
from api_python.app.common.sql_alchemy import Base

from typing import List
from datetime import datetime


class ReservationORM(Base):
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


