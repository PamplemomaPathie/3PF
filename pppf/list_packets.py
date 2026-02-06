#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from const import BASEDIR
from tools.json_tools import load_from_json
from pppf.pppf_tools import load_libs
import sys


def print_lib(name: str, lib, details: bool = True):
    desc = lib.get("desc", None)
    desc = desc if desc != None else "Custom packet"
    if desc[len(desc) - 1] == '.':
        desc = desc[:-1]

    print(f"- {name}: {desc}.")
    if details == False:
        return

    links = lib.get("links", None)
    if links != None and len(links) > 0:
        link_str = ""
        for link in links:
            link_str += ", " if link_str != "" else ""
            link_str += f"{link} v{links[link]}"
        print(f"\tDependencies: {link_str}")
    print(f"\tGroup: {lib.get('group', 'no group')}")

    versions = lib["versions"]
    print(f"\tAvailable versions:")
    for version in versions:
        changelog = versions[version].get("changelog", "")
        changelog = changelog if changelog != "" else "Custom version"
        print(f"\t   {version}: {changelog}")
        prototypes = versions[version]["content"].split("\n")
        print(f"\t     Available functions:")
        if prototypes[-1] == "":
            prototypes = prototypes[:-1]
        for function in prototypes:
            print(f"\t    \t{function}")
        tests = versions[version].get('tests', [])
        print(f"\t     Available unit tests: {len(tests)}")
        print(f"\t     Headers: {len(versions[version].get('headers', []))}")
    print('')


def display_libs(options):
    libs = load_libs()
    custom_libs = options.get("lib", [])
    print(f"3PF Available libs: {len(libs)}")
    if custom_libs != []:
        print(f"Selected {len(custom_libs)} librar{'y' if len(custom_libs) == 1 else 'ies'}: {', '.join(custom_libs)}")
    print('')
    for lib in libs:
        if not (lib in custom_libs or custom_libs == []):
            continue
        print_lib(lib, libs[lib], details=options["detail"])


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
    list_command.make_flag("--simple", [], flagD, "Don't display packet details.")

    list_command.parse(args)
    try:
        display_libs(options)
    except Exception as e:
        print("Wrong configuration of 3PF, please consider reinstalling the client.")
        print(f"Error detail: {e}")
        sys.exit(2)

