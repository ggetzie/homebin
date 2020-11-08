#! /usr/bin/env bash
## shortcut to start screen with the desired .screenrc file

PROFILE=${1:?"You must supply the profile name"}

screen -S ${PROFILE} -c /home/gabe/bin/screen/.screenrc-${PROFILE}




