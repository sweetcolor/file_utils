import pathlib

from prepare_smart_copy_input import args


class Logging:
    LOG_PATH = 'log'

    def __del__(self):
        self._log_file.close()

        self._log_file = self.open_existing_logging_file() if args.log_file else self.create_new_logging_file()

    def create_new_logging_file(self):
        self._create_log_directory()
        return pathlib.Path(Logging.LOG_PATH, f'copying {args.source.name}.log').open('a')

    def open_existing_logging_file(self):
        self._check_file_path()
        return open(args.log_file)

    def log_copied_file(self, file_path: pathlib.Path) -> None:
        self._log_file.write(f'{str(file_path)}\n')

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
