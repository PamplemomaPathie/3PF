#!/usr/bin/python3

from pppf.const import BASEDIR
from pppf.argument_arsenal import ArgumentArsenal
from pppf.tools.json_tools import load_from_json
import sys


def display_libs(options):
    libs = load_from_json(BASEDIR + "libs.json")
    if libs == {}:
        print("Error: Missing library configuration, please consider reload or reinstall 3PF.")
        sys.exit(1)
    custom_libs = options.get("lib", [])
    print(f"3PF Available libs: {len(libs)}")
    if custom_libs != []:
        print(f"Selected {len(custom_libs)} librar{'y' if len(custom_libs) == 1 else 'ies'}: {', '.join(custom_libs)}")
    print('')
    for lib in libs:
        if not (lib in custom_libs or custom_libs == []):
            continue
        desc = libs[lib].get("desc", "Custom packet")
        desc = desc if desc != None else "Custom packet"
        if desc[len(desc) - 1] == '.':
            desc = desc[:-1]
        print(f"- {lib}: {desc}.")
        if options["detail"] == False:
            continue
        links = libs[lib].get("links", None)
        if links != None and len(links) > 0:
            link_str = ""
            for link in links:
                link_str += ", " if link_str != "" else ""
                link_str += f"{link} v{links[link]}"
            print(f"\tDependencies: {link_str}")
        print(f"\tAvailable functions:")
        prototypes = libs[lib]["content"].split("\n")
        if prototypes[-1] == "":
            prototypes = prototypes[:-1]
        for function in prototypes:
            print(f"\t\t{function}")
        print(f"\tAvailable versions:")
        versions = libs[lib]["versions"]
        for version in versions:
            changelog = versions[version].get("changelog", "Custom version")
            changelog = changelog if changelog != "" else "Custom version"
            print(f"\t\t{version}: {changelog}")
            tests = versions[version].get('tests', [])
            print(f"\t\t  Available unit tests: {len(tests)}")
            print(f"\t\t  Headers: {len(versions[version].get('headers', []))}")

        print('')


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

