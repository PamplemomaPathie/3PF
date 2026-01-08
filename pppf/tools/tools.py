#!/usr/bin/python3

import subprocess


"""
Execute a bash command and return the result.

@param  command: The bash command to execute.
"""
def bash(command: str):
    return subprocess.run(command, shell=True, text=True, capture_output=True)