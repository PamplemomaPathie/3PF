"""
json_tools.py
------------

This file contains json related tools function.
"""


"""
Ensure that the folder for the given file path exists.
If the directory does not exist, it will be created, including any
necessary parent directories.

@param filename: The full path to a file (e.g., 'data/actions.json').
"""
def create_folder(filename: str):
    from pathlib import Path

    folder = Path(filename).parent
    folder.mkdir(parents=True, exist_ok=True)


"""
Convert a string so it can be embedded in JSON.
Only the minimal set of escape sequences are handled.

@param s: The string to be computed.

Returns the json.
"""
def string_to_json(s: str) -> str:
    escape_map = {
        '\\': '\\\\',
        '"': '\\"',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
    }
    return '"' + ''.join(escape_map.get(ch, ch) for ch in s) + '"'


"""
Recursively convert a Python object into a JSON string.
Supports: dict, list/tuple, str, int/float, bool, None.

@param obj: The object that will be converted.
"""
def convert_to_json(obj) -> str:
    if obj is None:
        return "null"

    if isinstance(obj, bool):
        return "true" if obj == True else "false"

    if isinstance(obj, (int, float)):
        return str(obj)

    if isinstance(obj, str):
        return string_to_json(obj)

    if isinstance(obj, (list, tuple)):
        items = ", ".join(convert_to_json(item) for item in obj)
        return f"[{items}]"

    if isinstance(obj, dict):
        items = ", ".join(f"{convert_to_json(k)}: {convert_to_json(v)}" for k, v in obj.items())
        return f"{{{items}}}"

    return "null"


"""
Format an object into a pretty json string.

@param obj: The object you're trying to convert into json.

Returns a string of the json object.
"""
def format_json(obj, indent: int = 0, step: int = 2) -> str:

    spacer = " " * indent
    if obj is None or isinstance(obj, (bool, int, float)):
        return convert_to_json(obj)

    if isinstance(obj, str):
        return string_to_json(obj)

    if isinstance(obj, (list, tuple)):
        if not obj:
            return "[]"
        inner = []
        for item in obj:
            inner.append(format_json(item, indent + step, step))
        return "[\n" + ",\n".join(" " * (indent + step) + line for line in inner) + f"\n{spacer}]"

    if isinstance(obj, dict):
        if not obj:
            return "{}"
        inner = []
        for k, v in obj.items():
            inner.append(f"{string_to_json(k)}: {format_json(v, indent + step, step)}")
        return "{\n" + ",\n".join(" " * (indent + step) + line for line in inner) + f"\n{spacer}}}"

    return "{}"


"""
Save JSON-serialzable data to a file.

@param data: Any data strcuture that can be serialized to JSON (e.g dict, list).
@param filename: The path to the output JSON file.
"""
def save_to_json(data, filename: str):
    create_folder(filename)
    json_text = format_json(data, indent=0, step=2)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json_text)


"""
Convert a JSON string into a Python data structure.

@param text: The string of the content of your file.

Return an object that will be the result of the file computation.
"""
def json_to_python(text: str):
    text = text.replace("true", "True")
    text = text.replace("false", "False")
    text = text.replace("null", "None")

    try:
        return eval(text, {"__builtins__": None}, {})
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return []


"""
Load data to a JSON file.

@param filename: The Path to the JSON file to read.
@param display_error: Tells if an error is printed or not.

Returns the data loaded from the file.
"""
def load_from_json(filename: str):
    import json
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)
        return {}
