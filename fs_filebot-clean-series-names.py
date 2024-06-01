#!/usr/bin/env python

import os
import sys

def scan(input_paths):
    for input_path in input_paths:
        if not os.path.exists(input_path):
            print(f"Error: Path '{input_path}' does not exist.")
            continue

        if os.path.isfile(input_path):  # Check if it's a file
            parts = input_path.split("/")
            q = parts[-1]
            filebot = f"filebot -r -rename --db TheTVDB --action move --conflict auto --q \"{q}\" \"{input_path}\""
            print(filebot)
            os.system(filebot)
        elif os.path.isdir(input_path):  # Check if it's a directory
            tree = os.listdir(input_path)
            for file in tree:
                filepath = os.path.join(input_path, file)
                if os.path.isfile(filepath):  # Check if it's a file before proceeding
                    parts = filepath.split("/")
                    q = parts[-1]
                    filebot = f"filebot -r -rename --db TheTVDB --action move --conflict auto --q \"{q}\" \"{filepath}\""
                    print(filebot)
                    os.system(filebot)
                else:
                    print(f"'{filepath}' is not a file.")
        else:
            print(f"'{input_path}' is neither a file nor a directory.")

if __name__ == "__main__":
    if len(sys.argv) > 1:  # Check if command-line arguments are provided
        input_paths = sys.argv[1:]
        scan(input_paths)
    else:  # If no command-line arguments, read from standard input
        input_paths = [line.strip() for line in sys.stdin]
        scan(input_paths)

