# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, VARCHAR, Integer

from api_python.app.common.pydantic_validator import str_to_list
from api_python.app.common.sql_alchemy import Base

import json
from typing import List


class RoomOrm(Base):
    __tablename__ = 'room_info'

    room_seq = Column(BigInteger, primary_key=True)
    stay_seq = Column(BigInteger, nullable=False)
    stay_name = Column(VARCHAR(255), nullable=True)
    stay_type = Column(BigInteger, nullable=False)
    room_name = Column(VARCHAR(255), nullable=True)
    room_type = Column(BigInteger, nullable=False)
    room_price = Column(BigInteger, nullable=False)
    room_available_count = Column(Integer, nullable=False)
    room_image_url_list = Column(VARCHAR(255), nullable=True)
    ott_service = Column(VARCHAR(255), nullable=True)
    toilet_option = Column(VARCHAR(255), nullable=True)
    room_option = Column(VARCHAR(255), nullable=True)
    special_room_option = Column(VARCHAR(255), nullable=True)
    min_people = Column(Integer, nullable=False)
    max_people = Column(Integer, nullable=False)
    additional_charge = Column(Integer, nullable=False)
    child_additional_charge = Column(Integer, nullable=False)


class RoomModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    room_seq: int
    stay_seq: int
    stay_name: str
    stay_type: int
    room_name: str
    room_type: int
    room_price: int
    room_available_count: int
    room_image_url_list: str
    ott_service: str
    toilet_option: str
    room_option: str
    special_room_option: str
    min_people: int
    max_people: int
    additional_charge: int
    child_additional_charge: int


class UserResponseRoomModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    room_seq: int
    stay_seq: int
    stay_name: str
    stay_type: int
    room_name: str
    room_type: int
    room_price: int
    room_available_count: int
    room_image_url_list: list[str]
    ott_service: list[str]
    toilet_option: list[str]
    room_option: list[str]
    special_room_option: list[str]
    min_people: int
    max_people: int
    additional_charge: int
    child_additional_charge: int


def convert_room_model_to_response(room_model: RoomModel) -> UserResponseRoomModel:
    return UserResponseRoomModel(
        room_seq=room_model.room_seq,
        stay_seq=room_model.stay_seq,
        stay_name=room_model.stay_name,
        stay_type=room_model.stay_type,
        room_name=room_model.room_name,
        room_type=room_model.room_type,
        room_price=room_model.room_price,
        room_available_count=room_model.room_available_count,
        room_image_url_list=str_to_list(room_model.room_image_url_list),
        ott_service=str_to_list(room_model.ott_service),
        toilet_option=str_to_list(room_model.toilet_option),
        room_option=str_to_list(room_model.room_option),
        special_room_option=str_to_list(room_model.special_room_option),
        min_people=room_model.min_people,
        max_people=room_model.max_people,
        additional_charge=room_model.additional_charge,
        child_additional_charge=room_model.child_additional_charge
    )


