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
    print(" --header <file.h>\tLink a header to a lib.")
    print("Example:")
    print('  3pf deploy "myOwnLib"\n  --descf ./desc.txt\n  --test ./tests/test_lib.c\n  --link "myFirstLib" 1\n  --header ./include/header_lib.h\n  ./srcs/filelib.c ./srcs/other_file.c')




def deploy_packet(args):

    if len(args) <= 1 or args[0] == "help":
        print_usage()
        sys.exit(0)

    print(args)
