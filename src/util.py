import os.path


def read_lines(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return [line.strip('\n') for line in f.readlines()]


def write_lines(filename, lines):
    with open(filename, "w+") as f:
        f.write("\n".join(lines))


def merge_results(input_files, output_file):
    lines = set()
    for input_file in input_files:
        for line in read_lines(input_file):
            lines.add(line)
    write_lines(output_file, list(lines))


def subtract_results(input_file, subtract_files, output_file):
    lines = set(read_lines(input_file))
    for sub_file in subtract_files:
        for line in read_lines(sub_file):
            lines.remove(line)
    write_lines(output_file, list(lines))
