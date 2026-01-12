#!/usr/bin/python3

import sys

def read_file(filename: str):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"No file {filename}.")
        sys.exit(1)
    return content

def get_function_prototypes(content: str):
    lala = content.split("\n")
    return lala

def main():
    file = sys.argv[1]
    print(file)
    content = read_file(file)
    funcprototypes = get_function_prototypes(content)
    print(funcprototypes)

main()
