import sys
import pathlib
import argparse


class PathAction(argparse.Action):
    def __call__(self, custom_parser, namespace, values, option_string=None):
        values = pathlib.Path(values)
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser(description='Copy files and directories with continue process ability',
                                 prog='Smart Copy')
parser.add_argument('source', help='source path', action=PathAction)
parser.add_argument('destination', help='destination path', action=PathAction)
parser.add_argument('-l', '--log_file', action=PathAction)
parser.add_argument('-f', '--only_files', action='store_true')
parser.add_argument('-v', '--version', action='version', version='0.1')

args = parser.parse_args()

if not (args.source.exists() and args.destination.exists()):
    print('wrong path')
    sys.exit()

if args.log_file and args.log_file.exists() and not args.log_file.is_file():
    print(f'{args.log_file} is wrong path for logging file')
    sys.exit()
