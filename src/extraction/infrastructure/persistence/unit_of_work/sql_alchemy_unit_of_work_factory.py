from shared.infrastructure.persistence.database.mysql_connector import MySQLConnector
from shared.application.ports.unit_of_work_factory_port import UnitOfWorkFactoryPort
from extraction.infrastructure.persistence.unit_of_work.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork
    

class SqlAlchemyUnitOfWorkFactory(UnitOfWorkFactoryPort):

    def __init__(self, connector: MySQLConnector):
        self.connector = connector

    def __call__(self) -> SqlAlchemyUnitOfWork:

        from extraction.infrastructure.persistence.repositories.sql_alchemy_extraction_job_repository import SqlAlchemyExtractionJobRepository
        from extraction.infrastructure.persistence.repositories.sql_alchemy_job_task_repository import SqlAlchemyExtractionTaskRepository
        
        return SqlAlchemyUnitOfWork(
            session_factory=self.connector.get_session,
            extraction_job_repo_cls=SqlAlchemyExtractionJobRepository,
            job_task_repo_cls=SqlAlchemyExtractionTaskRepository
        )
