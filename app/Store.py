import uuid
from typing import Mapping, Sequence

from sqlalchemy import AsyncAdaptedQueuePool, select, update, ScalarResult, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Info(Base):
    __tablename__ = "info"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    sheet_id: Mapped[str] = mapped_column(String(40), nullable=True)

    cron_question_about_game: Mapped[str] = mapped_column(String(40), nullable=True)

    cron_game: Mapped[str] = mapped_column(String(40), nullable=True)

    time_zone: Mapped[str] = mapped_column(String(40), nullable=True)

    chat_id: Mapped[int] = mapped_column(nullable=False)

    forum_id: Mapped[int] = mapped_column(nullable=True)

    range: Mapped[str] = mapped_column(String(9), nullable=True)

    def get_column_mapping(self) -> Mapping:
        return {
            'sheet_id': self.sheet_id,
            'cron_question_about_game': self.cron_question_about_game,
            'cron_game': self.cron_game,
            'chat_id': self.chat_id,
            'forum_id': self.forum_id,
            'time_zone': self.time_zone,
            'range': self.range
        }

    def get_info(self) -> str:
        return f"""
            'sheet_id': {self.sheet_id},
            'cron_question_about_game': {self.cron_question_about_game},
            'cron_game': {self.cron_game},
            'chat_id': {self.chat_id},
            'forum_id': {self.forum_id},
            'time_zone': {self.time_zone},
            'range': {self.range}"""


_engine = create_async_engine("sqlite+aiosqlite:///database.db", poolclass=AsyncAdaptedQueuePool)


async def select_by_chat_and_forum(chat: int, forum: int = None) -> Info:
    if not chat:
        raise ValueError("Chat id is null")

    async with AsyncSession(_engine) as session:
        return await session.scalar(select(Info).where(Info.chat_id == chat).where(Info.forum_id == forum))


async def select_all() -> Sequence[Info]:
    async with AsyncSession(_engine) as session:
        result: ScalarResult[Info] = await session.scalars(select(Info))

        return result.all()


async def save_info(info: Info) -> None:
    if not info:
        raise ValueError("Chat id is null")

    async with AsyncSession(_engine) as session:
        session.add(info)

        await session.commit()


async def update_info(info: Info):
    async with (AsyncSession(_engine) as session):
        await session.execute(
            update(Info)
            .where(Info.chat_id == info.chat_id)
            .where(Info.forum_id == info.forum_id)
            .values(info.get_column_mapping()))

        await session.commit()


async def create_table() -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def info_is_exist(info: Info) -> bool:
    return await select_by_chat_and_forum(info.chat_id, info.forum_id) is not None
