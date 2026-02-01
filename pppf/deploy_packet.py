#!/usr/bin/python3

from pppf.argument_arsenal import ArgumentArsenal
from pppf.tools.json_tools import load_from_json
from pppf.const import BASEDIR


# ============================================
"""              FLAG FUNCTIONS           """
# ============================================

def read_flag_file(filename: str, flag: str):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: '{filename}' is not a valid file for '{flag}' flag.")
        return None
    return content

def flag_test(args, options) -> bool:
    if read_flag_file(args[0], "--test") == None:
        return False
    options["unit-tests"].append(args[0])
    return True

def flag_link(args, options) -> bool:
    file = BASEDIR + "libs.json"

    libs = load_from_json(file)
    if args[0] not in libs:
        print(f"\033[1m> Error\033[0m: '\033[1m{args[0]}\033[0m' is not a library.")
        return False

    if args[1] not in libs[args[0]]["versions"]:
        print(f"\033[1m> {args[0]} version\033[0m has no version '\033[1m{args[1]}\033[0m'.")
        return False
    return True

def flag_header(args, options) -> bool:
    if read_flag_file(args[0], "--header") == None:
        return False
    options["header"] = args[0]

def store_sources(current: str, options) -> bool:
    options["sources"].append(current)


# ============================================
"""             COMMAND FUNCTIONS          """
# ============================================

def ask_packet_info(options):
    name = input("\033[1mPlease give us a name for your new lib.\033[0m\n>> ")

    libs = load_from_json(BASEDIR + "libs.json")
    while name in libs:
        print(f"{name} is already a library, please find another name.")
        name = input("\033[1mPlease give us a name for your new lib.\033[0m\n>> ")

    if name == "exit":
        return False

    options["name"] = name

    options["desc"] = input("\033[1mNow set a short description of what your lib does.\033[0m\n>> ")



def deploy_packet(args):

    options = {"name": None, "desc": None, "unit-tests": [], "link": [],
        "header": None, "sources": [] }

    deploy_command = ArgumentArsenal("deploy", options, args=[],
      desc="Deploy a packet in your 3PF libs.", additional=
      "The source files should be listed at the end of the command.")

    deploy_command.enable_va_arg("srcs", store_sources, optional=False)
    deploy_command.make_flag("--test", ["file.c"], flag_test,
        "Link a unit tests file to your packet.")
    deploy_command.make_flag("--link", ["libName", "version"], flag_link,
        "Create a dependency between your packet and another.")
    deploy_command.make_flag("--header", ["file.h"], flag_header,
        "Link a header to your packet.")

    deploy_command.parse(args)

    if ask_packet_info(options) == False:
        return
    print(options)

