#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from pppf.const import BASEDIR
from pppf.list_packets import load_libs
from pppf.reload_packets import reload_libs
import os

def make_archive(folder_path: str, output_zip: str):
    import shutil

    shutil.make_archive(output_zip, 'zip', folder_path)


def pack_packets(args):

    pack_command = ArgumentArsenal("pack", [], args=[],
      desc="Pack your 3PF libs in a simple zip file to share them.")

    pack_command.parse(args)

    libs = load_libs()
    reload_libs()

    output_file = "./3PF_pack"
    make_archive(BASEDIR, output_file)

    print(f"\033[1;32mSuccessfully packed \033[0m\033[1m{len(libs)} librar{'ies' if len(libs) > 1 else 'y'}\033[1;32m in \033[0m\033[1m'{output_file}.zip'\033[1;32m!")
