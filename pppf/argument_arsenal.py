#!/usr/bin/python3

ITALIC="\033[3m"
RESET="\033[0m"

import os
import sys

from shutil import get_terminal_size

term_size = get_terminal_size().columns - 4

"""
Prints an error message.

@param reason: reason of the error.
@param message: The message to be displayed.
"""
def error(reason: str, message: str, exit: bool = True):
    global term_size

    print("\033[31m\033[1mError: \033[0m", end='\033[1m')
    print(reason, end='\033[0m' + (" " if reason != "" else ""))
    size = term_size - (len(reason) + 7)
    for i in range(1000):
        if len(message) < size:
            print(f"{message}")
            break;
        print(f"  {message[:size]}")
        message = message[size:]
    if (exit == True):
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
@param additional: Additional description.
@param flags: Dictionary of the flags with at least:
    - "--flag_name"
      - "description"
@param vaArg: Dictionary of potential vaArgs, either None, or at least:
    - "name": The name of the vaArg
    - "optional": Boolean to tell if the argument is optional.
"""
def generate_helper(name: str, args, desc: str, additional: str, flags, vaArg):
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
    usage += " [flags]"
    if vaArg != None:
        usage += " [" if vaArg["optional"] == True else " <"
        usage += vaArg["name"]
        usage += "]" if vaArg["optional"] == True else ">"
    usage += "\n"
    print(usage)
    del usage

    for i in range(1000):
        if len(desc) < term_size:
            print(f"  {desc}")
            break;
        print(f"  {desc[:term_size]}")
        desc = desc[term_size:]
    if additional != None:
        print(ITALIC, end='')
        for i in range(1000):
            if len(additional) < term_size:
                print(f"  {additional}")
                break;
            print(f"  {additional[:term_size]}")
            additional = additional[term_size:]
    print(RESET)

    print("Flags:\n")
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
        desc: str = None,           # Optional desc for auto-generated '--help'
        additional: str = None      # Optional additional description
    ):
        self._name = command
        self._options = options
        self._helper = helper
        self._desc = desc if desc else "No description provided."
        self._additional = additional
        self._args = args

        self._vaArg = None

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
            self._additional,
            self._flags,
            self._vaArg
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


    """ Enable variadic arguments for the command """
    def enable_va_arg(self, name: str, function, optional=True):
        self._vaArg = {
            "name": name,
            "function": function,
            "optional": optional
        }


    """ Parse all argument of a command """
    def parse(self, args):
        va_args = True if self._vaArg == None else self._vaArg["optional"]
        required_args = len(self._args)
        if (len(args) < required_args):
            error(f"{self._name} command: Not enough arguments.", "", exit=False)
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
            if args[i] == "--help":
                self._print_usage(); sys.exit(0)
            for flag in self._flags:
                if args[i] == flag["name"]:
                    if flag["required"] + i + 1 > len(args):
                        error("", f"'{args[i][2:]}' flag requires {flag['required']} parameter(s).")
                    found = True
                    current_i = flag["required"]
                    trimmed_args = args[i + 1:]
                    trimmed_args = trimmed_args[:current_i]
                    if flag["function"](trimmed_args, self._options) == False:
                        error("Invalid parameter(s)", f"in '{args[i][2:]}' flag.")
                    break;

            if found == False:
                if self._vaArg == None:
                    if args[i][:2] == '--':
                        error("Invalid flag:", f"'{args[i][2:]}'.")
                    error("Invalid option:", f"'{args[i]}'.")
                self._vaArg["function"](args[i], self._options)
                va_args = True
        if va_args == False:
            error(f"Additional argument(s) '{self._vaArg['name']}' required.", "")
        return self._options


if __name__ == "__main__":

    def test(args, options) -> bool: # Adds the arguments to option.
        options["lib"].append(args)
        return True;

    def sillyArgs(current: str, options) -> bool:
        options["lib"].append("Silly: " + current)
        return True

    options = {
        "lib": []
    }

    make = ArgumentArsenal("make", options, args=["object", "size"], desc="baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba baba THIS IS A VERY LONG DESCRIPTION oh my freaking god blud WHY ARE YOU SAYING SO MUCH STUFFF", additional="This is silly isn't it?");

    make.enable_va_arg("Silly", sillyArgs, optional=False)

    make.make_flag("--version", ["name", "num"], test, "Check VERSION")
    make.make_flag("--pathie", [], test, "On Off to see the real version of pathie.")
    make.make_flag("--nononoBlud", ["GoofyGuy", "PenisSize", "Secret Santa Argument"], test, "Silly description")
    options = make.parse(sys.argv[1:])

    print(options)
