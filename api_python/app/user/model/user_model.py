# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, VARCHAR, TIMESTAMP, Index

from api_python.app.common.sql_alchemy import Base


class UserModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel, populate_by_name=True
    )

    user_seq: int
    user_name: str
    user_status: int
    gender: str
    birth_at: datetime
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None
    image: str | None
    service_agree: bool
    location_agree: bool
    marketing_agree: bool


class UserUpdateModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel, populate_by_name=True
    )

    user_name: str | None = None
    location_agree: bool | None = None
    marketing_agree: bool | None = None
