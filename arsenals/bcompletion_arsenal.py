#!/usr/bin/python3



class BCompletionArsenal:

    def __init__(self, name: str):
        self._name = name
        self._commands = {}

    def make_args(self, name: str, args, files: bool = False):
        flags = [" ", "--help"] + args
        self._commands[name] = flags
        self._commands[name] = {
            "flags": flags,
            "files": files
        }

    def export(self) -> str:
        func_name = f"_{self._name}_completion"

        lines = [
            f"{func_name}() {{",
            "    local cur prev words cword",
            "    _init_completion -n : || return",
            "",
            f"    local commands=\"{' '.join(self._commands.keys())}\"",
            "",
            "    if [[ $cword -eq 1 ]]; then",
            "        COMPREPLY=( $(compgen -W \"$commands\" -- \"$cur\") )",
            "        return",
            "    fi",
            "",
            "    case \"${words[1]}\" in",
        ]

        for cmd, info in self._commands.items():
            flags_str = " ".join(info["flags"])
            if info["files"]:
                lines.extend([
                    f"        {cmd})",
                    "            if [[ \"$cur\" == -* ]]; then",
                    f"                COMPREPLY=( $(compgen -W \"{flags_str}\" -- \"$cur\") )",
                    "            else",
                    "                COMPREPLY=()",
                    "            fi",
                    "            COMPREPLY+=( $(compgen -f -- \"$cur\") )",
                    "            ;;",
                ])
            else:
                lines.extend([
                    f"        {cmd})",
                    "            if [[ \"$cur\" == -* ]]; then",
                    f"                COMPREPLY=( $(compgen -W \"{flags_str}\" -- \"$cur\") )",
                    "            else",
                    "                COMPREPLY=()",
                    "            fi",
                    "            ;;",
                ])

        lines.extend([
            "    esac",
            "}",
            "",
            f"complete -F {func_name} {self._name}",
        ])

        return "\n".join(lines)


