from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


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

    def connect(self) -> AsyncEngine:
        # TODO: Handle connect errors
        engine = create_async_engine(self.dsn, echo=True)
        return engine
