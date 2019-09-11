import pathlib
from args_smart_copy import args
from logging import ExistLogging
from logging import JsonLogging
from logging import TextLogging


class SingleCopy:
    def __init__(self, source, destination):
        if args.exist_log_file:
            self.exist_log = ExistLogging()
        self.json_log = JsonLogging()
        self.log = self._create_logging()
        self.source: pathlib.Path = source
        self.destination: pathlib.Path = destination
        self._curr_source: pathlib.Path = self.source
        self._curr_destination: pathlib.Path = self.destination
        self._source_size: int = 0
        self.skip = set(map(lambda s: source.joinpath(s), self.json_log.skip))

    def copy_manager(self):
        if self.source.is_dir() and self.destination.is_dir():
            if args.create_folder:
                self.destination /= self.source.name
                self.destination.mkdir(parents=True, exist_ok=True)

            if self.json_log.copy:
                for copy_path in self.json_log.copy:
                    source = self.source / copy_path
                    destination = self.destination / copy_path

                    if source.is_dir():
                        destination.mkdir(parents=True, exist_ok=True)

                    self._copy_directory(source, destination)
            else:
                self._copy_directory(self.source, self.destination)

        elif self.source.is_file() and self.destination.is_file():
            self._curr_source = self.source
            self._copy_file()
        elif self.source.is_file() and self.destination.is_dir():
            self._curr_source = self.source
            self._curr_destination = self.destination / self.source.name
            self._copy_file()
        else:
            self.log.log_message(f"Can't copy {self.source} to {self.destination}")

    def _copy_directory(self, source_dir: pathlib.Path, destination_dir: pathlib.Path):
        list_directory = set(source_dir.iterdir()).difference(self.skip)

        for i, self._curr_source in enumerate(list_directory):
            self._curr_destination = destination_dir / self._curr_source.name
            counter = f'{i+1}/{len(list_directory)}'

            if self._curr_source.is_dir() and not args.only_files:
                self.log.log_message(f'=== copy {self._curr_source} directory {counter} ===')
                self._curr_destination.mkdir(parents=True, exist_ok=True)
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
                if args.exist_log_file:
                    self.exist_log.log_exist_file(self._curr_destination)
                else:
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

    @staticmethod
    def _create_logging() -> TextLogging:
        return TextLogging()

