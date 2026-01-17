#!/usr/bin/python3

import sys

def read_file(filename: str):
    try:
        with open(filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"No file {filename}.")
        sys.exit(1)
    return content

def get_function_prototypes(filename: str):
    content = read_file(filename)
    result = content.split("\n}") # end of a function body

    for i in range(len(result)):
        tmp = result[i].split("{", 1) # opening bracket of a function body
        if len(tmp) > 0:
            result[i] = tmp[0].strip("\n ") # keeping only first line (function prototype) & removing excess line feeds

    tmp = result[0].split("\n\n") # splitting first result (from the start of the file to the first function prototype)
    result[0] = tmp[len(tmp) - 1] # keeping only last line (first function's prototype)

    result = result[:-1] # removing last element (the line feed after the last function's closing bracket)

    for i in range(len(result)):
        if not result[i].startswith("static "):
             result[i] += ";" # adding semicolon at the end of each function prototype (unless function is static)

    result = [res for res in result if res[-1:] == ';'] # filtering prototypes to remove those without semicolon (since it means they're a static function)
    return result


def clean_prototype(prototype: str):
    parts = prototype.split("\n")
    in_prototype = False
    cleaned_prototype = []

    for line in parts:
        content = line.strip()

        if in_prototype:
            if content.startswith("//") or content.startswith("/*"):
                break
            cleaned_prototype.append(line)
            if content.endswith(')'):
                in_prototype = False
        elif content and not content.startswith("//") and not content.startswith("/*"):
            if '(' in content:
                cleaned_prototype.append(line)
                in_prototype = True

    return "\n".join(cleaned_prototype) if cleaned_prototype else None

def get_cleaned_function_prototypes(filename: str):
    prototypes = get_function_prototypes(filename)

    for i in range(len(prototypes)):
        prototypes[i] = clean_prototype(prototypes[i])

    return prototypes


def main():
    file = sys.argv[1]
    prototypes = get_cleaned_function_prototypes(file)
    for func in prototypes:
        print(func)
        print("====")

if __name__ == "__main__":
    main()
