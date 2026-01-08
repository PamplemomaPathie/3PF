#!/usr/bin/python3

from pppf.args_parsing import parse_args
import sys

def launch():
    print("Launching 3PF Packet Filter...")

    parse_args(sys.argv[1:])