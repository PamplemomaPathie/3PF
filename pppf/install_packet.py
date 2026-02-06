#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from const import BASEDIR
from pppf.pppf_tools import load_libs, lib_not_found
import sys
import os



def complete_path(text, state):
    import glob
    expanded = os.path.expanduser(text)

    matches = glob.glob(expanded + '*')

    matches = [m + '/' if os.path.isdir(match) else match for match in matches]
    try:
        return matches[state]
    except IndexError:
        return None

def install_lib(name: str, version: str, path: str, lib):
    import readline
    readline.set_completer(complete_path)
    readline.parse_and_bind('tab: complete')

    tests = len(lib["versions"][version]["tests"])
    if tests > 0:
        print(f"\033[1m3PF found \033[33m{tests}\033[0m\033[1m tests in '{name} v{version}'\033[0m.")
        test_dir = input("Directory for tests (empty to ignore) >> ")

    headers = len(lib["versions"][version]["headers"])
    if headers > 0:
        print(f"\033[1m3PF found \033[33m{headers}\033[0m\033[1m headers in '{name} v{version}'\033[0m.")
        header_dir = input("Directory for headers (empty to ignore) >> ")


def flag_version(args, options) -> bool:
    options["version"] = args[0]
    return True


def install_packet(args):

    options = {
        "version": "1",
    }

    deploy_command = ArgumentArsenal("install", options,
        args=["packet-name", "dest"],
        desc="Install a <packet-name> packet to a <dest> directory.",
        additional="")

    deploy_command.make_flag("--version", ["version"], flag_version,
        "Install a specific version of a packet.")

    deploy_command.parse(args)

    user_args = deploy_command.get_args()
    name = user_args[0]
    dest = user_args[1]

    libs = load_libs()
    if lib_not_found(name, libs):
        return

    version = options["version"]
    if version not in libs[name]["versions"]:
        print(f"\033[1;31mError\033[0m: '\033[1m{name}\033[0m' has no versions '\033[1m{version}\033[0m'.")
        return

    print(f"\033[1;32mInstalling \033[0m\033[1m'{name}'\033[1;32m library\033[0m...")

    install_lib(name, version, dest, libs[name])

    print(f"\033[1;32mSuccessfully installed \033[0m\033[1m'{name}'\033[1;32m library\033[0m!")
