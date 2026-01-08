#!/usr/bin/python3

from pppf.tools.display_messages import display_help, display_version
from pppf.install_packet import install_packet
from pppf.remove_packet import remove_packet


arguments = {
    "help": {
        "description": "Display this help message",
        "function": display_help
    },
    "version": {
        "description": "Show the version of the tool",
        "function": display_version
    },
    "install": {
        "description": "Install a packet",
        "function": install_packet
    },
    "remove": {
        "description": "Remove a packet",
        "function": remove_packet
    }
}


def parse_args(args):

    for arg in args:
        if arg in arguments:
            arguments[arg]["function"](args[1:])
            return
        else:
            print(f"Unknown argument: {arg}")
            display_help(args[1:])
            return