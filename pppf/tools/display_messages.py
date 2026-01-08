#!/usr/bin/python3

from pppf.const import arguments


def display_version(args):
    version_text = "3PF Packet Filter Version 0.0.1"
    print(version_text)


def display_help(args):

    help_text = """
3PF Packet Filter

Usage:
\t3pf <options>

Options:
"""
    for arg_name, arg_info in arguments.items():
        help_text += f"\t{arg_name}\t{arg_info.get('description', '')}\n"

    print(help_text)