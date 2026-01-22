#!/usr/bin/python3

#from pppf.const import BASEDIR, LIBDIR
#from pppf.tools.json_tools import save_to_json, load_from_json
#from pppf.tools.file_tools import read_file
import os
import sys

from shutil import get_terminal_size

term_size = get_terminal_size().columns - 4

"""
Prints an error message.

@param message: The message to be displayed.
"""
def error(message: str):
    print(f"Error: {message}")
    sys.exit(1)


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
@param args: A list of arguments that the command will take.
@param desc: Description of the command.
@param flags: Dictionary of the flags with at least:
    - "--flag_name"
      - "description"
"""
def generate_helper(name: str, args, desc: str, flags):
    global term_size

    usage = f"Usage: 3pf {name}"
    current_size = len(usage)
    for arg in args:
        current = f" <{arg}>"
        current_size += len(current)
        if current_size > term_size:
            usage += "\n  "
            current_size = 2
        usage += current
    usage += " [flags]\n"
    print(usage)
    del usage

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
        args = [],                  # Argument given to the command
        helper: str = None,         # Optional help message for '--help'
        desc: str = None            # Optional desc for auto-generated '--help'
    ):
        self._name = command
        self._options = options
        self._helper = helper
        self._desc = desc if desc else "No description provided."
        self._args = args

        self._flags = []

    """ Print usage message """
    def _print_usage(self):
        if self._helper != None:
            print(self._helper)
            return;
        generate_helper(
            self._name,
            self._args,
            self._desc,
            self._flags
        )


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


    def parse_argument(self, args):
        print(args)
        required_args = len(self._args)
        if (len(args) < required_args):
            print(f"{self._name}: Not enough arguments.")
            self._print_usage()
            sys.exit(1)

        args_output = []
        for i in range(required_args):
            args_output.append(args[i])
        current_i = 0
        for i in range(required_args, len(args)):
            if current_i > 0:
                current_i -= 1; continue
            found = False
            for flag in self._flags:
                if args[i] == flag["name"]:
                    if flag["required"] + i + 1 > len(args):
                        error(f"'{args[i][2:]}' flag requires {flag['required']} parameter(s).")
                    found = True
                    current_i = flag["required"]
                    print("Found flag:", args[i])
                    trimmed_args = args[i + 1:]
                    trimmed_args = trimmed_args[:current_i]
                    if flag["function"](trimmed_args, self._options) == False:
                        error(f"Invalid parameter(s) in '{args[i][2:]}' flag.")
                    break;

            if found == False:
                print("Invalid flag:", args[i])


def test(args, options) -> bool:
    print("CALLING FUNCTION, ", args)
    return True;

make = ArgumentArsenal("make", {}, args=["object", "size"], desc="baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba THIS IS A VERY LONG DESCRIPTION oh my freaking god blud WHY ARE YOU SAYING SO MUCH STUFFF");
make.make_flag("--version", ["name", "num"], test, "Check VERSION")
make.make_flag("--pathie", [], test, "On Off to see the real version of pathie.")
make.make_flag("--nononoBlud", ["GoofyGuy", "PenisSize", "Secret Santa Argument"], test, "Silly description")
#make._print_usage()
make.parse_argument(sys.argv[1:])
