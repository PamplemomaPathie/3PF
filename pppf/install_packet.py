#!/usr/bin/python3

from pppf.const import BASEDIR
from pppf.argument_arsenal import ArgumentArsenal
import sys



def flag_tests(args, options) -> bool:
    options["unit-tests"] = True
    return True

def flag_version(args, options) -> bool:
    try:
        val = int(args[0])
    except ValueError:
        print("No version number provided after '--version'.")
        return False
    options["version"] = args[0]
    return True

def flag_nodeps(args, options) -> bool:
    options["dependencies"] = False
    return True



def install_packet(args):

    options = {
        "unit-tests": False,
        "version": 0, # 0 for latest version
        "dependencies": True
    }

    deploy_command = ArgumentArsenal("install", options,
        args=["packet-name", "dest"],
        desc="Install a <packet-name> packet to a <dest> directory.",
        additional="")

    deploy_command.make_flag("--test", [], flag_tests,
        "Install packet with its unit test files.")
    deploy_command.make_flag("--version", ["version"], flag_version,
        "Install a specific version of a packet.")
    deploy_command.make_flag("--no-dependencies", [], flag_nodeps,
        "Install packet without its dependencies.")

    deploy_command.parse(args)

    user_args = deploy_command.get_args()
    name = user_args[0]
    dest = user_args[1]

    if options["version"] == 0:
        options["version"] = options["version"] # REMINDER TO SET TO LAST VERSION
    print(options)

