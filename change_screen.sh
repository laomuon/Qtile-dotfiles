#!/bin/sh
## Define screen ouputs and their positon
if ! (xrandr | grep "^HDMI-1" | grep "disconnected")
then
    xrandr --output HDMI-1 --primary --left-of eDP-1 --auto
else
    xrandr --output DP-2 --primary --left-of eDP-1 --auto
fi
