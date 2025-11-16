from extraction.application.ports.extraction_unit_of_work_port import ExtractionUnitOfWorkPort


class SqlAlchemyUnitOfWork(ExtractionUnitOfWorkPort):

    def __init__(self, 
                 session_factory, 
                 extraction_job_repo_cls,
                 job_task_repo_cls):
        
        self._session_factory = session_factory
        self._extraction_job_repo_cls = extraction_job_repo_cls
        self._job_task_repo_cls = job_task_repo_cls

        self.session = None
        self.extraction_job_repo = None
        self.job_task_repo = None

    def __enter__(self):
        self.session = self._session_factory()
        self.extraction_job_repo = self._extraction_job_repo_cls(self.session)
        self.job_task_repo = self._job_task_repo_cls(self.session)

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
