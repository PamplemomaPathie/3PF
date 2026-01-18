#!/usr/bin/python3

import sys

def read_file(filename: str, exit=True):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        if exit == True:
            print(f"No file {filename}.")
            sys.exit(1)
        else:
            return ""
    return content
