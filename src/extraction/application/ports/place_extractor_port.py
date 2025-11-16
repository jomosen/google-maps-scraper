from extraction.domain.job_task import JobTask


class PlaceExtractorPort:
    
    def extract(self, job_task: JobTask):
        raise NotImplementedError
