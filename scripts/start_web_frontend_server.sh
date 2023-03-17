#!/bin/bash

source "set_envs.sh"

cd ../web-frontend/web-interface || exit

npm install

npm run start