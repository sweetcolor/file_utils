import pathlib


class Logging:
    LOG_PATH = 'log'

    def __del__(self):
        self._log_file.close()

    def create_new_logging_file(self, file_name: str):
        self._create_log_directory()
        path = pathlib.Path(Logging.LOG_PATH, file_name)
        open_mode = 'a' if path.exists() else 'w'
        self._log_file = open(path, open_mode)

    def open_existing_logging_file(self, file_path: pathlib.Path):
        self._log_file = file_path.open('a')

    def log_copied_file(self, file_path: pathlib.Path) -> None:
        self._log_file.write(f'{str(file_path)}\n')

    @staticmethod
    def log_message(message: str, end: str = '\n') -> None:
        print(message, end=end)

    @staticmethod
    def _create_log_directory():
        log_path = pathlib.Path(Logging.LOG_PATH)

        if not log_path.is_dir():
            if log_path.exists():
                raise Exception
            log_path.mkdir()
