#!/bin/sh

# Two screens
if ! (xrandr | grep "^HDMI-1" | grep "disconnected")
then
    xrandr --output HDMI-1 --primary --left-of eDP-1 --auto
elif ! (xrandr | grep "^DP-1" | grep "disconnected")
  then
    xrandr --output DP-1 --primary --left-of eDP-1 --auto
elif ! (xrandr | grep "^DP-2" | grep "disconnected")
  then
    xrandr --output DP-2 --primary --left-of eDP-1 --auto
elif ! (xrandr | grep "^DP-3" | grep "disconnected")
  then
    xrandr --output DP-3 --primary --left-of eDP-1 --auto
elif ! (xrandr | grep "^DP-4" | grep "disconnected")
  then
    xrandr --output DP-4 --primary --left-of eDP-1 --auto
else
    xrandr --output DP-3 --off --output HDMI-1 --off --output DP-2 --off --output DP-1 --off --output DP-4 --off --output eDP-1 --primary --auto
fi

#############################################################################
#

# if ! (xrandr | grep "^HDMI-1" | grep "disconnected")
# then
#     xrandr --output HDMI-1 --primary --same-as eDP-1 --auto
# elif ! (xrandr | grep "^DP-1" | grep "disconnected")
#   then
#     xrandr --output DP-1 --primary --same-as eDP-1 --auto
# elif ! (xrandr | grep "^DP-2" | grep "disconnected")
#   then
#     xrandr --output DP-2 --primary --same-as eDP-1 --auto
# elif ! (xrandr | grep "^DP-3" | grep "disconnected")
#   then
#     xrandr --output DP-3 --primary --same-as eDP-1 --auto
# elif ! (xrandr | grep "^DP-4" | grep "disconnected")
#   then
#     xrandr --output DP-4 --primary --same-as eDP-1 --auto
# else
#     xrandr --output DP-3 --off --output HDMI-1 --off --output DP-2 --off --output DP-1 --off --output DP-4 --off --output eDP-1 --primary --auto
# fi
