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


def flag_desf(args, i):
    pass

def flag_desc(args, i):
    pass

def flag_test(args, i):
    pass

def flag_link(args, i):
    pass

def flag_header(args, i):
    pass


def parse_arguments(args):

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

    for i in range(len(args)):
        if args[i] in flags:
            current = flags[args[i]]
            if current.get("required", 0) + i + 1 > len(args):
                print(f"Error: {args[i]} requires {current.get("required", 0)} parameters.")
                sys.exit(1)


def deploy_packet(args):

    if len(args) <= 1 or args[0] == "help":
        print_usage()
        sys.exit(0)

    parse_arguments(args)
    print(args)

