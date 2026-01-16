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

def get_function_prototypes(content: str):
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

def main():
    file = sys.argv[1]
    prototypes = get_function_prototypes(read_file(file))
    for func in prototypes:
        print(func)
        print("====")

if __name__ == "__main__":
    main()
