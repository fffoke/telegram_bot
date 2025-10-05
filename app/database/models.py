from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase , Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker , create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    tasks = relationship('Task',back_populates='user')
    hour: Mapped[int] = mapped_column(nullable=True)
    min: Mapped[int] = mapped_column(nullable=True)





class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    des: Mapped[str] = mapped_column(String(500))
    user_id = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship('User', back_populates='tasks')

     


async def asyn_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)