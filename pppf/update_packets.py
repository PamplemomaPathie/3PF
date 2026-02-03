#!/usr/bin/python3

from pppf.argument_arsenal import ArgumentArsenal
from pppf.const import BASEDIR, LIBDIR
from pppf.reload_packets import reload_libs
from pppf.list_packets import load_libs, print_lib
from pppf.tools.file_tools import read_file, write_to_file, create_directory
from pppf.tools.prototype_parser import get_function_prototypes
from pppf.tools.json_tools import save_to_json


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
    options["tests"].append(args[0])
    return True

def flag_header(args, options) -> bool:
    if read_flag_file(args[0], "--header") == None:
        return False
    options["header"] = args[0]

def store_sources(current: str, options) -> bool:
    try:
        with open(current, "r") as file:
            content = file.read()
    except FileNotFoundError or Exception:
        print(f"\033[1;35mWarning\033[0m: '{current}' is not a valid file.")
        return False
    options["sources"].append(current)



def update_packets(args):

    options = {"tests": [], "header": None, "sources": []}

    update_command = ArgumentArsenal("update", options, args=["libName"],
      desc="Create a new version of your packet.",
      additional="A packet can have multiple versions, here is the place to create a new one!")

    update_command.enable_va_arg("srcs", store_sources, optional=False)
    update_command.make_flag("--test", ["file.c"], flag_test,
        "Link a unit tests file to your version.")
    update_command.make_flag("--header", ["file.h"], flag_header,
        "Link a header to your version.")

    update_command.parse(args)
    name = update_command.get_args()[0]

    print(options)

    libs = load_libs()
    if name not in libs:
        print(f"\033[1;31mError\033[0m: '\033[1m{name}\033[0m' is not a library.")
        return

    versions_cnt = len(libs[name]['versions'])
    print(f"\033[1m{name} library already have {versions_cnt} version{'s' if versions_cnt > 1 else ''}.")

    reload_libs()
    print(f"\033[1;32mSuccessfully created a new version for \033[0m\033[1m'{name}'\033[1;32m library\033[0m!")
