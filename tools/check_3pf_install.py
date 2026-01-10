#!/usr/bin/python3

import sys

CONST_FOLDER = "../const"

def read_file(filename: str):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"No file {filename}.")
        sys.exit(1)
    return content


def get_const_info(filename: str):
    content = read_file(filename)

    parts = content.split("\n")
    print(parts)


def check_install(filename: str, settings):
    content = read_file(filename)

    parts = content.split("\n")
    print(parts)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} <config-file>")
        sys.exit(0)

    settings = get_const_info("/".join(sys.argv[0].split("/")[:-1]) + ("/" if '/' in sys.argv[0] else "") + CONST_FOLDER) # Find const file depending on argv[0]
    print(settings)
    check_install(sys.argv[1], settings)
