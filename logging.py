import pathlib


class Logging:
    LOG_PATH = 'log'

    def __init__(self, log_name: str):
        self._create_log_directory()
        self._log_file = open(pathlib.Path(Logging.LOG_PATH, log_name), 'w')

    def __del__(self):
        self._log_file.close()

    def log_copied_file(self, file_path: pathlib.Path) -> None:
        self._log_file.write(f'{str(file_path)}\n')

    @staticmethod
    def log_message(message: str, end: str = '\n') -> None:
        print(message, end=end)

    @staticmethod
    def _create_log_directory():
        log_path = pathlib.Path(Logging.LOG_PATH)

        if not log_path.exists():
            if not log_path.is_dir():
                raise Exception
            log_path.mkdir()
