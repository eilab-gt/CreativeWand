#!/bin/bash

source "set_envs.sh"

# Parameters used to customize experiments.
CONFIG=""

cd ../source/CreativeWand/Application/Deployment || exit

python StartExperiment.py $CONFIG