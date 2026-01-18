#!/usr/bin/python3

from pppf.const import BASEDIR, LIBDIR
from pppf.tools.json_tools import save_to_json, load_from_json
from pppf.tools.prototype_parser import get_cleaned_function_prototypes
from pppf.tools.file_tools import read_file
import os
import sys


def print_usage():
    print("Usage: 3pf list [flags] [packets]\n\n")
    print("List all installed packets.")
    print("You can also display more info about specific packets by naming them.")
    print("\nFlags:")
    print("  --help\t\tDisplay help for list command.")
    print("  --no-detail\t\tDon't display packet details.")


def flag_detail(lib, args, i) -> bool:
    lib["detail"] = False

def flag_version(lib, args, i) -> bool:
    try:
        version = int(args[i + 1])
        lib["version"] = version
    except Exception as e:
        print(f"Error: '{args[i + 1]}' is not a valid number for flag version.")
        return False

def flag_lib(lib, args, i) -> bool:
    lib["lib"].append(args[i + 1])

flags = {
    "--no-detail": {
        "required": 0,
        "function": flag_detail
    }
}

def parse_arguments(args, libs):
    current_param = 0

    for i in range(len(args)):
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
                if func(libs, args, i) == False:
                    sys.exit(2)
                current_param = current.get("required", 0)

        elif args[i].startswith("--"):
            print(f"Error: '{args[i]}' unknown option in 'list' command.")
            sys.exit(1)

        else:
            libs["lib"].append(args[i])


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


def reload_libs(options):
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




def display_libs(options):
    libs = load_from_json(BASEDIR + "libs.json")
    if libs == {}:
        print("Error: Missing library configuration, please consider reload or reinstall 3PF.")
        sys.exit(1)
    print(options)
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


def list_packets(args):
    if len(args) >= 1 and ("help"in args or "--help" in args):
        print_usage()
        sys.exit(0)

    libs = {
        "detail": True,
        "lib": []
    }

    parse_arguments(args, libs)
    print(libs)
    try:
        reload_libs(libs)
        display_libs(libs)
    except Exception as e:
        print("Wrong configuration of 3PF, please consider reinstalling the client.")
        print(f"Error detail: {e}")
        sys.exit(2)

