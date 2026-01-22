#!/usr/bin/python3

#from pppf.const import BASEDIR, LIBDIR
#from pppf.tools.json_tools import save_to_json, load_from_json
#from pppf.tools.file_tools import read_file
import os
import sys

from shutil import get_terminal_size

term_size = get_terminal_size().columns - 4

"""
Return a custom display of a flag.

@param flags: an object with at least:
    - "name"
    - "args": ["argument1", "argument2", ...]
    - "desc"
"""
def get_flagdisplay(flag) -> str:
    global term_size
    args = flag["args"]
    desc = flag["desc"]

    result = f"  {flag['name']}"
    current_size = len(result)
    for arg in args:
        current = f" <{arg}>"
        current_size += len(current)

        if current_size > term_size - 2:
            result += "\n    "
            current_size = 4
        result += current

    result += "\n      "
    for i in range(1000):
        if len(desc) < term_size - 6:
            result += f"  {desc}\n"
            break;
        result += f"  {desc[:term_size - 6]}\n"
        desc = desc[term_size - 6:]
    return result


"""
Generate a helper of a command automatically based on the current flags.

@param name: name of the command.
@param desc: Description of the command.
@param flags: Dictionary of the flags with at least:
    - "--flag_name"
      - "description"
"""
def generate_helper(name: str, desc: str, flags):
    global term_size

    print(f"Usage: 3pf {name}\n") # Need to find a way to be customisable

    for i in range(1000):
        if len(desc) < term_size:
            print(f"  {desc}")
            break;
        print(f"  {desc[:term_size]}")
        desc = desc[term_size:]

    print("\nFlags:\n")
    print("  --help\n      Display this help message.\n")
    for flag in flags:
        required = flag.get('required', 0)
        print(get_flagdisplay(flag))


class ArgumentArsenal:
    """ Initialize the Argument parser """
    def __init__(self,
        command: str,               # Command name
        options,                    # Option you're passing to store the arguments
        helper: str = None,         # Optional help message for '--help'
        desc: str = None            # Optional desc for auto-generated '--help'
    ):
        self._name = command
        self._options = options
        self._helper = helper
        self._desc = desc

        self._flags = []

    """ Print usage message """
    def _print_usage(self):
        if self._helper != None:
            print(self._helper)
            return;
        generate_helper(self._name, self._desc if self._desc else "", self._flags)


    """ Create a custom flag for the command """
    def make_flag(self,
        name: str,                      # Name of the flag ex: '--flag'
        required_arguments,             # List of all the arguments
        function_called,                # The function that will be called when flag
                                            # must be 'bool func(args, options)'
        desc: str = "No description."   # Optional desc for auto-generated '--help'
    ):
        for flag in self._flags:
            if name == flag["name"]:
                print(f"{self._name}: flag '{name}' already registered.")
                return

        new_flag = {
            "name": name,
            "args": required_arguments,
            "required": len(required_arguments),
            "function": function_called,
            "desc": desc
        }
        self._flags.append(new_flag)

    def _print_flags(self):
        print(self._name, self._flags)


def test(args, options) -> bool:
    return True;

make = ArgumentArsenal("make", {}, desc="baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba THIS IS A VERY LONG DESCRIPTION oh my freaking god blud WHY ARE YOU SAYING SO MUCH STUFFF");
make.make_flag("--version", ["name", "num"], test, "Check VERSION")
make.make_flag("--pathie", [], test, "On Off to see the real version of pathie.")
make.make_flag("--nononoBlud", ["GoofyGuy", "PenisSize", "Secret Santa Argument"], test, "Silly description")
make._print_flags()
make._print_usage()
