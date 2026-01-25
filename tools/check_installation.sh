#!/bin/bash

BASE_DIR=".3pf"
LIBS_DIR="$BASE_DIR/libs"

error() {
    echo -e "\e[1m\e[31mError: $1\e[0m"
    exit 1
}

warn() {
    echo -e "\e[1m\e[35mWarn: $1\e[0m"
}


[[ -d "$BASE_DIR" ]] || error "3pf is not installed."
[[ -f "$BASE_DIR/libs.json" ]] || error "3pf libraries statuses are missing."
[[ -d "$LIBS_DIR" ]] || error "3pf libraries weren't initialized."


for lib in "$LIBS_DIR"/*; do
    [[ -d "$lib" ]] || continue

    lib_name="$(basename "$lib")"

    [[ -f "$lib/desc.txt" ]] || warn "Missing lib $lib_name description."
    [[ -f "$lib/content.txt" ]] || warn "Missing lib $lib_name content description."

    for version in "$lib"/*; do
        [[ -d "$version" ]] || continue

        folder_name="$(basename "$version")"

        if [[ "$folder_name" != 0 && "$folder_name" != 1 ]]; then
            [[ -f "$version/changelog.txt" ]] || \
                error "Missing $lib_name changelog for version $version."
        fi
    done
done

echo -e "\e[1m\e[32mAll libraries are valid.\e[0m"

