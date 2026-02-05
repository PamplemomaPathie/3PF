#!/usr/bin/python3

from const import BASEDIR
from tools.json_tools import load_from_json
import sys


def load_libs():
    libs = load_from_json(BASEDIR + "libs.json")
    if libs == {}:
        print("\033[1;31mError\033[0m: Missing library configuration, please consider reload or reinstall 3PF.")
        sys.exit(1)
    return libs


