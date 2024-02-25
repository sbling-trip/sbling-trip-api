# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances
from datetime import time
from typing import List

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, Boolean, TEXT, TIME, INTEGER, NUMERIC, VARCHAR

from api_python.app.common.pydantic_validator import str_to_list
from api_python.app.common.sql_alchemy import Base


class StayInfoOrm(Base):
    __tablename__ = 'stay_info'

    stay_seq = Column(BigInteger, primary_key=True)
    stay_name = Column(VARCHAR(255), nullable=True)
    manager = Column(VARCHAR(255), nullable=True)
    contact_number = Column(VARCHAR(50), nullable=True)
    address = Column(TEXT, nullable=True)
    check_in_time = Column(TIME, nullable=True)
    check_in_additional_info = Column(TEXT, nullable=True)
    check_out_time = Column(TIME, nullable=True)
    check_out_additional_info = Column(TEXT, nullable=True)
    description = Column(TEXT, nullable=True)
    stay_scale = Column(TEXT, nullable=True)
    capacity = Column(INTEGER, nullable=True)
    room_count = Column(INTEGER, nullable=True)
    room_type = Column(VARCHAR(255), nullable=True)
    refund_policy = Column(TEXT, nullable=True)
    homepage_url = Column(VARCHAR(255), nullable=True)
    reservation_info = Column(VARCHAR(255), nullable=True)
    pickup_available = Column(Boolean, nullable=True)
    pickup_additional_info = Column(VARCHAR(255), nullable=True)
    parking_available = Column(Boolean, nullable=True)
    parking_count = Column(INTEGER, nullable=True)
    cook_available = Column(Boolean, nullable=True)
    korea_tourism_certified = Column(Boolean, nullable=True)
    seminar_facilities = Column(Boolean, nullable=True)
    sports_facilities = Column(Boolean, nullable=True)
    sauna_facilities = Column(Boolean, nullable=True)
    beauty_facilities = Column(Boolean, nullable=True)
    karaoke_facilities = Column(Boolean, nullable=True)
    barbecue_facilities = Column(Boolean, nullable=True)
    campfire_facilities = Column(Boolean, nullable=True)
    fitness_center_facilities = Column(Boolean, nullable=True)
    internet_cafe_facilities = Column(Boolean, nullable=True)
    public_shower_facilities = Column(Boolean, nullable=True)
    bike_rental = Column(Boolean, nullable=True)
    latitude = Column(NUMERIC(10, 7), nullable=True)
    longitude = Column(NUMERIC(10, 7), nullable=True)
    postal_code = Column(VARCHAR(20), nullable=True)
    stay_detail = Column(TEXT, nullable=True)
    facilities_detail = Column(TEXT, nullable=True)
    food_beverage_area = Column(TEXT, nullable=True)


class StayInfoModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    stay_seq: int
    stay_name: str | None = None
    manager: str | None = None
    contact_number: str | None = None
    address: str | None = None
    check_in_time: time | None = None
    check_in_additional_info: str | None = None
    check_out_time: time | None = None
    check_out_additional_info: str | None = None
    description: str | None = None
    stay_scale: str | None = None
    capacity: int | None = None
    room_count: int | None = None
    room_type: str | None = None
    refund_policy: str | None = None
    homepage_url: str | None = None
    reservation_info: str | None = None
    pickup_available: bool | None = None
    pickup_additional_info: str | None = None
    parking_available: bool | None = None
    parking_count: int | None = None
    cook_available: bool | None = None
    korea_tourism_certified: bool | None = None
    seminar_facilities: bool | None = None
    sports_facilities: bool | None = None
    sauna_facilities: bool | None = None
    beauty_facilities: bool | None = None
    karaoke_facilities: bool | None = None
    barbecue_facilities: bool | None = None
    campfire_facilities: bool | None = None
    fitness_center_facilities: bool | None = None
    internet_cafe_facilities: bool | None = None
    public_shower_facilities: bool | None = None
    bike_rental: bool | None = None
    latitude: float | None = None
    longitude: float | None = None
    postal_code: str | None = None
    stay_detail: str | None = None
    facilities_detail: str | None = None
    food_beverage_area: str | None = None


class StayInfoWishModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    stay_seq: int
    stay_name: str | None = None
    manager: str | None = None
    contact_number: str | None = None
    address: str | None = None
    check_in_time: str | None = None
    check_out_time: str | None = None
    description: str | None = None
    refund_policy: str | None = None
    homepage_url: str | None = None
    reservation_info: str | None = None
    parking_available: bool | None = None
    latitude: float | None = None
    longitude: float | None = None
    facilities_detail: str | None = None
    food_beverage_area: str | None = None
    wish_state: bool = False


class StayInfoWishReviewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    stay_seq: int
    stay_name: str | None = None
    manager: str | None = None
    contact_number: str | None = None
    address: str | None = None
    check_in_time: str | None = None
    check_out_time: str | None = None
    description: str | None = None
    refund_policy: str | None = None
    homepage_url: str | None = None
    reservation_info: str | None = None
    parking_available: bool | None = None
    latitude: float | None = None
    longitude: float | None = None
    facilities_detail: str | None = None
    food_beverage_area: str | None = None
    wish_state: bool = False
    review_count: int = 0
    review_score_average: float = 0.0
    room_image_url_list: str | None = None


class UserResponseStayInfoModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    stay_seq: int
    stay_name: str | None = None
    manager: str | None = None
    contact_number: str | None = None
    address: str | None = None
    check_in_time: str | None = None
    check_out_time: str | None = None
    description: str | None = None
    refund_policy: str | None = None
    homepage_url: str | None = None
    reservation_info: str | None = None
    parking_available: bool | None = None
    latitude: float | None = None
    longitude: float | None = None
    facilities_detail: str | None = None
    food_beverage_area: str | None = None
    wish_state: bool = False
    review_count: int = 0
    review_score_average: float = 0.0
    room_image_url_list: List[str] | None = None


def convert_stay_info_model_to_response(stay: StayInfoWishReviewModel) -> UserResponseStayInfoModel:
    return UserResponseStayInfoModel(
        stay_seq=stay.stay_seq,
        stay_name=stay.stay_name,
        manager=stay.manager,
        contact_number=stay.contact_number,
        address=stay.address,
        check_in_time=stay.check_in_time,
        check_out_time=stay.check_out_time,
        description=stay.description,
        refund_policy=stay.refund_policy,
        homepage_url=stay.homepage_url,
        reservation_info=stay.reservation_info,
        parking_available=stay.parking_available,
        latitude=stay.latitude,
        longitude=stay.longitude,
        facilities_detail=stay.facilities_detail,
        food_beverage_area=stay.food_beverage_area,
        wish_state=stay.wish_state,
        review_count=stay.review_count,
        review_score_average=stay.review_score_average,
        room_image_url_list=str_to_list(stay.room_image_url_list)
    )
