#! /usr/bin/env bash
## shortcut to start screen with the desired .screenrc file

PROFILE=${1:?"You must supply the profile name"}
NAME=${2:?"You must supply a name for the screen session"}

screen -S ${NAME} -c /home/gabe/bin/screen/.screenrc-${PROFILE}




