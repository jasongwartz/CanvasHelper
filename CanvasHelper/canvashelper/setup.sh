#!/bin/bash

python get-pip.py > ../logs/pipinstall.txt
python setup.py install > ../logs/setuppyinstall.txt

cp canvashelper.py canvashelper.command
chmod +x canvashelper.command

ln -s "$PWD"/canvashelper.command /Applications/CanvasHelper.command

find ../. -exec chmod 777 {} \;
