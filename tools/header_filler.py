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
    lala = content.split("}\n\n")
    for i in range(len(lala)):
        tmp = lala[i].split("{", 1)
        if len(tmp) > 0:
            lala[i] = tmp[0].strip("\n")
    tmp = lala[0].split("\n")
    lala[0] = tmp[len(tmp) - 1]
    return lala

def main():
    file = sys.argv[1]
    print(file)
    content = read_file(file)
    funcprototypes = get_function_prototypes(content)
    for func in funcprototypes:
        print(func)
        print("=====")

main()
