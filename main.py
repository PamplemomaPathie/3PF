#!/usr/bin/python3

from pppf.launch import launch
import sys

def main():

    if len(sys.argv) <= 1:
        from pppf.tools.display_help import display_help
        display_help()

    launch()


if __name__ == "__main__":
    main()