#!/bin/bash

source "set_envs_addon.sh"

# Parameters used to determine which addons to be run.
SERVICES="pnb"

cd ../source/CreativeWand/Addons/WebServer/ || exit

python AddonServer.py $SERVICES