#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from const import BASEDIR
from pppf.pppf_tools import load_libs, lib_not_found
import sys


def flag_version(args, options) -> bool:
    print("Add detection here")
    options["version"] = args[0]
    return True


def install_packet(args):

    options = {
        "version": 0, # 0 for latest version
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

    if options["version"] == 0:
        options["version"] = options["version"] # REMINDER TO SET TO LAST VERSION
    print(options)

