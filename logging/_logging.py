import pathlib
import abc

from args_smart_copy import args


class _Logging(abc.ABC):
    LOG_PATH = 'log'
    EXTENSION = 'log'
    ARG_LOG_FILE = args.log_file

    def __init__(self):
        self._create_log_directory()
        self._log_file_path = self._setup_log_file()

    @classmethod
    def _setup_log_file(cls) -> pathlib.Path:
        if cls.ARG_LOG_FILE:
            return pathlib.Path(cls.ARG_LOG_FILE)
        return pathlib.Path(cls.LOG_PATH, f'{pathlib.Path(args.source[0]).name}.{cls.EXTENSION}')

    @classmethod
    def _create_log_directory(cls) -> None:
        log_path = pathlib.Path(cls.LOG_PATH)

        if not log_path.is_dir():
            if log_path.exists():
                raise Exception
            log_path.mkdir()

    @staticmethod
    def log_message(message: str, end: str = '\n') -> None:
        print(message, end=end)
