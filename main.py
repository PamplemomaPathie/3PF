#!/usr/bin/python3

from pppf.launch import launch
import sys

def main():

    if len(sys.argv) <= 1:
        from tools.display_messages import display_help
        display_help(sys.argv[1:])

    launch()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31mStopped.\033[0m")
        sys.exit(0)
