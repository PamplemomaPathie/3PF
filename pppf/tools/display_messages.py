#!/usr/bin/python3


def display_version(args):
    version_text = "3PF Packet Filter Version 0.0.1"
    print(version_text)


def display_help(args):

    help_text = """
\t3PF Packet Filter

\tUsage:
\t\t3pf <options>

\tOptions:
\t\thelp\t\tDisplay this help message
\t\t version\t\tShow the version of the tool
\t\t install\t\tInstall a packet
\t\t remove\t\tRemove a packet
 """

    print(help_text)