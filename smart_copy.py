import time
import pathlib

from logging import TextLogging
from logging import JsonLogging
from args_smart_copy import args


class SmartCopy:
    def __init__(self):
        self.source: pathlib.Path = args.source
        self.destination: pathlib.Path = args.destination

        self.time_start = time.perf_counter()
        self.log = self._create_logging()
        self.json_log = JsonLogging()

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
        list_directory = list(source_dir.iterdir())

        for i, self._curr_source in enumerate(list_directory):
            self._curr_destination = destination_dir / self._curr_source.name
            counter = f'{i+1}/{len(list_directory)}'

            if self._curr_source.is_dir():
                self.log.log_message(f'=== copy {self._curr_source} directory {counter} ===')
                self._mkdir_destination()
                self._copy_directory(self._curr_source, self._curr_destination)
            elif self._curr_source.is_file():
                if str(self._curr_source) in self.log.copied_files:
                    self.log.log_message(f'{self._curr_source} file already copied, so skipped')
                else:
                    self.log.log_message(f'copy {self._curr_source} file {counter} in {source_dir}')
                    self._copy_file()
            else:
                self.log.log_message(f'Not file {self._curr_source}')

    def _copy_file(self):
        self._source_size = self._curr_source.stat().st_size

        if self._curr_destination.exists():
            destination_size = self._curr_destination.stat().st_size
            self.log.log_message(f'source file has {self._source_size} bytes')

            if destination_size < self._source_size:
                self.log.log_message(f'destination file has {destination_size} bytes already')
                self._copy_file_from_position(destination_size)
            elif destination_size == self._source_size:
                self.log.log_message('file is already exists')
            else:
                self.log.log_message('destination file is bigger than source')
        else:
            self._copy_file_from_position()
        self.log.log_copied_file(self._curr_source)

    def _copy_file_from_position(self, position=0):
        block_size = 4096
        source_file = self._curr_source.open('rb')
        source_file.seek(position)

        with self._curr_destination.open('ab') as destination_file:
            while True:
                self.log.log_message(f'copying {self._curr_source.relative_to(self.source)} from {position} '
                                     f'/ {self._source_size}', end='\r')
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

    @staticmethod
    def _create_logging() -> TextLogging:
        return TextLogging()


if __name__ == '__main__':
    smart_copy = SmartCopy()
    smart_copy.copy()
