#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from const import LIBDIR
from pppf.list_packets import load_libs
from pppf.remove_packets import remove_lib, remove_directory
from pppf.reload_packets import reload_libs
from tools.json_tools import load_from_json
import os


def unarchive(zip_file: str, output_folder: str):
    import shutil

    shutil.unpack_archive(zip_file, output_folder, format='zip')
    os.remove(zip_file)


def handle_conflicts(new_obj, current_obj):
    return len(new_obj["versions"]) > len(current_obj["versions"])


def copy_folder(folder: str, dest: str):
    import shutil

    shutil.copytree(folder, dest)


def merge_libs(new_libs, current_libs):
    result = []

    for lib in new_libs:
        if lib in current_libs:
            if handle_conflicts(new_libs[lib], current_libs[lib]) == True:
                print(f"\033[1;33mUpgraded \033[0m\033[1m'{lib}'\033[1m library to newest version.\033[0m")
                remove_lib(lib)
                result.append(lib)
        else:
            print(f"\033[1;32mInstalled \033[0m\033[1m'{lib}'\033[1m!\033[0m")
            result.append(lib)
    return result


def unpack_packets(args):

    unpack_command = ArgumentArsenal("unpack", [], args=["3PF_pack.zip"],
      desc="Unpack 3PF libs & merge them with your libs.")

    unpack_command.parse(args)
    pack = unpack_command.get_args()[0]
    if not os.path.exists(pack) or not pack.endswith(".zip"):
        print(f"\033[1;31mError\033[0m: '\033[1m{pack}\033[0m' is not a valid file.")
        return

    work_dir = ".3PF_tmp/"

    unarchive(pack, work_dir)
    new_libs = load_from_json(work_dir + "libs.json")
    current_libs = load_libs()

    lib_names = merge_libs(new_libs, current_libs)
    for name in lib_names:
        copy_folder(work_dir + "libs/" + name, LIBDIR + name)
    remove_directory(work_dir)

    reload_libs()
    print(f"\033[1;32mSuccessfully unpacked \033[0m\033[1m{len(new_libs)} librar{'ies' if len(new_libs) != 1 else 'y'}\033[1;32m from \033[0m\033[1m'{pack}'\033[0m!")
