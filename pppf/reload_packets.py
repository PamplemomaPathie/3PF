#!/usr/bin/python3

from pppf.const import BASEDIR, LIBDIR
from pppf.argument_arsenal import ArgumentArsenal
from pppf.tools.json_tools import save_to_json
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
    return read_file(lib_dir + "content.txt")

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
        default_lib["desc"] = read_file(lib_dir + "desc.txt")
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

    reload = ArgumentArsenal("reload", [], args=[],
        desc="Reload 3PF packets configuration.")

    reload.parse(args)

    reload_libs()
