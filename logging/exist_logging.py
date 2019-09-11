import pathlib
from args_smart_copy import args
from . import _Logging


class ExistLogging(_Logging):
    LOG_PATH = 'exist_log'
    ARG_LOG_FILE = args.exist_log_file

    def __init__(self):
        super().__init__()
        self._log_file = self._log_file_path.open('w')

    def log_exist_file(self, file_path: pathlib.Path) -> None:
        self._log_file.write(f'{str(file_path)}\n')

