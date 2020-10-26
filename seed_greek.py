import argparse
import sys
import time

from file_util import get_files, read_file, try_write
from insert_util import try_insert
from json_util import add_chapter, add_verse, new_doc
from text_util import (bookname, is_greek_chapter, should_break_greek,
                       split_greek_verses)


def parse_file(file):
    fname = bookname(file)
    document = new_doc(fname, 'lxx')
    chapter = 0
    verse = 0

    chapter_line = True
    for line in read_file(file):
        if should_break_greek(line):
            break

        if not line.strip():
            break

        if chapter_line:
            try:
                chapter, verse = is_greek_chapter(line)
            except (TypeError, ValueError):
                print(line)
            document = add_chapter(document, chapter)
            chapter_line = False
            continue

        for text in split_greek_verses(line):
            add_verse(document, verse, text)
            verse += 1

        chapter_line = True

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
    FLAGS, _ = parser.parse_known_args()

    # check_text_type_error(FLAGS.mt, FLAGS.lxx)

    # --file takes precedence over --dir
    if FLAGS.file is not None:
        try:
            document, fname = parse_file(FLAGS.file)
            try_write(document, 'lxx/json', fname, FLAGS.write)
            try_insert(document, FLAGS.insert)
        except Exception as e:
            print(f'Encountered error {e}, stopping: {FLAGS.file}')
    else:
        for doc, fname in parse_dir(FLAGS.dir, FLAGS.pattern):
            try_write(doc, 'lxx/json', fname, FLAGS.write)
            try_insert(doc, FLAGS.insert)

    print(f'\nDone in {round(time.perf_counter() - START, 3)}s')
