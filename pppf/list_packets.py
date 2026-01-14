#!/usr/bin/python3

from pppf.tools.tools import list_dir
from pppf.const import BASEDIR
import os
import sys


def print_usage():
    print("Usage: 3pf list [options] [libs]\n\n")
    print("List all installed packages.")
    print("You can also list more data about specific libraries by naming them.")
    print("\nOptions:")
    print("  --help\t\tHelp for list command.")
    print("  --detail\t\tDisplay more detail on the libraries.")
    print("  --version <number>\tList all specific versions.")


def flag_detail(lib, args, i) -> bool:
    lib["detail"] = True

def flag_version(lib, args, i) -> bool:
    try:
        version = int(args[i + 1])
        lib["version"] = version
    except Exception as e:
        print(f"Error: '{args[i + 1]}' is not a valid number for flag version.")
        return False

def flag_lib(lib, args, i) -> bool:
    lib["lib"].append(args[i + 1])

flags = {
    "--detail": {
        "required": 0,
        "function": flag_detail
    },
    "--version": {
        "required": 1,
        "function": flag_version
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

        elif args[i].startswith("--"):
            print(f"Error: '{args[i]}' unknown option in 'list' command.")
            sys.exit(1)

        else:
            libs["lib"].append(args[i])


def list_libs(libs):
    basedir = "./.3pf/libs/"
    lib_dir = os.listdir(basedir)

    lib_list = {}
    for lib in lib_dir:
        if not os.path.isdir(basedir + lib):
            print(f"Warning: Bad Configuration for '{lib}' library.")
            continue
        content = os.listdir(basedir + lib)
        lib_list[lib] = content
        if "content.txt" not in content:
            print(f"Warning: Bad Configuration for '{lib}' library.")
    print(lib_list)


def list_packets(args):
    if len(args) >= 1 and ("help"in args or "--help" in args):
        print_usage()
        sys.exit(0)

    libs = {
        "detail": False,
        "version": 0, # 0 For all versions
        "lib": []
    }

    parse_arguments(args, libs)
    print(libs)
    try:
        list_libs(libs)
    except Exception as e:
        print("Wrong configuration of 3PF, please consider reinstalling the client.")
        print(f"Error detail: {e}")
        sys.exit(2)

