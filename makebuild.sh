#!/bin/bash

# I use this to copy new builds into a seperate directory for testing or deployment

rm -r ../CH-new_build
mkdir -p ../CH-new_build
mkdir ../CH-new_build/CanvasHelper
cd CanvasHelper
find . -name '*.py' -exec cp {} ../../CH-new_build/CanvasHelper/ \;
find . -name '*.sh' -exec cp {} ../../CH-new_build/CanvasHelper/ \;
cp devkey.json ../../CH-new_build/CanvasHelper/devkey.json
cd ..

find . -type d -exec mkdir -p ../CH-new_build/{} \;

rm -r ../CH-new_build/setup.app

find . -name '*.app' -exec cp -rp {} ../CH-new_build/ \;
#cp -rp setup.app ../CH-new_build/setup.app


cp README.md ../CH-new_build/README.md

#zip -r ../CanvasHelper.zip ../CH-new_build