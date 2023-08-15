from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self, dsn: str = None):
        self.dsn = dsn

    def connect(self) -> async_sessionmaker[AsyncSession]:
        # TODO: Handle connect errors
        engine = create_async_engine(self.dsn, echo=True)
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        return async_session
