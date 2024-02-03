from datetime import datetime
from typing import Optional, Tuple

from api_python.app.common.client.postgres.postgres_client import postgres_client
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, case, and_, ChunkedIteratorResult

from api_python.app.stay.model.stay_model import StayInfoOrm, StayInfoModel
from api_python.app.stay.repository.stay_repository import stay_orm_to_wish_pydantic_model, stay_orm_to_pydantic_model
from api_python.app.wish.model.wish_model import WishOrm


def stay_orm_to_pydantic_model_wish(result: ChunkedIteratorResult[Tuple[StayInfoOrm, Optional[str]]]) -> list[StayInfoModel]:
    return [
        StayInfoModel(
            stay_seq=orm.stay_seq,
            stay_name=orm.stay_name,
            manager=orm.manager,
            contact_number=orm.contact_number,
            address=orm.address,
            wish=wish if wish is not None else 'N'
        )
        for orm, wish in result.all()
    ]

async def insert_by_user_seq_stay_seq(user_seq: int, stay_seq: int) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                # 만약 이미 찜한 숙소라면 N으로 변경
                stmt = insert(WishOrm).values(
                    user_seq=user_seq,
                    stay_seq=stay_seq,
                    state='Y',
                    wished_at=datetime.utcnow(),
                    modified_at=datetime.utcnow()
                ).on_conflict_do_update(
                    index_elements=['user_seq', 'stay_seq'],
                    set_={'state': 'Y', 'modified_at': datetime.utcnow()}
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            print(e)
            return False


async def update_by_user_seq_stay_seq(user_seq: int, stay_seq) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                # 만약 이미 찜한 숙소라면 N으로 변경
                stmt = insert(WishOrm).values(
                    user_seq=user_seq,
                    stay_seq=stay_seq,
                    state='N',
                    wished_at=datetime.utcnow(),
                    modified_at=datetime.utcnow()
                ).on_conflict_do_update(
                    index_elements=['user_seq', 'stay_seq'],
                    set_={'state': 'N', 'modified_at': datetime.utcnow()}
                )
                await session.execute(stmt)
        except Exception as e:
            print(e)
            return False


async def get_stay_info_for_user_wish(user_seq: int) -> list[StayInfoModel]:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                # wish 테이블에서 state가 'Y'인 stay_seq 추출
                subquery = select(WishOrm.stay_seq).where(
                    WishOrm.user_seq == user_seq,
                    WishOrm.state == 'Y'
                ).subquery()

                # 추출된 stay_seq를 사용하여 stay_info 테이블과 조인
                stmt = select(StayInfoOrm).join(
                    subquery, StayInfoOrm.stay_seq == subquery.c.stay_seq
                )

                result = await session.execute(stmt)
                return stay_orm_to_pydantic_model(result)
        except Exception as e:
            print(e)
            return []


async def get_stay_info_with_for_user_wish_all(user_seq: int):
    async with postgres_client.session() as session:  # 비동기 세션 사용
        try:
            subquery = select(
                StayInfoOrm,
            ).outerjoin(
                WishOrm.state,
                and_(
                    StayInfoOrm.stay_seq == WishOrm.stay_seq,  # stay_seq 기반으로 조인
                    WishOrm.user_seq == user_seq,  # 특정 사용자의 위시리스트만 고려
                    WishOrm.state == 'Y'  # 위시리스트 상태가 'Y'인 경우만 고려
                )
            ).subquery()

            stmt = select(subquery).add_columns(
                case(
                    subquery.state == "Y", "Y",
                    else_="N"
                )
            )

            result = await session.execute(stmt)  # 비동기 쿼리 실행
            pydantic_model = stay_orm_to_pydantic_model_wish(result)
            print(pydantic_model)
            return pydantic_model

        except Exception as e:
            print(e)
            return []