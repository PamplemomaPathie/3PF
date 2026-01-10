#!/usr/bin/pyton3

import sys

def check_install(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"No file {filename}.")
        sys.exit(1)

    parts = content.split("\n")
    print(parts)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} <config-file>")
        sys.exit(0)
    check_install(sys.argv[1])
