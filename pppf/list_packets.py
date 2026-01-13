#!/usr/bin/python3

from pppf.tools.tools import list_dir
from pppf.const import BASEDIR
import os
import sys


def print_usage():
    print("Usage: 3pf list [options]\n") # Need to explain what does the command do
    print("\nOptions:\n")
    print("  --detail\t\t\tDisplay more detail on the libraries.\n")
    print("  --version <number>\t\tList all specific versions.")
    print("  --lib <lib-name>\t\tGet information about a specific library.\n")



def flag_version(lib, args, i) -> bool:
    pass


flags = {
    "--version": {
        "required": 1,
        "function": flag_version
    }
}

def parse_arguments(args, libs):
    current_param = 0

    for i in range(1, len(args)):
        if current_param > 0:
            current_param -= 1
            continue

        if args[i] in flags:
            current = flags[args[i]]

            if current.get("required", 0) + i + 1 > len(args):
                print(f"Error: '{args[i][2:]}' flag requires {current.get("required", 0)} parameters.")
                sys.exit(1)

            func = current.get("function", None)
            if func != None:
                if func(libs, args, i) == False:
                    sys.exit(2)
                current_param = current.get("required", 0)

        elif args[i].startswith("--"):
            print(f"Error: {args[i]} unknown flag in 'deploy' command.")
            sys.exit(1)


def list_packets(args):
    if len(args) >= 1 and args[0] == "help":
        print_usage()
        sys.exit(0)

    libs = []

    parse_arguments(args, libs)
    print(libs)
