#!/bin/bash

# If cordova does not exist, install it
if ! command -v cordova >/dev/null; then
    npm install -g cordova
fi

# Install cordova platforms and plugins
rm -rf ./node_modules ./platforms ./plugins
cordova platform add ios
cordova prepare

npm run build
cordova run browser
