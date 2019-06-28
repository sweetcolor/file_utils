import time
import pathlib

from logging import Logging
from prepare_smart_copy_input import PrepareSmartCopyInput


class SmartCopy:
    def __init__(self, source: pathlib.Path, destination: pathlib.Path):
        self.source = source
        self.destination = destination

        self.time_start = time.perf_counter()
        self.log = self._create_logging()

        self._curr_source: pathlib.Path = self.source
        self._curr_destination: pathlib.Path = self.destination
        self._source_size: int = 0

    def copy(self):
        if self.source.is_dir() and self.destination.is_dir():
            self._copy_directory(self.source, self.destination)
        elif self.source.is_file() and self.destination.is_file():
            self._copy_file()
        elif self.source.is_file() and self.destination.is_dir():
            self._curr_destination = self.destination / self.source.name
            self._copy_file()
        else:
            self.log.log_message(f"Can't copy {self.source} to {self.destination}")

    def _copy_directory(self, source_dir: pathlib.Path, destination_dir: pathlib.Path):
        for self._curr_source in source_dir.iterdir():
            self._curr_destination = destination_dir / self._curr_source.name

            if self._curr_source.is_dir():
                self.log.log_message(f'=== copy {self._curr_destination} directory ===')
                self._mkdir_destination()
                self._copy_directory(self._curr_source, self._curr_destination)
            elif self._curr_source.is_file():
                self._copy_file()
            else:
                self.log.log_message(f'Not file {self._curr_source}')

    def _copy_file(self):
        self.log.log_message(f'copy {self._curr_source} file')

        if self._curr_destination.exists():
            self._source_size = self._curr_source.stat().st_size
            destination_size = self._curr_destination.stat().st_size

            if destination_size < self._source_size:
                self.log.log_message(f'destination file has {destination_size} bytes already')
                self._copy_file_from_position(destination_size)
            elif destination_size == self._source_size:
                self.log.log_message('file is already exists')
            else:
                self.log.log_message('destination file is bigger than source')
        else:
            self._copy_file_from_position()

    def _copy_file_from_position(self, position=0):
        block_size = 4096
        source_file = self._curr_source.open('rb')
        source_file.seek(position)

        with self._curr_destination.open('ab') as destination_file:
            while True:
                self.log.log_message(f'copying {self._curr_source} from {position}', end='\r')
                chunk = source_file.read(block_size)

                if not chunk:
                    self.log.log_message('\nEOF')
                    break

                destination_file.write(chunk)
                position += block_size

        self.log.log_message(f'file {self._curr_source.name} is copied, '
                             f'destination size {self._curr_destination.stat().st_size}')

    def _mkdir_destination(self) -> None:
        if not self._curr_destination.exists():
            self.log.log_message('=== make directory ===')
            self._curr_destination.mkdir()

    def _create_logging(self) -> Logging:
        return Logging(f'copying {self.source.name}.log')


if __name__ == '__main__':
    smart_copy = SmartCopy(*PrepareSmartCopyInput().get_input())
    smart_copy.copy()
