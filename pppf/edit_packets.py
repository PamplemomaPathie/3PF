#!/usr/bin/python3

from arsenals.argument_arsenal import ArgumentArsenal
from pppf.const import LIBDIR
from pppf.list_packets import load_libs, print_lib
from pppf.reload_packets import reload_libs
from tools.file_tools import write_to_file
from tools.json_tools import save_to_json, load_from_json
import os

def edit_desc(name: str, libs):
    print(f"\033[1mCurrent description\033[0m: '{libs[name]['desc']}'.")
    print("\033[1mPlease enter a new description for this lib.\033[0m")
    answer = input(">> \033[2mdesc\033[0m >> ")
    if answer == "exit":
        print("Exited.")
        return
    write_to_file(LIBDIR + name + "/desc.txt", answer);
    libs[name]['desc'] = answer
    print("\033[1;32mDescription updated\033[0m!")


def edit_links_add(name: str, libs):
    print("\033[1mPlease name the lib you want to link.\033[0m")
    lib = input(">> \033[2mlinks\033[0m >> \033[2madd\033[0m >> ").strip()

    while lib not in libs or lib == name:
        if lib == "exit":
            print("Exited.")
            return
        print(f"\033[1;35mWarning\033[0m: '{lib}' is not a valid lib.")
        print("\033[1mPlease name the lib you want to link.\033[0m")
        lib = input(">> \033[2mlinks\033[0m >> \033[2madd\033[0m >> ").strip()


    print("\033[1mNow specify the version you want to link.\033[0m")

    all_versions = [lib for lib in libs[lib]["versions"]]
    available_versions = ""
    for option in all_versions:
        available_versions += "" if available_versions == "" else ", "
        available_versions += "v" + option

    print(f"\033[1mAvailable versions\033[0m: {available_versions}.")
    version = input(f">> \033[2mlinks\033[0m >> \033[2madd\033[0m >> \033[2m{lib}\033[0m v").strip()

    while version not in all_versions:
        if version == "exit":
            print("Exited.")
            return
        print(f"\033[1;35mWarning\033[0m: '{version}' is not a valid version.")
        print("\033[1mPlease specify a valid version.\033[0m")
        print(f"\033[1mAvailable versions\033[0m: {available_versions}.")
        version = input(f">> \033[2mlinks\033[0m >> \033[2madd\033[0m >> \033[2m{lib}\033[0m v").strip()

    filepath = LIBDIR + name + "/" + "details.json"
    content = load_from_json(filepath)
    content[lib] = version
    save_to_json(content, filepath)
    libs[name]["links"][lib] = version
    print(f"\033[1;32mSuccessfully linked \033[0m\033[1m'{lib} v{version}'\033[1;32m to library\033[0m!")
    

def edit_links_rm(name: str, libs):
    print("\033[1mPlease name the link you want to remove.\033[0m")
    lib = input(">> \033[2mlinks\033[0m >> \033[2mrm\033[0m >> ").strip()

    while lib not in libs[name]['links']:
        if lib == "exit":
            print("Exited.")
            return
        print(f"\033[1;35mWarning\033[0m: '{lib}' is not a valid lib.")
        print("\033[1mPlease name the link you want to remove.\033[0m")
        lib = input(">> \033[2mlinks\033[0m >> \033[2mrm\033[0m >> ").strip()

    filepath = LIBDIR + name + "/" + "details.json"
    content = load_from_json(filepath)
    del content[lib]
    save_to_json(content, filepath)
    del libs[name]["links"][lib]
    print(f"\033[1;32mSuccessfully removed \033[0m\033[1m'{lib}'\033[1;32m link from library\033[0m!")

def edit_links(name: str, libs):

    options = {
        "add": edit_links_add,
        "rm": edit_links_rm
    }

    available_functions = ""
    for option in options:
        available_functions += "" if available_functions == "" else ", "
        available_functions += option

    while True:
        if len(libs[name]['links']) == 0:
            print("\033[3mCurrent links\033[0m: none.")
        else:
            link_str = ""
            for link in libs[name]['links']:
                link_str += ", " if link_str != "" else ""
                link_str += f"{link} v{libs[name]['links'][link]}"
            print(f"\033[3mCurrent links\033[0m: {link_str}")

        print(f"\033[3mAvailable commands\033[0m: {available_functions}, exit.")
        answer = input(">> \033[2mlinks\033[0m >> ").strip()
        if answer == "exit":
            print("Exited.")
            return
        founded = False
        for option in options:
            if answer == option:
                founded = True
                options[option](name, libs)
                return
        if founded == False:
            print(f"\033[1;35mWarning\033[0m: '{answer}' is not an available command.")

def edit_changelog(name: str, libs):
    pass

def edit_lib(name: str, libs):

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
                founded = True
                options[option](name, libs)
                break
        if founded == False:
            print(f"\033[1;35mWarning\033[0m: '{answer}' is not an available command.")


def edit_packets(args):

    edit_command = ArgumentArsenal("edit", [], args=["libName"],
      desc="Edit library informations.")

    edit_command.parse(args)
    name = edit_command.get_args()[0]

    libs = load_libs()
    if name not in libs:
        print(f"\033[1;31mError\033[0m: '\033[1m{name}\033[0m' is not a library.")
        return

    print(f"\033[1mYou're currently editing '{name}' library.\033[0m")
    print_lib(name, libs[name])
    edit_lib(name, libs)

    reload_libs()
    print(f"\033[1;32mSuccessfully edited \033[0m\033[1m'{name}'\033[1;32m library\033[0m!")
