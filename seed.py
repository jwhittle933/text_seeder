import argparse
import sys
import time


def check_text_type_error(mt, lxx):
    """Either --mt or --lxx should be selected
    If neither or both, exit """
    if mt == lxx:
        print("You must specify a text type: Either --mt or --lxx")
        sys.exit(1)


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
