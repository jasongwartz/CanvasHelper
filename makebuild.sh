#!/bin/bash

# I use this to copy new builds into a seperate directory for testing or deployment

rsync -av . ../chnewbuild --exclude=makebuild.sh --exclude=*.pyc --exclude=logs/*.txt --exclude=*.csv --exclude=*/sensitive.json