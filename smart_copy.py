import time
import typing
import pathlib

from args_smart_copy import args
from single_copy import SingleCopy


class SmartCopy:
    def __init__(self):
        self.global_sources: typing.List[pathlib.Path] = args.source
        self.global_destination: pathlib.Path = args.destination

        self.time_start = time.perf_counter()

    def copy(self):
        for source in self.global_sources:
            destination = self.global_destination
            SingleCopy(source, destination).copy_manager()


if __name__ == '__main__':
    smart_copy = SmartCopy()
    smart_copy.copy()
