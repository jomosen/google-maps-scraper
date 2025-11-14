import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from src.infrastructure.persistence.database.base import Base
from src.application.contracts.abstract_logger import AbstractLogger

load_dotenv()


class MySQLConnector:

    def __init__(self, logger: AbstractLogger):
        self.logger = logger
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = os.getenv("MYSQL_PORT", "3306")
        self.db_name = os.getenv("MYSQL_DB", "google_maps_scraper")

        self.server_engine = self._create_engine(with_database=False)
        self.engine = None
        self.SessionLocal = None

    def _create_engine(self, with_database=True):
        base_url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}"
        if with_database:
            base_url += f"/{self.db_name}"
        return create_engine(
            f"{base_url}?charset=utf8mb4",
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
            future=True
        )

    def get_session(self):
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized. Call init_db() first.")
        return self.SessionLocal()

    def init_db(self):
        with self.server_engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS {self.db_name} "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                )
            )

        self.engine = self._create_engine(with_database=True)

        self.SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

        import src.infrastructure.persistence.models

        Base.metadata.create_all(bind=self.engine)

        self.logger.info("Database initialized successfully")
