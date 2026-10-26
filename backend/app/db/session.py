from collections.abc import Generator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings, normalize_database_url


def create_db_engine(database_url: str) -> Engine:
    normalized_url = normalize_database_url(database_url)
    connect_args = {"check_same_thread": False} if normalized_url.startswith("sqlite") else {}
    engine_options: dict[str, object] = {
        "connect_args": connect_args,
        "pool_pre_ping": True,
    }
    if normalized_url == "sqlite:///:memory:":
        engine_options["poolclass"] = StaticPool
    engine = create_engine(normalized_url, **engine_options)

    if normalized_url.startswith("sqlite"):

        @event.listens_for(engine, "connect")
        def enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


settings = get_settings()
engine = create_db_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session]:
    with SessionLocal() as session:
        yield session

