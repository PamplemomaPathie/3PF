#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from const import BASEDIR, LIBDIR
from pppf.reload_packets import reload_libs
from pppf.pppf_tools import load_libs
from tools.json_tools import save_to_json
from tools.file_tools import read_file, write_to_file, create_directory
from tools.prototype_parser import get_function_prototypes


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

def flag_link(args, options) -> bool:
    file = BASEDIR + "libs.json"

    libs = load_libs()
    if args[0] not in libs:
        print(f"\033[1m> Error\033[0m: '\033[1m{args[0]}\033[0m' is not a library.")
        return False

    if args[1] not in libs[args[0]]["versions"]:
        print(f"\033[1m> {args[0]} library\033[0m has no version '\033[1m{args[1]}\033[0m'.")
        return False
    options["links"][args[0]] = args[1]

    other_links = libs[args[0]]["links"]
    for link in other_links:
        options["links"][link] = other_links[link]
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

def ask_packet_info(options):
    name = input("\033[1mPlease give us a name for your new lib.\033[0m\n>> ")

    libs = load_libs()
    while name in libs or name.strip() == "":
        if name.strip() == "":
            print(f"Please enter a valid name.")
        else:
            print(f"{name} is already a library, please find another name.")
        name = input("\033[1mPlease give us a name for your new lib.\033[0m\n>> ")

    if name == "exit":
        return False

    options["name"] = name.replace("/", "-")

    options["desc"] = input("\033[1mNow set a short description of what your lib does.\033[0m\n>> ")



def create_prerequisites(options, filepath: str):
    create_directory(filepath)

    version_path = filepath + "1/"
    create_directory(version_path)

    source_path = version_path + "srcs/"
    create_directory(source_path)
    prototypes = []
    for src in options["sources"]:
        prototypes += get_function_prototypes(src)
        content = read_file(src, exit=False)
        if content != "":
            src_filename = src.split("/")[-1]
            write_to_file(source_path + src_filename, content)

    if len(options["tests"]) > 0:
        test_path = version_path + "tests/"
        create_directory(test_path)
        for test in options["tests"]:
            test_filename = test.split("/")[-1]
            write_to_file(test_path + test_filename, read_file(test, exit=False))
    if options["header"] != None:
        header_path = version_path + "headers/"
        create_directory(header_path)
        write_to_file(header_path + options["header"],
            read_file(options["header"], exit=False))

    write_to_file(filepath + "desc.txt", options["desc"]);
    prototype_str = "\n".join(prototypes)
    write_to_file(filepath + "content.txt", prototype_str);
    save_to_json(options["links"], filepath + "details.json");


def deploy_packet(args):

    options = {"name": None, "desc": None, "tests": [], "links": {},
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

    filepath = LIBDIR + options["name"] + "/"
    create_prerequisites(options, filepath)
    reload_libs()
    print(f"\033[1;32mCreated\033[0m \033[1m'{options['name']}' \033[32msuccessfully\033[0m!")

