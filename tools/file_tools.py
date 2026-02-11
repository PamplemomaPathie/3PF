#!/usr/bin/python3

import sys
import os

def read_file(filename: str, exit=False):
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


def write_to_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error: {e}")


def create_directory(directory_name):
    try:
        os.makedirs(directory_name, exist_ok=True)
    except Exception as e:
        print(f"Error: {e}")


def copy_directory(src: str, dest: str):
    all_files = os.listdir(src)

    for file in all_files:
        content = read_file(src + file)
        write_to_file(dest + file, content)
