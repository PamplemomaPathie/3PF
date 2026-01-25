#!/usr/bin/python3

from pppf.argument_arsenal import ArgumentArsenal


def print_usage():
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


def flag_desc(args, options) -> bool:
    if args[0] == "":
        print("Please provide a valid description.")
        return False
    options["desc"] = args
    return True

def flag_desf(args, options) -> bool:
    content = read_flag_file(args[0], "--desf")
    if content == None:
        return False
    options["desc"] = content
    return True

def flag_test(args, options) -> bool:
    if read_flag_file(args[0], "--test") == None:
        return False
    options["unit-tests"].append(args[0])
    return True

def flag_link(args, options) -> bool:
    pass

def flag_header(args, options) -> bool:
    if read_flag_file(args[0], "--header") == None:
        return False
    options["header"] = args[0]

def store_sources(current: str, options) -> bool:
    options["sources"].append(current)

def deploy_packet(args):

    options = {
        "name": None,
        "desc": None,
        "unit-tests": [],
        "link": [],
        "header": None,
        "sources": []
    }

    deploy_command = ArgumentArsenal("deploy", options, args=["LibName"],
      desc="Deploy a packet in your 3PF libs.", additional=
      "The source files should be listed at the end of the command.")

    deploy_command.enable_va_arg("srcs", store_sources)
    deploy_command.make_flag("--desc", ["libDesc"], flag_desc,
        "Set packet description.")
    deploy_command.make_flag("--desf", ["descF.txt"], flag_desf,
        "Set packet description from a text file.")
    deploy_command.make_flag("--test", ["file.c"], flag_test,
        "Link a unit tests file to your packet.")
    deploy_command.make_flag("--link", ["libName", "version"], flag_link,
        "Create a dependency between your packet and another.")
    deploy_command.make_flag("--header", ["file.h"], flag_header,
        "Link a header to your packet.")

    deploy_command.parse(args)

    print(options)

