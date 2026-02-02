#!/usr/bin/python3

from pppf.argument_arsenal import ArgumentArsenal
from pppf.const import LIBDIR
from pppf.list_packets import load_libs
from pppf.reload_packets import reload_libs
import os

def remove_directory(path):
    if not os.path.exists(path):
        return
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except Exception:
                continue
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
            except Exception:
                continue
    try:
        os.rmdir(path)
    except Exception:
        return

def remove_packets(args):

    remove_command = ArgumentArsenal("rm", [], args=["libName"],
      desc="Remove a library from 3PF.")

    remove_command.parse(args)
    name = remove_command.get_args()[0]

    libs = load_libs()
    if args[0] not in libs:
        print(f"\033[1;31mError\033[0m: '\033[1m{args[0]}\033[0m' is not a library.")
        return
    remove_directory(LIBDIR + name)
    reload_libs()
    print(f"\033[1;32mSuccessfully removed \033[0m\033[1m'{name}'\033[1;32m library\033[0m!")
