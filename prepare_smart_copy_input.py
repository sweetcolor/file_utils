import sys
import pathlib
import argparse


class PrepareSmartCopyInput:
    def __init__(self):
        self._check_argv()

        self.source = pathlib.Path(sys.argv[1])
        self.destination = pathlib.Path(sys.argv[2])
        self.log_file = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else None

        self._check_input()

    def get_input(self):
        return self.source, self.destination, self.log_file

    @staticmethod
    def _check_argv():
        if len(sys.argv) < 3:
            print('set destination and source directory')
            sys.exit()

    def _check_input(self):
        if not (self.source.exists() and self.destination.exists()):
            print('wrong path')
            sys.exit()


parser = argparse.ArgumentParser(description='Copy files and directories with continue process ability',
                                 prog='Smart Copy')
parser.add_argument('source', help='source path')
parser.add_argument('destination', help='destination path')
parser.add_argument('-l', '--log_file')
parser.add_argument('-f', '--only_files', action='store_true')
parser.add_argument('-v', '--version', action='version', version='0.0.1')

args = parser.parse_args(['foo', 'bar'])
print(args)
