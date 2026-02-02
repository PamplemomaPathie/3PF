#!/usr/bin/python3

from pppf.argument_arsenal import ArgumentArsenal
from pppf.list_packets import load_libs, print_lib
from pppf.reload_packets import reload_libs
import os

def edit_desc(name: str):
    pass

def edit_links(name: str):
    pass

def edit_changelog(name: str):
    pass

def edit_lib(name: str):

    options = {
        "desc": edit_desc,
        "links": edit_links,
        "changelog": edit_changelog
    }

    available_functions = ""
    for option in options:
        available_functions += "" if available_functions == "" else ", "
        available_functions += option

    while True:
        print(f"\033[1mAvailable commands\033[0m: {available_functions}, exit.")
        answer = input(">> ")
        if answer == "exit":
            break
        founded = False
        for option in options:
            if answer == option:
                options[option](name)
                founded = True
                break
        if founded == False:
            print(f"\033[1;35mWarning\033[0m: '{answer}' is not an available command.")


def edit_packets(args):

    remove_command = ArgumentArsenal("edit", [], args=["libName"],
      desc="Edit library informations.")

    remove_command.parse(args)
    name = remove_command.get_args()[0]

    libs = load_libs()
    if name not in libs:
        print(f"\033[1;31mError\033[0m: '\033[1m{name}\033[0m' is not a library.")
        return

    print(f"\033[1mYou're currently editing '{name}' library.\033[0m")
    print_lib(name, libs[name])
    edit_lib(name)

    reload_libs()
    print(f"\033[1;32mSuccessfully edited \033[0m\033[1m'{name}'\033[1;32m library\033[0m!")
