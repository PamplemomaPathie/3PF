#!/usr/bin/python3

from const import arguments
from tools.string_tools import get_similar
from tools.display_messages import display_help, display_version
from pppf.install_packet import install_packet
from pppf.list_packets import list_packets
from pppf.reload_packets import reload_command
from pppf.deploy_packet import deploy_packet
from pppf.remove_packets import remove_packets
from pppf.edit_packets import edit_packets
from pppf.pack_packets import pack_packets
from pppf.unpack_packets import unpack_packets
from pppf.update_packets import update_packets

arguments.get("help")["function"] = display_help
arguments.get("version")["function"] = display_version
arguments.get("install")["function"] = install_packet
arguments.get("deploy")["function"] = deploy_packet
arguments.get("list")["function"] = list_packets
arguments.get("reload")["function"] = reload_command
arguments.get("rm")["function"] = remove_packets
arguments.get("edit")["function"] = edit_packets
arguments.get("pack")["function"] = pack_packets
arguments.get("unpack")["function"] = unpack_packets
arguments.get("update")["function"] = update_packets

def parse_args(args):

    for arg in args:
        if arg in arguments:
            if "function" in arguments[arg]:
                arguments[arg]["function"](args[1:])
            return
        else:
            print(f"\033[1;31mError\033[0m: '\033[1m{arg}\033[0m' is not a valid command. See '\033[1m3pf --help\033[0m'.")
            similar = get_similar(arg, arguments)
            if similar != None:
                print(f"\033[1;36mNote: \033[33mPerhaps you were looking for \033[0m\033[1m'{similar}'\033[33m.\033[0m")
            return
