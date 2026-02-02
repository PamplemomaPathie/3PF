#!/usr/bin/python3

from pppf.argument_arsenal import ArgumentArsenal
from pppf.list_packets import load_libs
from pppf.reload_packets import reload_libs
import os

def unarchive(zip_file: str, output_folder: str):
    import shutil

    shutil.unpack_archive(zip_file, output_folder, format='zip')


def unpack_packets(args):

    unpack_command = ArgumentArsenal("unpack", [], args=["3PF_pack.zip"],
      desc="Unpack 3PF libs & merge them with your libs.")

    unpack_command.parse(args)
    pack = unpack_command.get_args()[0]
    if not os.path.exists(pack) or not pack.endswith(".zip"):
        print(f"\033[1;31mError\033[0m: '\033[1m{pack}\033[0m' is not a valid file.")
        return
    libs = load_libs()

    unarchive(pack, ".3pf_cache/")
    reload_libs()
    print(f"\033[1;32mSuccessfully unpacked \033[0m\033[1m{len(libs)} librar{'ies' if len(libs) > 1 else 'y'}\033[1;32m from \033[0m\033[1m'{pack}'\033[0m!")
