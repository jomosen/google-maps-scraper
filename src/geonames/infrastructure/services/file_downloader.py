import requests
from contextlib import nullcontext
from src.geonames.infrastructure.services.exceptions.file_download_error import FileDownloadError
from src.geonames.application.contracts.abstract_progress_bar import AbstractProgressBar
from src.geonames.application.contracts.abstract_file_downloader import AbstractFileDownloader


class FileDownloader(AbstractFileDownloader):
    def __init__(self, progress_bar_cls: type[AbstractProgressBar] | None = None):
        self.progress_bar_cls = progress_bar_cls

    def download(self, url: str, dest_path: str) -> None:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("Content-Length", 0))
            chunk_size = 8192

            progress_ctx = (
                self.progress_bar_cls(total=total_size, desc=f"Downloading {url}", unit="B")
                if self.progress_bar_cls
                else nullcontext()
            )

            with open(dest_path, "wb") as f, progress_ctx as bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        if self.progress_bar_cls:
                            bar.update(len(chunk))

        except Exception as e:
            raise FileDownloadError(f"Failed to download {url}: {e}") from e
