#!/usr/bin/python3

from const import arguments


def display_version(args):
    version_text = "3PF Packet Filter Version 0.1.3"
    print(version_text)


def display_help(args):

    help_text = """3PF Packet Filter

Usage:
  3pf <command>

Available Commands:
"""
    for arg_name, arg_info in arguments.items():
        help_text += f"  {arg_name}{' ' * (7 - len(arg_name))}\t{arg_info.get('description', '')}\n"

    print(help_text)
    print('Use "3pf <command> --help" for more information about a command.')
