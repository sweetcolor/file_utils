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
        json_log = self.read_()
        self.copy = json_log.get('copy', list())
        self.skip = set(json_log.get('skip', set()))

    def read_(self) -> typing.Dict[str, typing.Union[bool, typing.Dict]]:
        if self._log_file_path.exists():
            with self._log_file_path.open() as f:
                return json.load(f)
        return dict()
