#!/usr/bin/python3

#from pppf.const import BASEDIR, LIBDIR
#from pppf.tools.json_tools import save_to_json, load_from_json
#from pppf.tools.file_tools import read_file
import os
import sys

from shutil import get_terminal_size


"""
Generate a helper of a command automatically based on the current flags.

@param name: name of the command.
@param desc: Description of the command.
@param flags: Dictionary of the flags with at least:
    - "--flag_name"
      - "description"
"""
def generate_helper(name: str, desc: str, flags):
    size = get_terminal_size().columns - 4
    print(size, len(desc))
    print(f"Usage: 3pf {name}\n") # Needd to find a way to be customisable

    for i in range(1000):
        if len(desc) < size:
            print(f"  {desc}")
            break;
        print(f"  {desc[:size]}")
        desc = desc[size:]

    print("\nFlags:")
    print("  --help\t\tDisplay this help message.")
    for flag in flags:
        required = flags[flag].get('required', 0)
        print(f"  {flag}{' <>' * required}{'\t' * max(2 - int(required / 2), 0)}{flags[flag].get('desc', '')}")


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

        self._flags = {}

    """ Print usage message """
    def _print_usage(self):
        if self._helper != None:
            print(self._helper)
            return;
        generate_helper(self._name, self._desc if self._desc else "", self._flags)


    """ Create a custom flag for the command """
    def make_flag(self,
        name: str,                      # Name of the flag ex: '--flag'
        required_arguments: int,        # The required arguments after the flag
        function_called,                # The function that will be called when flag
                                            # must be 'bool func(args, options)'
        desc: str = "No description."   # Optional desc for auto-generated '--help'
    ):
        if name in self._flags:
            print(f"{self._name}: flag '{name}' already registered.")
            return

        self._flags[name] = {
            "required": required_arguments,
            "function": function_called,
            "desc": desc
        }

    def _print_flags(self):
        print(self._name, self._flags)


def test(args, options) -> bool:
    return True;

make = ArgumentArsenal("make", {}, desc="baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba THIS IS A VERY LONG DESCRIPTION oh my freaking god blud WHY ARE YOU SAYING SO MUCH STUFFF");
make.make_flag("--version", 2, test, "Check version")
make.make_flag("--pathie", 0, test, "On Off to see the real version of pathie.")
make._print_flags()
make._print_usage()
