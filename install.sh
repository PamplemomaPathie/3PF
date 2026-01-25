#!/bin/bash

BASE_DIR="$HOME/.3pf"
LIBS_DIR="$BASE_DIR/libs"

BINARY="3pf"

LOGLEVEL="warn"

show_help() {
    cat <<EOF
Usage: $0 [flags]

Flags:
  --help           Show this help message
  --loglevel=LEVEL Set log level (info, warn, error). Default to warn.
EOF
}


error() {
    echo -e "\e[1m\e[31m$1\e[0m"
    exit 1
}

error_print() {
    echo -e "\e[1m\e[31m$1\e[0m"
}

success() {
    echo -e "\e[1m\e[32m$1\e[0m"
}

warn() {
    [[ "$LOGLEVEL" == "info" || "$LOGLEVEL" == "warn" ]] && echo -e "\e[1m\e[35mWarn: $1\e[0m"
}

info_print() {
    [[ "$LOGLEVEL" == "info" ]] && echo -e "$1"
}



if [[ $# -ge 1 ]]; then
    arg="$1"
    if [[ "$arg" == "--help" ]]; then
        show_help
        exit 0
    fi

    if [[ "$arg" == --loglevel=* ]]; then
        level="${arg#*=}"
        if [[ "$level" == "info" || "$level" == "warn" || "$level" == "error" ]]; then
            LOGLEVEL="$level"
        fi
    fi
fi



install_3pf() {
    echo -e "\e[1mStarting insallation...\e[0m"

    [[ -f "$BINARY" ]] || error "Can't find $BINARY, please compile before installing."

    info_print "Creating base directory..."
    mkdir -p "$BASE_DIR"
    info_print "Creating library foler..."
    mkdir -p "$LIBS_DIR"

    info_print "Initializing libraries statuses."
    echo "{}" > "$BASE_DIR/libs.json" || error "Failed to create libraries statuses."

    info_print "Moving binary"
    mv $BINARY $BASE_DIR

    info_print "Installing alias for percistance."

    cat << EOF >> ~/.bashrc
# 3pf
if [ -d "$BASE_DIR" ] && [ -f "$BASE_DIR/$BINARY" ]; then
    alias 3pf="$BASE_DIR/$BINARY"
fi
EOF

    alias 3pf="$BASE_DIR/$BINARY"

    success "Installation finished."
}

reinstall_3pf() {
    info_print "Starting reinstallation..."
    info_print "Removing 3pf..."
    rm -rf "$BASE_DIR"
    info_print "Removed 3pf."
    info_print "Launching reinstallation..."
    install_3pf
}


check_installation() {
    install=0

    [[ -d "$BASE_DIR" ]] || { install=1; return $install; }
    [[ -f "$BASE_DIR/libs.json" ]] || { error_print "3pf libraries statuses are missing."; install=1; }
    [[ $install -eq 1 ]] && return $install
    [[ -d "$LIBS_DIR" ]] || { error_print "3pf libraries weren't initialized."; install=1; }
    [[ $install -eq 1 ]] && return $install

    for lib in "$LIBS_DIR"/*; do
        [[ -d "$lib" ]] || continue
        lib_name="$(basename "$lib")"

        info_print "Checking library: $lib_name"

        [[ -f "$lib/desc.txt" ]] || { warn "Missing $lib_name description."; install=1; }
        [[ -f "$lib/content.txt" ]] || { warn "Missing $lib_name content description."; install=1; }

        for version in "$lib"/*; do
            [[ -d "$version" ]] || continue
            folder_name="$(basename "$version")"

            if [[ "$folder_name" != 0 && "$folder_name" != 1 ]]; then
                [[ -f "$version/changelog.txt" ]] || { error_print "Missing $lib_name changelog for version $folder_name."; install=1; }
            fi
        done
    done

    if [[ $install -eq 0 ]]; then
        success "3pf already installed!"
    fi

    return $install
}

if ! check_installation; then
    echo -e "\e[1m3pf is not installed, installing program...\e[0m"
    reinstall_3pf
fi

