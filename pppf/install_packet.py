#!/usr/bin/python3

from pppf.const import BASEDIR
import sys



def print_usage():
    print("Usage: 3pf install <packet-name> <dest> [flags]\n")
    print("\nInstall a <packet-name> packet to a <dest> directory.")
    print("\nFlags:")
    print("  --help\t\tHelp for install command.")
    print("  --tests\t\tInstall packet with its unit test files.")
    print("  --version <version>\tInstall a specific version of a packet.")
    print("  --no-dependencies\tInstall packet without its dependencies.")
    print("\nExample:")
    print('  3pf install "myOwnLib"\n  --version 2')


def flag_tests(lib, args, i) -> bool:
    lib["unit-tests"] = True
    return True

def flag_version(lib, args, i) -> bool:
    try:
        val = int(args[i + 1])
    except ValueError:
        print("No version number provided after '--version'.")
        return False
    lib["version"] = args[i + 1]
    return True

def flag_nodeps(lib, args, i) -> bool:
    lib["dependencies"] = False
    return True


flags = {
    "--tests": {
        "required": 0,
        "function": flag_tests
    },
    "--version": {
        "required": 1,
        "function": flag_version
    },
    "--no-dependencies": {
        "required": 0,
        "function": flag_nodeps
    }
}

def parse_arguments(args, lib):
    current_param = 0

    for i in range(len(args)):
        if current_param > 0:
            current_param -= 1
            continue

        if args[i] in flags:
            current = flags[args[i]]

            if current.get("required", 0) + i + 1 > len(args):
                print(f"Error: '{args[i][2:]}' flag requires {current.get('required', 0)} parameters.")
                sys.exit(1)

            func = current.get("function", None)
            if func != None:
                if func(lib, args, i) == False:
                    sys.exit(2)
                current_param = current.get("required", 0)

        elif args[i].startswith("--"):
            print(f"Error: '{args[i]}' unknown flag in 'deploy' command.")
            sys.exit(1)


def install_packet(args):

    if len(args) <= 1 or args[0] == "help" or args[0] == "--help":
        print_usage()
        sys.exit(0)

    lib = {
        "unit-tests": False,
        "version": 0, # 0 for latest version
        "dependencies": True
    }

    parse_arguments(args, lib)
    if lib["version"] == 0:
        lib["version"] = lib["version"] # REMINDER TO SET TO LAST VERSION
    print(lib)

