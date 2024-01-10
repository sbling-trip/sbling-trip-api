# https://docs.pydantic.dev/2.5/concepts/models/#arbitrary-class-instances
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, BigInteger, VARCHAR, TIMESTAMP, Index

from api_python.app.common.sql_alchemy import Base


class UserOrm(Base):
    __tablename__ = 'users'

    user_seq = Column(BigInteger, primary_key=True)
    email = Column(VARCHAR(255), nullable=False)
    external_id = Column(VARCHAR(255), nullable=False)
    first_name = Column(VARCHAR(254), nullable=True)
    last_name = Column(VARCHAR(254), nullable=True)
    oauth_provider = Column(VARCHAR(255), nullable=False)
    logo_url = Column(VARCHAR(255), nullable=True)
    expired_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    logged_in_at = Column(TIMESTAMP, nullable=False)

    __table_args__ = (
        Index("external_id_index", "external_id"),
    )


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

    user_seq: int
    email: str
    external_id: str
    first_name: str | None = None
    last_name: str | None = None
    oauth_provider: str
    logo_url: str | None = None
    expired_at: datetime
    created_at: datetime
    logged_in_at: datetime

