import pathlib
import typing

from args_smart_copy import args


class Logging:
    LOG_PATH = 'log'

    def __init__(self):
        self._create_log_directory()
        self._log_file_path = self._setup_log_file()
        self.copied_files = self._read_log_file() if self._log_file_path.exists() else set()
        self._log_file = self._log_file_path.open('a')

    def __del__(self):
        self._log_file.close()

    def log_copied_file(self, file_path: pathlib.Path) -> None:
        self._log_file.write(f'{str(file_path)}\n')

    def _read_log_file(self) -> typing.Set[str]:
        with self._log_file_path.open() as f:
            return set(map(lambda s: s.strip(), f.readlines()))

    @staticmethod
    def _setup_log_file() -> pathlib.Path:
        if args.log_file:
            return pathlib.Path(args.log_file)
        return pathlib.Path(Logging.LOG_PATH, f'{pathlib.Path(args.source).name}.log')

    @staticmethod
    def log_message(message: str, end: str = '\n') -> None:
        print(message, end=end)

    @staticmethod
    def _check_file_path():
        if not pathlib.Path(args.log_file).is_file():
            raise Exception

    @staticmethod
    def _create_log_directory():
        log_path = pathlib.Path(Logging.LOG_PATH)

        if not log_path.is_dir():
            if log_path.exists():
                raise Exception
            log_path.mkdir()
