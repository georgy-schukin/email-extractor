from util import merge_results, subtract_results

import sys


def main():
    if len(sys.argv) < 4:
        print("Usage: {0} merge|sub [input files] [output file]".format(sys.argv[0]))
    mode = sys.argv[1]
    if mode == "merge":
        merge_results(sys.argv[2:-1], sys.argv[-1])
    elif mode == "sub":
        subtract_results(sys.argv[2], sys.argv[3:-1], sys.argv[-1])
    else:
        print("Unknown mode: {0}".format(mode))


if __name__ == '__main__':
    main()
