#!/usr/bin/python3

import sys

CONST_FOLDER = "../const"

"""

Signal output meaning :

0 -> Simple quit, user canceled/ everything is good
1 -> Error occured in the checking
2 -> User wants a Full Reinstall
3 -> User wants a Soft Reinstall (Keep libs)

"""

def send_reinstall_signal(message: str):
    reinstall_response = input(message + "\n(y/n) >>> ")
    if reinstall_response.strip().lower() == "y":
        print("Would you like a complete reinstall or do you wish to keep your libraries?")
        print("1. Complete Reinstall")
        print("2. Keep Libraries")
        print("3. Cancel")
        a = input("(1-3) >>> ")
        if a == "1":
            sys.exit(2)
        elif a == "2":
            sys.exit(3)
        else:
            sys.exit(0)
    sys.exit(0)


def read_file(filename: str):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"No file {filename}.")
        sys.exit(1)
    return content


def get_const_info(filename: str):
    content = read_file(filename)

    return content.split("\n")


def check_install(filename: str, settings):
    content = read_file(filename)

    user_config = content.split("\n")
    if len(user_config) <= 0 or len(settings) <= 0 or not user_config[0].startswith("version:"):
        print("CheckInstall: Your configuration doesn't match the standard one,")
        send_reinstall_signal("would you like to reinstall 3PF?")
    if user_config[0] != settings[0]:
         print("CheckInstall: Old version detected.")
         send_reinstall_signal("Would you like to reinstall 3PF to the newest version?")
    print("Your version is up to date.")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} <config-file>")
        sys.exit(0)

    settings = get_const_info("/".join(sys.argv[0].split("/")[:-1]) + ("/" if '/' in sys.argv[0] else "") + CONST_FOLDER) # Find const file depending on argv[0]
    try:
        check_install(sys.argv[1], settings)
    except KeyboardInterrupt as ki:
        print("Interrupted.")
        sys.exit(0)
