#!/bin/bash

source "set_envs.sh"

# Parameters used to customize experiments.
CONFIG="$*"

echo "Parameters: $CONFIG"

cd ../source/CreativeWand/Application/Deployment || exit

python StartExperiment.py $CONFIG