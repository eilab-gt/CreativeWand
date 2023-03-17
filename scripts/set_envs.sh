#!/bin/bash

# This script is used to set up environments, and is used by other scripts in this directory.

eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"

echo "Setting source directory..."

#BASEDIR=$(dirname "$0")
BASEDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo "$BASEDIR"
SOURCEDIR="$BASEDIR/../source/"
#echo $SOURCEDIR

export PYTHONPATH="$PYTHONPATH:$SOURCEDIR"

echo "PYTHONPATH is [$PYTHONPATH]"

echo "Activating conda env creative-wand-framework..."

conda activate creative-wand-framework