import sys
import glob
import os
import pathlib


def get_extensions():
    return set(map(lambda f: pathlib.Path(f).suffix, glob.glob('*') + glob.glob('*')))


def move_files_by_extension(ext_: str):
    files = glob.glob(f'*.{ext_}') + glob.glob(f'*.{ext_}')

    if len(files) > 1:
        if not os.path.exists(ext_):
            os.mkdir(ext_)
        for file_ in files:
            # print(file_, os.path.join(ext, os.path.basename(file_)))
            new_path = os.path.join(ext_, os.path.basename(file_))
            if not os.path.exists(new_path):
                os.rename(file_, new_path)
            else:
                print(file_)


if __name__ == '__main__':
    try:
        dir_path = sys.argv[1]
    except IndexError:
        print('Set start directory!!!')
        sys.exit()

    os.chdir(dir_path)
    # exts = get_extensions()
    # print(exts)
    extensions = ['gif', 'png', 'mp4', 'webm', 'jpeg', 'avi', 'htm']
    for ext in extensions:
        move_files_by_extension(ext)
