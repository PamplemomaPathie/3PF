#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from pppf.const import BASEDIR, LIBDIR
from tools.json_tools import save_to_json, load_from_json
from tools.prototype_parser import get_cleaned_function_prototypes
from tools.file_tools import read_file
import os


def warning_print(content: str, enable_printing: bool):
    if enable_printing:
        print(f"\033[1;35mWarning\033[0m: {content}")

"""
Return the inside content of a libraries directory.
"""
def get_libs_inside_content(lib_original_dir: str):
    lib_dir_content = os.listdir(lib_original_dir)

    lib_list = {}
    for lib in lib_dir_content:
        lib_dir = lib_original_dir + lib
        if not os.path.isdir(lib_dir):
            warning_print(f"Can't open '{lib}' folder.")
            continue
        content = os.listdir(lib_dir)
        lib_list[lib] = content
    return lib_list


def get_lib_tests(path, path_content):
    if "tests" not in path_content:
        return [[]]
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
    return read_file(lib_dir + "content.txt")

def get_lib_info(lib, content, warnings_printing: bool):
    wp = warnings_printing
    default_lib = {
        "content": None,
        "desc": None,
        "links": None,
        "versions": {}
    }
    lib_dir = LIBDIR + lib + "/"
    if "content.txt" in content:
        default_lib["content"] = get_all_prototypes(lib_dir)
    else:
        warning_print(f"\033[1m{lib}\033[0m: Missing '\033[1mcontent.txt\033[0m' file.", wp)
    if "desc.txt" in content:
        default_lib["desc"] = read_file(lib_dir + "desc.txt")
    else:
        warning_print(f"\033[1m{lib}\033[0m: Missing '\033[1mdesc.txt\033[0m' file.", wp)
    if "details.json" in content:
        content = load_from_json(lib_dir + "details.json")
        default_lib["links"] = content
    else:
        warning_print(f"\033[1m{lib}\033[0m: Missing '\033[1mdetails.json\033[0m' file.", wp)
    return default_lib


def reload_libs(warnings: bool = False):
    lib_list = get_libs_inside_content(LIBDIR)

    libs = {}
    for lib in lib_list:
        current_lib = get_lib_info(lib, lib_list[lib], warnings)
        lib_dir = LIBDIR + lib + "/"
        for version in lib_list[lib]:
            current_path = lib_dir + version
            if not os.path.isdir(current_path):
                continue # Possibly get the changelog detection here
            content = os.listdir(current_path)
            current_lib["versions"][version] = {}
            current_lib["versions"][version]["changelog"] = read_file(current_path + "/changelog.txt")
            current_lib["versions"][version]["tests"] = get_lib_tests(current_path + "/", content)[0]
            current_lib["versions"][version]["headers"] = get_lib_headers(current_path + "/", content)
        libs[lib] = current_lib
    save_to_json(libs, BASEDIR + "libs.json")


def reload_command(args):

    reload = ArgumentArsenal("reload", [], args=[],
        desc="Reload 3PF packets configuration.")

    reload.parse(args)

    reload_libs(warnings=True)
    print(f"\033[1;32mReloaded your libraries successfully\033[0m!")
