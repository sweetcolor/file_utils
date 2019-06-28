import sys
import pathlib


class PrepareSmartCopyInput:
    def __init__(self):
        self._check_argv()

        self.source = pathlib.Path(sys.argv[1])
        self.destination = pathlib.Path(sys.argv[2])

        self._check_input()

    def get_input(self):
        return self.source, self.destination

    @staticmethod
    def _check_argv():
        if len(sys.argv) < 3:
            print('set destination and source directory')
            sys.exit()

    def _check_input(self):
        if not (self.source.exists() and self.destination.exists()):
            print('wrong path')
            sys.exit()
