#!/bin/bash
cd  /home/nbeasley/game/lightupGame/
git pull

/usr/bin/python3 /home/nbeasley/game/lightupGame/gameManager.py  /boot/gameConfig.ini &
