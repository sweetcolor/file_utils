import pathlib
import typing
from . import _Logging


class TextLogging(_Logging):
    def __init__(self):
        super().__init__()

        self.copied_files = self._read_copied_files()
        self._log_file = self._log_file_path.open('a')

    def __del__(self):
        self._log_file.close()

    def log_copied_file(self, file_path: pathlib.Path) -> None:
        self._log_file.write(f'{str(file_path)}\n')

    def _read_copied_files(self) -> typing.Set[str]:
        return set(self._log_file_path.read_text().split() if self._log_file_path.exists() else [])
