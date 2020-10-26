import argparse
import sys
import time

from file_util import get_files, read_file, try_write
from insert_util import try_insert
from json_util import add_chapter, add_verse, new_doc
from text_util import (bookname, hebrew_chars, is_hebrew_chapter,
                       should_skip_hebrew)


def check_text_type_error(mt, lxx):
    """Either --mt or --lxx should be selected
    If neither or both, exit """
    if mt == lxx:
        print("You must specify a text type: Either --mt or --lxx")
        sys.exit(1)


def parse_file(file):
    fname = bookname(file)
    document = new_doc(fname, 'mt')
    chapter = 0
    verse = 0
    for line in read_file(file):
        m = is_hebrew_chapter(line)
        if m is not None:
            chapter = m
            document = add_chapter(document, chapter)
            verse = 0
            continue

        if should_skip_hebrew(line):
            continue

        verse += 1
        text_line = hebrew_chars(line)
        document = add_verse(document, verse, text_line)

    return document, fname


def parse_dir(directory=".", pattern='*.txt'):
    """Entrypoint"""
    files = get_files(directory, pattern)
    for file in files:
        yield parse_file(file)


if __name__ == "__main__":
    START = time.perf_counter()
    parser = argparse.ArgumentParser(description="Biblical Text parser")
    parser.add_argument('--dir', type=str, default='.')
    parser.add_argument('--file', type=str, default=None)
    parser.add_argument('--pattern', type=str, default='*.txt')
    parser.add_argument('--insert', action="store_true")
    parser.add_argument('--write', action="store_true")
    parser.add_argument('--write-force', action="store_true")
    FLAGS, _ = parser.parse_known_args()

    # check_text_type_error(FLAGS.mt, FLAGS.lxx)

    # --file takes precedence over --dir
    if FLAGS.file is not None:
        try:
            document, fname = parse_file(FLAGS.file)
            try_write(document, 'mt', fname, FLAGS.write)
            try_insert(document, FLAGS.insert)
        except Exception as e:
            print(f'Encountered error {e}, stopping: {FLAGS.file}')
    else:
        for doc, fname in parse_dir(FLAGS.dir, FLAGS.pattern):
            try_write(doc, 'mt', fname, FLAGS.write)
            try_insert(doc, FLAGS.insert)

    print(f'\nDone in {round(time.perf_counter() - START, 3)}s')
