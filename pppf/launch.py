#!/usr/bin/python3

from pppf.args_parsing import parse_args
import sys

def launch():
    parse_args(sys.argv[1:])
