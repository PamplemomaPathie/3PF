#!/usr/bin/python3

import sys

from pppf.const import BASEDIR



def print_usage():
    print("Usage: 3pf deploy <Title> [options] <srcs> ...\n")
    print("\nYou must list the sources files at the end of the command")
    print("\nOptions:\n")
    print("  --desf <desc.txt>\t\tSet the library description from a file content.")
    print("  --desc \"your desc\"\t\tSet directly the library description.\n")
    print("  --test <file.c>\t\tSet a unit test file.")
    print("\t\t\t\t(Flag can be called multiple times for multiple files)\n")
    print("  --link <lib-name> <version>\tLink a dependency to another lib.")
    print("\t\t\t\t(Flag can be called multiple times for multiple files)\n")
    print("  --header <file.h>\tLink a header to a lib.\n")
    print("Example:")
    print('  3pf deploy "myOwnLib"\n  --descf ./desc.txt\n  --test ./tests/test_lib.c\n  --link "myFirstLib" 1\n  --header ./include/header_lib.h\n  ./srcs/filelib.c ./srcs/other_file.c')



def flag_desf(lib, args, i):
    try:
        with open(args[i + 1], "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: You must provide a valid file after '--desf' flag.")
        return False
    lib["desc"] = content
    return True

def flag_desc(lib, args, i):
    if args[i + 1] == "":
        print("Please provide a valid description.")
        return False
    lib["desc"] = args[i + 1]
    return True

def flag_test(lib, args, i):
    pass

def flag_link(lib, args, i):
    pass

def flag_header(lib, args, i):
    pass


flags = {
    "--desf": {
        "required": 1,
        "function": flag_desf
    },
    "--desc": {
        "required": 1,
        "function": flag_desc
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

    for i in range(len(args)):
        if current_param > 0:
            current_param -= 1
            continue

        if args[i] in flags:
            current = flags[args[i]]

            if current.get("required", 0) + i + 1 > len(args):
                print(f"Error: {args[i]} requires {current.get("required", 0)} parameters.")
                sys.exit(1)

            func = current.get("function", None)
            if func != None:
                if func(lib, args, i) == False:
                    sys.exit(2)
                current_param = current.get("required", 0)

        elif args[i].startswith("--"):
            print(f"Error: {args[i]} unknown flag in 'deploy' command.")
            sys.exit(1)


def deploy_packet(args):

    if len(args) <= 1 or args[0] == "help":
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

