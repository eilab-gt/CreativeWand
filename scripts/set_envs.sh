#!/bin/bash

# This script is used to set up environments, and is used by other scripts in this directory.

eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"

echo "Setting source directory..."

BASEDIR=$(dirname "$0")
#echo "$BASEDIR"
SOURCEDIR="$BASEDIR/../source/"
#echo $SOURCEDIR

export PYTHONPATH="$PYTHONPATH:$SOURCEDIR"

echo "PYTHONPATH is [$PYTHONPATH]"

echo "Activating conda env..."

conda activate creative-wand