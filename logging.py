import pathlib


class Logging:
    def __init__(self, log_name: str):
        self._log_file = open(log_name, 'w')

    def __del__(self):
        self._log_file.close()

    def log_copied_file(self, file_path: pathlib.Path) -> None:
        self._log_file.write(f'{str(file_path)}\n')

    @staticmethod
    def log_message(message: str, end: str = '\n') -> None:
        print(message, end=end)
