#!/bin/bash

# I use this to copy new builds into a seperate directory for testing or deployment

<<<<<<< HEAD
rsync -av . ../chnewbuild --exclude=makebuild.sh --exclude=*.pyc --exclude=logs/*.txt --exclude=*.csv --exclude=*/sensitive.json
=======
rsync -av . ../chnewbuild --exclude=*.pyc --exclude=logs/*.txt --exclude=*.csv --exclude=*/sensitive.json
>>>>>>> refs/remotes/origin/master
