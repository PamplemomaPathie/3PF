#!/usr/bin/python3

from pppf.tools.tools import list_dir
from pppf.const import BASEDIR
import os
import sys


def print_usage():
    print("Usage: 3pf list [options]\n\n")
    print("List all installed packages.")
    print("\nOptions:")
    print("  --help\t\tHelp for list command.")
    print("  --detail\t\tDisplay more detail on the libraries.")
    print("  --version <number>\tList all specific versions.")
    print("  --lib <lib-name>\tGet information about a specific library.")



def flag_detail(lib, args, i) -> bool:
    lib["detail"] = True

def flag_version(lib, args, i) -> bool:
    pass

def flag_lib(lib, args, i) -> bool:
    pass

flags = {
    "--detail": {
        "required": 0,
        "function": flag_detail
    },
    "--version": {
        "required": 1,
        "function": flag_version
    },
    "--lib": {
        "required": 1,
        "function": flag_lib
    }
}

def parse_arguments(args, libs):
    current_param = 0

    for i in range(len(args)):
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

        else:
            print(f"Error: '{args[i]}' unknown option in 'list' command.")
            sys.exit(1)


def list_packets(args):
    if len(args) >= 1 and (args[0] == "help" or args[0] == "--help"):
        print_usage()
        sys.exit(0)

    libs = {
        "detail": False,
        "version": 0, # 0 For all versions
        "lib": []
    }

    parse_arguments(args, libs)
    print(libs)
