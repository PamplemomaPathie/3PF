#!/usr/bin/python3

from pppf.argument_arsenal import ArgumentArsenal
from pppf.list_packets import load_libs
from pppf.reload_packets import reload_libs
import os


def edit_packets(args):

    remove_command = ArgumentArsenal("edit", [], args=["libName"],
      desc="Edit library informations.")

    remove_command.parse(args)
    name = remove_command.get_args()[0]

    libs = load_libs()
    if args[0] not in libs:
        print(f"\033[1;31mError\033[0m: '\033[1m{args[0]}\033[0m' is not a library.")
        return


    reload_libs()
    print(f"\033[1;32mSuccessfully edited \033[0m\033[1m'{name}'\033[1;32m library\033[0m!")
