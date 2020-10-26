import os
import sys
from fnmatch import fnmatch
from pathlib import Path

from json_util import serialize


def __resolve_path(path):
    return str(Path(path).resolve())


def get_files(directory, pattern="*.txt"):
    """Get list of files to parse and insert"""
    _dir = __resolve_path(directory)
    files = [
        f'{_dir}/{file}' for file in os.listdir(_dir)
        if fnmatch(file, pattern)
    ]
    if files == []:
        print(f'No files matching {pattern} found in {_dir}')
        sys.exit(0)
    else:
        return files


def read_file(filename):
    """Read file contents line by line"""
    with open(filename) as f:
        print(f'Reading from {os.path.basename(f.name)}')
        lines = f.readlines()
        for line in lines:
            yield line.strip()


def try_write(document, dir, filename, should):
    if should:
        fname = f'formatted/{dir}/{filename}.json'
        # overwrite = 'n'
        # if os.path.exists(fname):
        with open(fname, "w+") as f:
            f.write(serialize(document))
