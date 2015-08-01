#!/bin/bash

python get-pip.py > ../logs/pipinstall.txt
python setup.py install > ../logs/setuppyinstall.txt

cp main.py main.command
chmod +x main.command

ln -s "$PWD"/main.command /Applications/CanvasHelper.command

find ../. -exec chmod 777 {} \;
