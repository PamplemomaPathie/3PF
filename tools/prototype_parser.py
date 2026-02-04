#!/usr/bin/python3

import sys

from tools.file_tools import read_file

def get_py_prototypes(filename: str):
    content = read_file(filename, exit=True)
    result = content.split("\n")
    lines = result
    final_result = []

    result = [res.split("#")[0] for res in result]
    result = [res for res in result if len(res.strip()) != 0]

    for i in range(len(result)):
        if result[i].strip().startswith("def "):
            result[i] = result[i].rstrip()
        else:
            result[i] = result[i].strip()

    classes = [res.split("(")[0].strip("\n :") for res in result if res.strip().startswith("class ")]

    result = "\n".join(result)

    result = result.split("def ")

    result.pop(0)
    result = ["def " + res for res in result]
    for i in range(1, len(result)):
        result[i] = result[i - 1].split("\n")[-1] + result[i]

    for i in range(len(result)):
        tmp = result[i].split(":\n", 1)
        if len(tmp) > 0:
            result[i] = tmp[0].rstrip().replace("\n", " ").replace(" )", ")")

    for line in lines:
        for function in result:
            if function.split("(")[0] in line:
                final_result.append(function)
                break
        for class_prot in classes:
            if class_prot in line:
                final_result.append(class_prot)
                break
    return final_result


def get_c_prototypes(filename: str):
    content = read_file(filename, exit=True)
    result = content.split("\n}")

    for i in range(len(result)):
        tmp = result[i].split("{", 1)
        if len(tmp) > 0:
            result[i] = tmp[0].strip("\n ")

    tmp = result[0].split("\n\n")
    result[0] = tmp[len(tmp) - 1]

    result = result[:-1]

    for i in range(len(result)):
        if not result[i].startswith("static "):
             result[i] += ";"

    result = [res for res in result if res[-1:] == ';']
    return result


def get_function_prototypes(filename: str):
    filetype = filename.split(".")[-1:]

    if filename.endswith(".py"):
        return get_py_prototypes(filename)
    else:
        return get_c_prototypes(filename)

def clean_prototype(prototype: str):
    if prototype.strip().startswith("def "):
        return prototype

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
    prototypes = get_function_prototypes(file)
    for func in prototypes:
        print(func)
        print("====")

if __name__ == "__main__":
    main()
