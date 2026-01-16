#!/usr/bin/python3

import sys

from pppf.const import BASEDIR



def print_usage():
    print("Usage: 3pf deploy <title> [options] <srcs> ...\n")
    print("\nDeploy a packet in your 3PF libs.")
    print("The source files should be listed at the end of the command.")
    print("\nOptions:")
    print("  --help\t\t\tDisplay help for the deploy command.")
    print("  --desc \"your desc\"\t\tSet packet description.")
    print("  --desf <desc.txt>\t\tSet packet description (from a text file).")
    print("  --test <file.c>\t\tLink a unit tests file to your packet.")
    print("\t\t\t\t(this flag applies to the preceding packet only, and can be used multiple times in one command)")
    print("  --link <lib-name> <version>\tCreate a dependency between your packet and another.")
    print("\t\t\t\t(this flag applies to the preceding packet only, and can be used multiple times in one command)")
    print("  --header <file.h>\t\tLink a header to your packet.\n")
    print("Example:")
    print('  3pf deploy "myOwnLib"\n  --descf ./desc.txt\n  --test ./tests/test_lib.c\n  --link "myFirstLib" 1\n  --header ./include/header_lib.h\n  ./srcs/filelib.c ./srcs/other_file.c')


def read_flag_file(filename: str, flag: str):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: '{filename}' is not a valid file for '{flag}' flag.")
        return None
    return content


def flag_desc(lib, args, i) -> bool:
    if args[i + 1] == "":
        print("Please provide a valid description.")
        return False
    lib["desc"] = args[i + 1]
    return True

def flag_desf(lib, args, i) -> bool:
    content = read_flag_file(args[i + 1], "--desf")
    if content == None:
        return False
    lib["desc"] = content
    return True

def flag_test(lib, args, i) -> bool:
    if read_flag_file(args[i + 1], "--test") == None:
        return False
    lib["unit-tests"].append(args[i + 1])
    return True

def flag_link(lib, args, i) -> bool:
    pass

def flag_header(lib, args, i) -> bool:
    if read_flag_file(args[i + 1], "--header") == None:
        return False
    lib["header"] = args[i + 1]


flags = {
    "--desc": {
        "required": 1,
        "function": flag_desc
    },
    "--desf": {
        "required": 1,
        "function": flag_desf
    },
    "--test": {
        "required": 1,
        "function": flag_test
    },
    "--link": {
        "required": 2,
        "function": flag_link
    },
    "--header": {
        "required": 1,
        "function": flag_header
    }
}

def parse_arguments(args, lib):
    current_param = 0

    lib["name"] = args[0]
    for i in range(1, len(args)):
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


def deploy_packet(args):

    if len(args) <= 1 or args[0] == "help" or args[0] == "--help":
        print_usage()
        sys.exit(0)

    lib = {
        "name": None,
        "desc": None,
        "unit-tests": [],
        "link": [],
        "header": None,
        "sources": []
    }

    parse_arguments(args, lib)
    print(lib)

