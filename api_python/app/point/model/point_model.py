# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from api_python.app.common.sql_alchemy import Base


class PointModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel, populate_by_name=True
    )

    point_seq: int
    point: int
    created_at: datetime
    updated_at: datetime | None
    user_seq: int
