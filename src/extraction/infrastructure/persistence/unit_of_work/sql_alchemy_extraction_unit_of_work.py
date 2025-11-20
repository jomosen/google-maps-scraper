from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort
from shared.application.ports.unit_of_work_port import UnitOfWorkFactoryPort
from shared.infrastructure.persistence.database.mysql_connector import MySQLConnector


class SqlAlchemyExtractionUnitOfWork(ExtractionUnitOfWorkPort):

    def __init__(self, 
                 session_factory, 
                 extraction_job_repo_cls,
                 extraction_task_repo_cls):
        
        self._session_factory = session_factory
        self._extraction_job_repo_cls = extraction_job_repo_cls
        self._extraction_task_repo_cls = extraction_task_repo_cls

        self.session = None
        self.extraction_job_repo = None
        self.extraction_task_repo = None

    def __enter__(self):
        self.session = self._session_factory()
        self.extraction_job_repo = self._extraction_job_repo_cls(self.session)
        self.extraction_task_repo = self._extraction_task_repo_cls(self.session)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        finally:
            self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

class SqlAlchemyExtractionUnitOfWorkFactory(UnitOfWorkFactoryPort):

    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def __call__(self) -> SqlAlchemyExtractionUnitOfWork:

        from extraction.infrastructure.persistence.repositories.sql_alchemy_extraction_job_repository import SqlAlchemyExtractionJobRepository
        from extraction.infrastructure.persistence.repositories.sql_alchemy_extraction_task_repository import SqlAlchemyExtractionTaskRepository
        
        return SqlAlchemyExtractionUnitOfWork(
            session_factory=self.connector.get_session,
            extraction_job_repo_cls=SqlAlchemyExtractionJobRepository,
            extraction_task_repo_cls=SqlAlchemyExtractionTaskRepository
        )