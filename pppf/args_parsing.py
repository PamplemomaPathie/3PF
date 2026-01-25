#!/usr/bin/python3

from pppf.tools.display_messages import display_help, display_version
from pppf.install_packet import install_packet
from pppf.list_packets import list_packets
from pppf.reload_packets import reload_command
from pppf.deploy_packet import deploy_packet
from pppf.const import arguments

arguments.get("help")["function"] = display_help
arguments.get("version")["function"] = display_version
arguments.get("install")["function"] = install_packet
arguments.get("deploy")["function"] = deploy_packet
arguments.get("list")["function"] = list_packets
arguments.get("reload")["function"] = reload_command

def parse_args(args):

    for arg in args:
        if arg in arguments:
            if "function" in arguments[arg]:
                arguments[arg]["function"](args[1:])
            return
        else:
            print(f"Unknown argument: {arg}")
            display_help(args[1:])
            return
