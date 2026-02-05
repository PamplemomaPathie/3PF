#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from const import BASEDIR
from pppf.pppf_tools import load_libs, lib_not_found
import sys


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
        
    print("pulling version", version)

