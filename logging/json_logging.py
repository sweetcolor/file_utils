import pathlib
import typing
import json
from . import _Logging
from args_smart_copy import args


class JsonLogging(_Logging):
    LOG_PATH = 'json_log'
    EXTENSION = 'json'
    ARG_LOG_FILE = args.json_log_file

    def __init__(self):
        super().__init__()
        self.json_log = self.read_()

    def __del__(self):
        self.write()

    def write(self):
        json.dump(self.json_log, self._log_file_path)

    def read_(self) -> typing.Dict[str, typing.Union[bool, typing.Dict]]:
        return json.load(self._log_file_path) if self._log_file_path.exists() else dict()
