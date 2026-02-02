#!/usr/bin/python3

from pppf.bcompletion_arsenal import BCompletionArsenal

def handle_autocomplete():
    model = BCompletionArsenal("3pf")

    model.make_args("install", [])

    model.make_args("deploy", ["--test", "--link", "--header"], True)

    model.make_args("list", ["--simple"])

    model.make_args("reload", [])

    model.make_args("edit", [])

    model.make_args("rm", [])

    model.make_args("pack", [])

    model.make_args("unpack", [], True)

    model.make_args("version", [])

    model.make_args("help", [])

    result = model.export()
    print(result)


if __name__ == "__main__":
    handle_autocomplete()
