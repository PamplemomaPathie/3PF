#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from pppf.const import LIBDIR
from pppf.reload_packets import reload_libs
from pppf.list_packets import load_libs
from tools.file_tools import read_file, write_to_file, create_directory


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


# ============================================
"""             COMMAND FUNCTIONS          """
# ============================================

def create_prerequisites(options, filepath: str, changelog: str):

    create_directory(filepath)

    write_to_file(filepath + "changelog.txt", changelog)
    source_path = filepath + "srcs/"
    create_directory(source_path)
    for src in options["sources"]:
        content = read_file(src, exit=False)
        if content != "":
            src_filename = src.split("/")[-1]
            write_to_file(source_path + src_filename, content)

    if len(options["tests"]) > 0:
        test_path = filepath + "tests/"
        create_directory(test_path)
        for test in options["tests"]:
            test_filename = test.split("/")[-1]
            write_to_file(test_path + test_filename, read_file(test, exit=False))
    if options["header"] != None:
        header_path = filepath + "headers/"
        create_directory(header_path)
        write_to_file(header_path + options["header"],
            read_file(options["header"], exit=False))


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

    libs = load_libs()
    if name not in libs:
        print(f"\033[1;31mError\033[0m: '\033[1m{name}\033[0m' is not a library.")
        return

    versions_cnt = len(libs[name]['versions'])
    print(f"Found \033[1m{versions_cnt} version{'s' if versions_cnt > 1 else ''}\033[0m in '{name}' library.")

    print("\033[1mPlease give us a changelog that summarize your version.\033[0m")
    changelog = input(">> ")

    try:
        version = int(list(libs[name]["versions"])[-1])
    except Exception as e:
        print("\033[1;31mError\033[0m\033[1m: last version name is not valid.\033[0m")
        return

    filepath = LIBDIR + name + "/" + str(version + 1) + "/"
    create_prerequisites(options, filepath, changelog)

    reload_libs()
    print(f"\033[1;32mSuccessfully created a new version for \033[0m\033[1m'{name}'\033[1;32m library\033[0m!")
