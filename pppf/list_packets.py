#!/usr/bin/python3

from pppf.const import BASEDIR, LIBDIR
from pppf.argument_arsenal import ArgumentArsenal
from pppf.tools.json_tools import save_to_json, load_from_json
from pppf.tools.prototype_parser import get_cleaned_function_prototypes
from pppf.tools.file_tools import read_file
import os
import sys


"""
Return the inside content of a libraries directory.
"""
def get_libs_inside_content(lib_original_dir: str):
    lib_dir_content = os.listdir(lib_original_dir)

    lib_list = {}
    for lib in lib_dir_content:
        lib_dir = lib_original_dir + lib
        if not os.path.isdir(lib_dir):
            print(f"Warning: Can't open '{lib}' folder.")
            continue
        content = os.listdir(lib_dir)
        lib_list[lib] = content
    return lib_list


def get_lib_tests(path, path_content):
    if "tests" not in path_content:
        return []
    full_path = path + "tests/"
    tests = os.listdir(full_path)
    try:
        prototypes = []
        for test in tests:
            current_prototypes = get_cleaned_function_prototypes(full_path + test)
            for i in range(len(current_prototypes)):
                current_prototypes[i] = current_prototypes[i].split("(")[1].split(",")[0]
            prototypes.append(current_prototypes)
    except Exception as e:
        return tests

    return prototypes


def get_lib_headers(path, path_content):
    if "headers" not in path_content:
        return []
    headers = os.listdir(path + "headers/")
    return headers


def get_all_prototypes(lib_dir):
    print(lib_dir)
    return read_file(lib_dir + "content.txt", exit=False)

def get_lib_info(lib, content):
    default_lib = {
        "content": None,
        "desc": None,
        "versions": {}
    }
    lib_dir = LIBDIR + lib + "/"
    print(lib, content)
    print(lib_dir)
    if "content.txt" in content:
        default_lib["content"] = get_all_prototypes(lib_dir)
    else:
        print(f"Warning: Missing 'content.txt' file in '{lib}' library.")
    if "desc.txt" in content:
        default_lib["desc"] = read_file(lib_dir + "desc.txt", exit=False)
    else:
        print(f"Warning: Missing 'desc.txt' file in '{lib}' library.")
    return default_lib


def reload_libs():
    lib_list = get_libs_inside_content(LIBDIR)

    libs = {}
    for lib in lib_list:
        current_lib = get_lib_info(lib, lib_list[lib])
        lib_dir = LIBDIR + lib + "/"
        for version in lib_list[lib]:
            current_path = lib_dir + version
            if not os.path.isdir(current_path):
                continue # Possibly get the changelog detection here
            content = os.listdir(current_path)
            current_lib["versions"][version] = {}
            current_lib["versions"][version]["changelog"] = ""
            current_lib["versions"][version]["tests"] = get_lib_tests(current_path + "/", content)[0]
            current_lib["versions"][version]["headers"] = get_lib_headers(current_path + "/", content)
        libs[lib] = current_lib
    print(libs)
    save_to_json(libs, BASEDIR + "libs.json")


def reload_command(args):
    if len(args) >= 1 and ("help"in args or "--help" in args):
        print("Usage: 3pf reload\n")
        print("Reload 3PF packets configuration.")
        print("\nFlags:")
        print("  --help\tDisplay this help message.")
        sys.exit(0)

    reload_libs()



def display_libs(options):
    libs = load_from_json(BASEDIR + "libs.json")
    if libs == {}:
        print("Error: Missing library configuration, please consider reload or reinstall 3PF.")
        sys.exit(1)
    custom_libs = options.get("lib", [])
    print(f"3PF Available libs: {len(libs)}")
    if custom_libs != []:
        print(f"Selected {len(custom_libs)} librar{'y' if len(custom_libs) == 1 else 'ies'}: {', '.join(custom_libs)}")
    print('')
    for lib in libs:
        if not (lib in custom_libs or custom_libs == []):
            continue
        desc = libs[lib].get("desc", "Custom packet")
        desc = desc if desc != None else "Custom packet"
        print(f"- {lib}: {desc}.")
        if options["detail"] == False:
            continue
        print(f"\tAvailable functions:")
        prototypes = libs[lib]["content"].split("\n")
        if prototypes[-1] == "":
            prototypes = prototypes[:-1]
        for function in prototypes:
            print(f"\t\t{function}")
        print(f"\tAvailable versions:")
        versions = libs[lib]["versions"]
        for version in versions:
            changelog = versions[version].get("changelog", "Custom version")
            changelog = changelog if changelog != "" else "Custom version"
            print(f"\t\t{version}: {changelog}")
            tests = versions[version].get('tests', [])
            print(f"\t\t  Available unit tests: {len(tests)}")
            print(f"\t\t  Headers: {len(versions[version].get('headers', []))}")

        print('')


def flagD(args, options) -> bool:
    options["detail"] = False
    return True

def handleVaArgArgument(current: str, options) -> bool:
    options["lib"].append(current)
    return True

def list_packets(args):

    options = {
        "detail": True,
        "lib": []
    }

    list_command = ArgumentArsenal("list", options, args=[],
      desc="List all installed packets.", additional=
      "You can also display more info about specific packets by naming them.")

    list_command.enable_va_arg("packets", handleVaArgArgument)
    list_command.make_flag("--no-detail", [], flagD, "Don't display packet details.")

    list_command.parse(args)
    try:
        display_libs(options)
    except Exception as e:
        print("Wrong configuration of 3PF, please consider reinstalling the client.")
        print(f"Error detail: {e}")
        sys.exit(2)

