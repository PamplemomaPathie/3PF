#!/usr/bin/python3

from pathlib import Path
home = str(Path.home())

BASEDIR = home + "/.3pf/"
LIBDIR = home + "/.3pf/libs/"

arguments = {
    "install": {
        "description": "Install a packet"
    },
    "deploy": {
        "description": "Deploy a lib"
    },
    "list": {
        "description": "List all available packets"
    },
    "reload": {
        "description": "Reload 3PF configuration."
    },
    "edit": {
        "description": "Edit packet informations."
    },
    "update": {
        "description": "Create a new version of a packet."
    },
    "rm": {
        "description": "Remove a lib."
    },
    "pack": {
        "description": "Pack your 3PF libs in a simple zip file to share them."
    },
    "unpack": {
        "description": "Unpack 3PF libs & merge them with your libs."
    },
    "version": {
        "description": "Show the version of 3PF"
    },
    "help": {
        "description": "Display this help message"
    }
}
