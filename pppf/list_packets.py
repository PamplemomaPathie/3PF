#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from const import BASEDIR
from tools.json_tools import load_from_json
from pppf.pppf_tools import load_libs, get_all_groups
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
    custom_libs = options["lib"]

    groups = {}
    for lib in libs:
        group = libs[lib].get("group", None)
        if group != None:
            if groups.get(group, None) == None:
                groups[group] = []
            groups[group].append(lib)

    if len(custom_libs) == 0:
        print(f"3PF Available groups: {len(groups)}")
        print(f"    Available libs: {len(libs)}")
        for group in groups:
            print("")
            print(f"- \033[1m{group}\033[0m - \033[1m{len(groups[group])}\033[0m packets.")
            for content in groups[group]:
                print(f"    \033[3m{content}\033[0m")
        print("\n\033[3mPlease give us a group/library name to get info about it.\033[0m")
    elif custom_libs[0] in groups:
        print(f"Selected \033[1m{custom_libs[0]}\033[0m group.")
        printed = 0
        for lib in libs:
            if libs[lib].get("group", None) == custom_libs[0]:
                if options["detail"] == True or printed == 0:
                    print("")
                printed += 1
                print_lib(lib, libs[lib], details=options["detail"])
    else:
        print(f"Selected {len(custom_libs)} librar{'y' if len(custom_libs) == 1 else 'ies'}: {', '.join(custom_libs)}")
        for lib in libs:
            if lib in custom_libs or custom_libs == []:
                print("")
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
      desc="List all installed packets and groups.", additional=
      "You can also display more info about specific packets by naming them.")

    list_command.enable_va_arg("group/packets", handleVaArgArgument)
    list_command.make_flag("--simple", [], flagD, "Don't display packet details.")

    list_command.parse(args)
    display_libs(options)
    try:
        print("", end='')
    except Exception as e:
        print("Wrong configuration of 3PF, please consider reinstalling the client.")
        print(f"Error detail: {e}")
        sys.exit(2)

