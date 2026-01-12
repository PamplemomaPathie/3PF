#!/usr/bin/bash

readonly BASEDIR=./.3pf/



if [ -f $BASEDIR/config ]; then

    echo "3PF is already installed on this computer, verifying installation..."
    python3 ./tools/check_3pf_install.py $BASEDIR/config
    readonly VERSION_CHECKING_SIGNAL=$(echo $?)

    if [ $VERSION_CHECKING_SIGNAL -eq 0 ]; then
        exit 0
    elif [ $VERSION_CHECKING_SIGNAL -eq 2 ]; then
        echo "Launching Full Reinstall.."
        rm -rf $BASEDIR
    elif [ $VERSION_CHECKING_SIGNAL -eq 3 ]; then
        echo "Launching Reinstall..."
        rm -f $BASEDIR/config
    else
        exit 0
    fi
fi


echo "Installing 3PF..."


# ===== Init Base subfolders ===== #

mkdir -p $BASEDIR
mkdir -p $BASEDIR/libs/

touch $BASEDIR/config
echo $(cat const) > $BASEDIR/config

