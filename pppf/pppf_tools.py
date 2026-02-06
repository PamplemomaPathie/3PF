#!/usr/bin/python3

from const import BASEDIR
from tools.json_tools import load_from_json
from tools.string_tools import get_similar
import sys


def load_libs():
    libs = load_from_json(BASEDIR + "libs.json")
    if libs == {}:
        print("\033[1;31mError\033[0m: Missing library configuration, please consider reload or reinstall 3PF.")
        sys.exit(1)
    return libs


def lib_not_found(name: str, libs):
    if name in libs:
        return False

    similar = get_similar(name, libs)

    print(f"\033[1;31mError\033[0m: '\033[1m{name}\033[0m' is not a library.")
    if similar != None:
        print(f"\033[1;36mNote: \033[33mPerhaps you were looking for \033[0m\033[1m'{similar}'\033[33m.\033[0m")

    return True


def get_all_groups(libs):
    groups = {}
    for lib in libs:
        group = libs[lib].get("group", None)
        if group != None:
            if groups.get(group, None) == None:
                groups[group] = []
            groups[group].append(lib)
    return groups
